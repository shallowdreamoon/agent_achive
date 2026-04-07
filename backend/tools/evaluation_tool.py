from typing import Dict, List


class EvaluationTool:
    name = "evaluation_tool"

    def run(self, predictions: List[Dict]) -> Dict[str, float]:
        if not predictions:
            return {"accuracy": 0.0, "reasoning_score": 0.0, "task_coverage": 0.0}
        hits = sum(1 for x in predictions if x.get("has_evidence"))
        reasoning = sum(float(x.get("reasoning_depth", 0.0)) for x in predictions) / len(predictions)
        coverage = len(set(x.get("task", "unknown") for x in predictions)) / 3.0
        return {
            "accuracy": round(hits / len(predictions), 3),
            "reasoning_score": round(reasoning, 3),
            "task_coverage": round(min(1.0, coverage), 3),
        }
