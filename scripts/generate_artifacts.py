import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "outputs" / "benchmark_summary.json"
DETAIL = ROOT / "outputs" / "benchmark_results.json"
BENCH_SVG = ROOT / "docs" / "benchmark-chart.svg"
UI_PLACEHOLDER = ROOT / "docs" / "ui-placeholder.svg"


def ensure_placeholder_ui() -> None:
    if UI_PLACEHOLDER.exists():
        return
    UI_PLACEHOLDER.parent.mkdir(parents=True, exist_ok=True)
    UI_PLACEHOLDER.write_text(
        """<svg xmlns='http://www.w3.org/2000/svg' width='960' height='540'>
<rect width='100%' height='100%' fill='#f8fafc'/>
<rect x='32' y='24' width='896' height='70' rx='12' fill='#ffffff' stroke='#cbd5e1'/>
<text x='52' y='67' font-size='28' fill='#0f172a'>IP Multi-Agent UI Screenshot Placeholder</text>
<text x='52' y='104' font-size='16' fill='#334155'>Replace this file with a real screenshot after running frontend.</text>
</svg>""",
        encoding="utf-8",
    )


def generate_benchmark_chart() -> None:
    if not SUMMARY.exists():
        return
    s = json.loads(SUMMARY.read_text(encoding="utf-8"))
    metrics = [
        ("overall", s["average_overall_score"]),
        ("keyword", s["keyword_match_score"]),
        ("evidence", s["evidence_hit_rate"]),
        ("structured", s["structured_output_validity"]),
    ]
    width, height = 760, 360
    bar_w, gap = 110, 40
    base_y = 300
    x = 60
    parts = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}'>", "<rect width='100%' height='100%' fill='#ffffff'/>"]
    for name, value in metrics:
        bh = int(200 * value)
        y = base_y - bh
        parts.append(f"<rect x='{x}' y='{y}' width='{bar_w}' height='{bh}' fill='#4f46e5' rx='8'/>")
        parts.append(f"<text x='{x+bar_w/2}' y='{y-8}' text-anchor='middle' font-size='13'>{value:.2f}</text>")
        parts.append(f"<text x='{x+bar_w/2}' y='320' text-anchor='middle' font-size='13'>{name}</text>")
        x += bar_w + gap
    parts.append("</svg>")
    BENCH_SVG.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    ensure_placeholder_ui()
    generate_benchmark_chart()
    if DETAIL.exists():
        print(f"Generated artifacts from {DETAIL}")
    else:
        print("No benchmark detail file yet. Run benchmark first.")


if __name__ == "__main__":
    main()
