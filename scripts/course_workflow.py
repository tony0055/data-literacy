#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Emit the course request contract without starting a model or creating a project.

Run: python3 scripts/course_workflow.py slides gpt-6-astra
Modes: analysis, visualization, slides, practice, midterm, team.
"""
import json
from pathlib import Path
import sys
from typing import Final, TypedDict

ROOT: Final = Path(__file__).resolve().parents[1]
KNOWLEDGE: Final = "school/school_project/course-domain"
MODES: Final = (
    "analysis", "visualization", "slides", "practice", "midterm", "team",
)
COMMON: Final = (
    f"{KNOWLEDGE}/README.md", f"{KNOWLEDGE}/concepts.md",
    f"{KNOWLEDGE}/method-selector.md", "docs/course-workflow.md",
)
DECK: Final = (
    "docs/data-to-slides-workflow.md", f"{KNOWLEDGE}/presentation-patterns.md",
)

class CourseContract(TypedDict):
    mode: str
    model: str
    reads: list[str]
    steps: list[str]
    artifacts: list[str]
    deploy: bool
    worker_model: str
    decision_model: str


def contract(mode: str, model: str) -> CourseContract:
    """Preserve the selected model and return request-specific artifacts."""
    if mode not in MODES or not model.strip():
        raise ValueError((mode, model))
    reads = list(COMMON)
    steps = ["concept", "specification", "source_diagnosis"]
    artifacts = ["spec.md", "sources.csv", "diagnosis.json", "verification.md", "ai-use.csv"]
    match mode:
        case "analysis":
            steps.extend(["approved_cleaning", "analysis", "independent_check"])
            artifacts.extend(["cleaning-log.csv", "analysis.py", "report.md"])
        case "visualization":
            steps.extend(["chart_question", "aggregation", "chart_render", "chart_check"])
            artifacts.extend(["chart-data.csv", "figures/", "chart-notes.md"])
        case "slides":
            reads.extend(DECK)
            steps.extend(["verified_analysis", "story", "design_standard", "render", "browser_check"])
            artifacts.extend(["report.md", "presentation/index.html", "speaker-notes.md"])
        case "practice":
            reads.append(f"{KNOWLEDGE}/assessments.md")
            steps.extend(["assessment_scope", "task_execution", "independent_check", "submission_check"])
            artifacts.append("task-results/")
        case "midterm" | "team":
            reads.append(f"{KNOWLEDGE}/assessments.md")
            steps.extend(["assessment_scope", "analysis", "sensitivity_check", "submission_check"])
            artifacts.extend(["cleaning-log.csv", "analysis.py", "report.md"])
            if mode == "team":
                reads.extend(DECK)
                steps.extend(["story", "design_standard", "render", "browser_check"])
                artifacts.extend(["plan.md", "presentation/index.html", "speaker-notes.md"])
        case _:
            raise ValueError(mode)
    return {
        "mode": mode, "model": model,
        "reads": reads, "steps": steps,
        "artifacts": artifacts, "deploy": False,
        "worker_model": model,
        "decision_model": model,
    }


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        result = contract(sys.argv[1], sys.argv[2])
    except ValueError as error:
        print(f"Invalid course mode/model: {error}", file=sys.stderr)
        return 2
    missing = [path for path in result["reads"] if not (ROOT / path).is_file()]
    if missing:
        print(f"Missing workflow documents: {missing}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
