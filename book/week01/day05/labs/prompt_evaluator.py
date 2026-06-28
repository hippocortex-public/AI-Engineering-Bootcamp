"""
Lab — Prompt Evaluator

Objectif :
Évaluer localement une stratégie de classification de tickets.

Ce lab ne dépend d'aucune API externe. Il simule une étape d'évaluation
pour apprendre la démarche AI Engineering : dataset, prédiction, validation,
score et analyse d'erreurs.

Exécution :
python book/week01/day05_prompt_engineering/labs/prompt_evaluator.py
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

Category = Literal["BUG", "QUESTION", "FEATURE_REQUEST", "OTHER"]


@dataclass(frozen=True)
class TestCase:
    id: str
    ticket: str
    expected: Category


@dataclass(frozen=True)
class EvaluationResult:
    id: str
    expected: Category
    predicted: Category
    passed: bool
    reason: str


def load_cases(path: Path) -> list[TestCase]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [TestCase(**item) for item in data]


def classify_ticket(ticket: str) -> Category:
    """
    Simulateur déterministe.

    Dans un vrai système, cette fonction serait remplacée par :
    - un appel LLM ;
    - un prompt template ;
    - une validation de sortie ;
    - une stratégie de retry ou fallback.

    Le but ici est de tester la mécanique d'évaluation.
    """
    text = ticket.lower()

    bug_keywords = [
        "erreur",
        "error",
        "500",
        "403",
        "bug",
        "plante",
        "crash",
        "timeout",
        "ne fonctionne pas",
    ]
    feature_keywords = [
        "ajouter",
        "pouvez-vous ajouter",
        "nouvelle fonctionnalité",
        "feature",
        "mode sombre",
        "export csv",
    ]
    question_keywords = [
        "comment",
        "où",
        "pourquoi",
        "puis-je",
        "changer",
        "modifier",
    ]

    # Priorité aux bugs pour résister aux injections simples.
    if any(keyword in text for keyword in bug_keywords):
        return "BUG"
    if any(keyword in text for keyword in feature_keywords):
        return "FEATURE_REQUEST"
    if any(keyword in text for keyword in question_keywords):
        return "QUESTION"
    return "OTHER"


def explain_prediction(ticket: str, predicted: Category) -> str:
    if predicted == "BUG":
        return "Le ticket contient un signal de dysfonctionnement ou de code d'erreur."
    if predicted == "QUESTION":
        return "Le ticket formule une demande d'information ou d'aide."
    if predicted == "FEATURE_REQUEST":
        return "Le ticket demande une amélioration ou une nouvelle fonctionnalité."
    return "Le ticket ne correspond pas clairement aux catégories principales."


def evaluate(cases: list[TestCase]) -> list[EvaluationResult]:
    results: list[EvaluationResult] = []
    for case in cases:
        predicted = classify_ticket(case.ticket)
        results.append(
            EvaluationResult(
                id=case.id,
                expected=case.expected,
                predicted=predicted,
                passed=predicted == case.expected,
                reason=explain_prediction(case.ticket, predicted),
            )
        )
    return results


def accuracy(results: list[EvaluationResult]) -> float:
    if not results:
        return 0.0
    return sum(result.passed for result in results) / len(results)


def render_report(results: list[EvaluationResult]) -> str:
    lines = [
        "# Rapport d'évaluation",
        "",
        "| ID | Attendu | Prédit | Statut | Raison |",
        "|---|---|---|---|---|",
    ]

    for result in results:
        status = "PASS" if result.passed else "FAIL"
        lines.append(
            f"| {result.id} | {result.expected} | {result.predicted} | {status} | {result.reason} |"
        )

    lines.extend(
        [
            "",
            f"Accuracy: {accuracy(results):.2%}",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    current_dir = Path(__file__).resolve().parent
    cases = load_cases(current_dir / "sample_tasks.json")
    results = evaluate(cases)
    print(render_report(results))


if __name__ == "__main__":
    main()
