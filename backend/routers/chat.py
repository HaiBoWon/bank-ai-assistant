from fastapi import APIRouter, HTTPException
from backend.models.question import ChatRequest, ChatResponse
from backend.services.llm_service import LLMService
from backend.services.knowledge_base import KnowledgeBase
from backend.services.question_classifier import QuestionClassifier

router = APIRouter(prefix="/api", tags=["chat"])

# 初始化服务（在实际应用中，这些应该通过依赖注入）
kb = KnowledgeBase()
# 初始化 LLM 服务
llm_service = LLMService()
classifier = QuestionClassifier(kb)

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """处理用户问题"""
    try:
        # 1. 分类问题
        category = classifier.classify(request.question)
        
        # 2. 搜索知识库
        kb_result = kb.search(request.question)
        
        # 3. 生成回答
        answer = None
        topic = None
        confidence = 0.5
        
        if kb_result:
            # 如果找到知识库匹配，尝试用 LLM 增强回答
            answer = kb_result['answer']
            topic = kb_result['topic']
            confidence = 0.9
            
            # 构建LLM上下文
            context = f"类别：{kb_result['category']}\n主题：{kb_result['topic']}\n知识库答案：{kb_result['answer']}"
            
            try:
                # 调用LLM服务增强回答
                llm_answer = await llm_service.generate_response(request.question, context)
                if llm_answer:
                    # LLM增强回答成功，使用增强后的回答
                    answer = llm_answer
            except Exception as e:
                # LLM请求失败，继续使用知识库答案
                print(f"LLM增强失败：{str(e)}")
                # 可以选择记录日志，但不影响用户体验
        else:
            # 没有找到匹配知识，直接返回提示信息（不调用 LLM，避免超时）
            answer = "抱歉，我暂时无法回答这个问题。建议您：\n1. 联系人工客服（电话：95588）\n2. 尝试使用更具体的关键词提问\n3. 访问银行官网或手机银行APP查询相关信息\n\n我可以帮您解答以下类型的问题：\n• 账户类：挂失、余额查询、交易明细、冻结/解冻\n• 信用卡类：账单查询、还款、额度提升、逾期罚息、积分兑换\n• 基础业务类：手机银行/网银注册、转账限额、手续费、利率查询\n• 常见操作类：密码重置、短信提醒、银行卡解绑"
        
        return ChatResponse(
            answer=answer or "抱歉，服务暂时不可用，请稍后重试。",
            category=category,
            topic=topic,
            confidence=confidence
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理请求时出错: {str(e)}")

@router.get("/health")
async def health():
    """健康检查"""
    return {"status": "ok", "message": "服务运行正常"}

