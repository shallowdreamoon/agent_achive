from typing import Dict, List


class ReasoningTool:
    name = "reasoning_tool"

    def run(self, agent: str, query: str, evidence: List[Dict]) -> Dict:
        top = evidence[0] if evidence else {"risk_type": "Unknown", "country": "N/A", "advice": "Need more data"}
        if agent == "qa":
            return {
                "risk_type": top.get("risk_type", "Unknown"),
                "country": top.get("country", "N/A"),
                "analysis": f"针对问题‘{query}’，主要风险为{top.get('risk_type', 'Unknown')}。",
                "suggestion": top.get("advice", "补充检索证据后再决策。"),
            }
        if agent == "layout":
            return {
                "application_type": "PCT + National Phase",
                "timeline": "0-12个月优先权布局，30个月进入目标国家",
                "regions": sorted(list({x.get("country", "N/A") for x in evidence})),
                "strategy": top.get("advice", "先核心专利后外围专利。"),
            }
        return {
            "risk_judgement": "Medium" if evidence else "Unknown",
            "legal_path": "证据保全 → 律师函回应 → 无效/和解/诉讼",
            "key_factor": top.get("risk_type", "Unknown"),
            "recommendation": top.get("advice", "建立诉讼时间线并准备应诉材料。"),
        }
