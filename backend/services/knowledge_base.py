import json
from typing import Dict, List, Optional
from pathlib import Path

class KnowledgeBase:
    def __init__(self, data_path: str = "backend/data/knowledge_base.json"):
        self.data_path = Path(data_path)
        self.knowledge: Dict = {}
        self.load_knowledge()
    
    def load_knowledge(self):
        """加载知识库"""
        if self.data_path.exists():
            with open(self.data_path, 'r', encoding='utf-8') as f:
                self.knowledge = json.load(f)
        else:
            raise FileNotFoundError(f"知识库文件不存在: {self.data_path}")
    
    def search(self, question: str) -> Optional[Dict]:
        """搜索匹配的知识库条目"""
        question_lower = question.lower()
        
        # 遍历所有类别和问题
        for category, items in self.knowledge.items():
            for key, item in items.items():
                # 检查问题是否匹配
                question_list = item.get("question", [])
                if isinstance(question_list, str):
                    question_list = [question_list]
                
                if any(q.lower() in question_lower for q in question_list):
                    return {
                        "category": category,
                        "topic": key,
                        "answer": item["answer"],
                        "keywords": item.get("keywords", [])
                    }
                
                # 关键词匹配
                keywords = item.get("keywords", [])
                if isinstance(keywords, str):
                    keywords = [keywords]
                
                if any(kw.lower() in question_lower for kw in keywords):
                    return {
                        "category": category,
                        "topic": key,
                        "answer": item["answer"],
                        "keywords": item.get("keywords", [])
                    }
        
        return None
    
    def get_by_category(self, category: str) -> Dict:
        """按类别获取知识"""
        return self.knowledge.get(category, {})
    
    def get_all_categories(self) -> List[str]:
        """获取所有类别"""
        return list(self.knowledge.keys())


