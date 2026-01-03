import os
from typing import Optional
from openai import OpenAI
import asyncio

class LLMService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY 环境变量未设置")
        
        # 读取基础URL配置
        base_url = os.getenv("LLM_BASE_URL")
        
        client_params = {
            "api_key": api_key,
            "timeout": 30.0  # 设置30秒超时
        }
        if base_url:
            client_params["base_url"] = base_url  # 添加base_url配置
            print(f"已配置基础URL: {base_url}")
        
        self.client = OpenAI(**client_params)
        self.model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
        print(f"LLM服务初始化成功，模型: {self.model}, 基础URL: {base_url or '默认'}")
    
    async def generate_response(
        self, 
        user_question: str, 
        context: Optional[str] = None
    ) -> str:
        """生成回答"""
        system_prompt = """你是一个专业的银行智能客服助手。
请根据提供的知识库信息，准确、友好地回答用户的问题。
回答要简洁明了，条理清晰，使用序号或分点说明。
如果问题不在知识库范围内，请礼貌地告知用户并建议联系人工客服（电话：95588）。"""
        
        messages = [
            {"role": "system", "content": system_prompt},
        ]
        
        if context:
            messages.append({
                "role": "system", 
                "content": f"相关知识库信息：\n{context}"
            })
        
        messages.append({
            "role": "user", 
            "content": user_question
        })
        
        try:
            # 在线程池中运行同步的 OpenAI 调用，避免阻塞
            def call_openai():
                print(f"正在调用 LLM API，模型：{self.model}")
                print(f"用户问题：{user_question}")
                print(f"上下文信息：{context}")
                
                try:
                    return self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        temperature=0.7,
                        max_tokens=500
                    )
                except Exception as inner_e:
                    print(f"OpenAI客户端内部错误：{str(inner_e)}")
                    print(f"错误类型：{type(inner_e).__name__}")
                    raise
            
            loop = asyncio.get_event_loop()
            response = await asyncio.wait_for(
                loop.run_in_executor(None, call_openai),
                timeout=20.0  # 增加超时时间到20秒
            )
            
            print(f"LLM API 调用成功")
            return response.choices[0].message.content
        except asyncio.TimeoutError:
            print(f"LLM API 调用超时，模型：{self.model}")
            return None  # 返回 None 表示超时，让调用方处理
        except Exception as e:
            print(f"LLM API 调用错误: {str(e)}")
            print(f"错误类型：{type(e).__name__}")
            return None  # 返回 None 表示错误，让调用方处理

