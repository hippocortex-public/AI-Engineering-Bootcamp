"""
Lab — Production architecture for AI systems.

Run:
    python book/week05/day01/labs/production_architecture_lab.py
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[4]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_platform.architecture import (  # noqa: E402
    ProductionArchitectureValidator,
    build_support_ai_blueprint,
    render_mermaid,
    summarize_readiness,
)


def demo() -> None:
    blueprint = build_support_ai_blueprint(sensitive_actions_enabled=True)
    report = ProductionArchitectureValidator().validate(blueprint)
    print(summarize_readiness(report))
    print()
    print("Architecture JSON excerpt:")
    print(blueprint.to_json()[:800] + "...")
    print()
    print("Mermaid:")
    print(render_mermaid(blueprint))


if __name__ == "__main__":
    demo()
