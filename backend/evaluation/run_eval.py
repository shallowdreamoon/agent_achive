from pathlib import Path

from backend.evaluation.benchmark import BenchmarkRunner
from backend.tools.evaluation_tool import EvaluationTool


if __name__ == "__main__":
    runner = BenchmarkRunner(EvaluationTool())
    out = runner.run(Path(__file__).resolve().parent / "results.json")
    print(out)
