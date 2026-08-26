"""Executable lab for S4 J7 integration."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mini_framework.integration import build_support_framework


def run_demo():
    framework = build_support_framework()
    framework.memory.remember(
        user_id="user_123",
        key="preferred_tone",
        value="empathique et professionnel",
    )

    result = framework.run(
        user_id="user_123",
        message="Bonjour, ma commande est cassée et je souhaite un remboursement.",
        workflow_name="support_resolution",
    )
    return result


if __name__ == "__main__":
    demo_result = run_demo()
    print(demo_result.to_json())
