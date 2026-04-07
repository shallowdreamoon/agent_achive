import json
from pathlib import Path
from typing import Dict, List

from backend.models.schemas import BenchmarkCase
from backend.tools.evaluation_tool import EvaluationTool


class BenchmarkRunner:
    def __init__(self, router, evaluation_tool: EvaluationTool, dataset_path: Path):
        self.router = router
        self.evaluation_tool = evaluation_tool
        self.dataset_path = dataset_path

    def _load_cases(self) -> List[BenchmarkCase]:
        payload = json.loads(self.dataset_path.read_text(encoding="utf-8"))
        return [BenchmarkCase.model_validate(item) for item in payload]

    def run(self, output_dir: Path) -> Dict:
        cases = self._load_cases()
        detail_rows = []
        for case in cases:
            agent_name = case.task_type
            agent = self.router.dispatch(agent_name)
            run = agent.run(query=case.input["query"], extra_params=case.input.get("extra_params", {}))
            metrics = self.evaluation_tool.score_case(
                output=run["structured_result"],
                reference=case.reference,
                expected_keywords=case.expected_keywords,
                evidence=run["evidence"],
            )
            detail_rows.append(
                {
                    "id": case.id,
                    "agent": agent_name,
                    **metrics,
                }
            )

        src_summary = self.evaluation_tool.summarize(detail_rows)
        summary = {
            "average_score": src_summary["average_overall_score"],
            "task_coverage": src_summary["task_coverage"],
            "evidence_hit_rate": src_summary["evidence_hit_rate"],
            "structured_output_validity": src_summary["structured_output_validity"],
        }

        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "benchmark_results.json").write_text(json.dumps(detail_rows, ensure_ascii=False, indent=2), encoding="utf-8")
        (output_dir / "benchmark_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"summary": summary, "details": detail_rows}
