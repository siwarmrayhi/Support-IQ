"""Evalue le pipeline complet (retrieve + grade + generate/escalate)
sur les 20 tickets du dataset."""

import json
import time

from supportiq.config import settings
from supportiq.graph.workflow import graph

PAUSE_BETWEEN_TICKETS = 5  # secondes, marge de securite face au quota


def load_dataset() -> list[dict]:
    path = settings.raw_data_dir.parent.parent / "eval" / "dataset.jsonl"
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def run() -> None:
    tickets = load_dataset()

    correct_escalations = 0
    total_refusal_cases = 0
    correct_responses = 0
    wrong_escalations = 0
    total_answer_cases = 0

    for i, ticket in enumerate(tickets):
        result = graph.invoke({"ticket": ticket["ticket"]})
        expected = ticket["expected_status"]
        actual = result["status"]

        match = "OK  " if actual == expected else "MISS"
        print(f"[{match}] {ticket['id']:6s} attendu={expected:25s} obtenu={actual}")

        if expected == "human_review_required":
            total_refusal_cases += 1
            if actual == "human_review_required":
                correct_escalations += 1
        else:
            total_answer_cases += 1
            if actual == "auto_response":
                correct_responses += 1
            else:
                wrong_escalations += 1

        if i < len(tickets) - 1:
            time.sleep(PAUSE_BETWEEN_TICKETS)

    print(f"\n--- Cas de refus ({total_refusal_cases} tickets) ---")
    print(f"Escalades correctes : {correct_escalations}/{total_refusal_cases}")

    print(f"\n--- Cas de reponse attendue ({total_answer_cases} tickets) ---")
    print(f"Reponses correctes  : {correct_responses}/{total_answer_cases}")
    print(f"Escalades abusives  : {wrong_escalations}/{total_answer_cases}")


if __name__ == "__main__":
    run()