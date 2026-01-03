from typing import Dict
from backend.services.knowledge_base import KnowledgeBase

class QuestionClassifier:
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        self.categories = ["账户类", "信用卡类", "基础业务类", "常见操作类"]
    
    def classify(self, question: str) -> str:
        """分类问题"""
        question_lower = question.lower()
        
        # 关键词映射
        category_keywords = {
            "账户类": ["账户", "银行卡", "余额", "交易明细", "冻结", "解冻", "挂失", "补办", "流水"],
            "信用卡类": ["信用卡", "账单", "还款", "额度", "逾期", "罚息", "积分", "兑换", "滞纳金"],
            "基础业务类": ["手机银行", "网上银行", "网银", "注册", "登录", "转账", "限额", "手续费", "利率", "存款"],
            "常见操作类": ["密码", "重置", "短信提醒", "解绑", "绑定", "开通", "关闭", "修改"]
        }
        
        # 计算每个类别的匹配分数
        scores = {}
        for category, keywords in category_keywords.items():
            score = sum(1 for kw in keywords if kw in question_lower)
            scores[category] = score
        
        # 返回得分最高的类别
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        
        return "未知类别"


