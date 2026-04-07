from typing import Any, Dict, List


class EvaluationTool:
    name = "evaluation_tool"

    def score_case(self, output: Dict[str, Any], reference: Dict[str, Any], expected_keywords: List[str], evidence: List[Dict]) -> Dict[str, float]:
        text = str(output).lower()
        keyword_hit = 0.0
        if expected_keywords:
            hit_count = sum(1 for k in expected_keywords if k.lower() in text)
            keyword_hit = hit_count / len(expected_keywords)

        structured_valid = 1.0 if all(key in output for key in reference.keys()) else 0.0
        evidence_hit = 1.0 if evidence else 0.0

        overall = 0.4 * keyword_hit + 0.35 * structured_valid + 0.25 * evidence_hit
        return {
            "overall_score": round(overall, 4),
            "keyword_match": round(keyword_hit, 4),
            "structured_valid": round(structured_valid, 4),
            "evidence_hit": round(evidence_hit, 4),
        }

    def summarize(self, case_scores: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not case_scores:
            return {
                "task_coverage": 0.0,
                "evidence_hit_rate": 0.0,
                "structured_output_validity": 0.0,
                "keyword_match_score": 0.0,
                "average_overall_score": 0.0,
                "per_agent_score": {},
            }

        n = len(case_scores)
        agent_scores: Dict[str, List[float]] = {}
        for row in case_scores:
            agent_scores.setdefault(row["agent"], []).append(row["overall_score"])

        return {
            "task_coverage": round(len(agent_scores) / 3.0, 4),
            "evidence_hit_rate": round(sum(x["evidence_hit"] for x in case_scores) / n, 4),
            "structured_output_validity": round(sum(x["structured_valid"] for x in case_scores) / n, 4),
            "keyword_match_score": round(sum(x["keyword_match"] for x in case_scores) / n, 4),
            "average_overall_score": round(sum(x["overall_score"] for x in case_scores) / n, 4),
            "per_agent_score": {k: round(sum(v) / len(v), 4) for k, v in agent_scores.items()},
        }
