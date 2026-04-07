import json
from pathlib import Path
from typing import Dict, List

from backend.tools.evaluation_tool import EvaluationTool


class BenchmarkRunner:
    def __init__(self, evaluation_tool: EvaluationTool):
        self.evaluation_tool = evaluation_tool

    def build_demo_predictions(self) -> List[Dict]:
        return [
            {"task": "qa", "has_evidence": True, "reasoning_depth": 0.88},
            {"task": "qa", "has_evidence": True, "reasoning_depth": 0.82},
            {"task": "qa", "has_evidence": True, "reasoning_depth": 0.79},
            {"task": "layout", "has_evidence": True, "reasoning_depth": 0.91},
            {"task": "layout", "has_evidence": True, "reasoning_depth": 0.84},
            {"task": "layout", "has_evidence": False, "reasoning_depth": 0.67},
            {"task": "litigation", "has_evidence": True, "reasoning_depth": 0.90},
            {"task": "litigation", "has_evidence": True, "reasoning_depth": 0.85},
            {"task": "litigation", "has_evidence": True, "reasoning_depth": 0.81},
        ]

    def run(self, output_path: Path) -> Dict:
        preds = self.build_demo_predictions()
        overall = self.evaluation_tool.run(preds)
        per_agent = {
            task: self.evaluation_tool.run([x for x in preds if x["task"] == task])
            for task in ["qa", "layout", "litigation"]
        }
        result = {**overall, "per_agent": per_agent}
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        return result
