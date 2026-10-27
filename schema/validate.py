#!/usr/bin/env python3
"""Валидация отчёта об инциденте без внешних зависимостей."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

SEVERITIES = {"low", "medium", "high", "critical"}
STATUSES = {"open", "contained", "eradicated", "recovered", "closed"}
REQUIRED: dict[str, type] = {
    "incident_id": str,
    "title": str,
    "severity": str,
    "status": str,
    "detected_at": str,
    "summary": str,
    "timeline": list,
    "affected_assets": list,
    "indicators": list,
    "root_cause": str,
    "actions": list,
}


def validate(document: dict[str, Any]) -> list[str]:
    """Вернуть список нарушений схемы."""
    errors: list[str] = []
    for field, expected in REQUIRED.items():
        if field not in document:
            errors.append(f"missing field: {field}")
        elif not isinstance(document[field], expected):
            errors.append(f"{field}: expected {expected.__name__}")

    severity = document.get("severity")
    if isinstance(severity, str) and severity not in SEVERITIES:
        errors.append(f"severity: expected one of {sorted(SEVERITIES)}")

    status = document.get("status")
    if isinstance(status, str) and status not in STATUSES:
        errors.append(f"status: expected one of {sorted(STATUSES)}")

    timeline = document.get("timeline")
    if isinstance(timeline, list):
        for index, event in enumerate(timeline):
            if not isinstance(event, dict):
                errors.append(f"timeline[{index}]: expected object")
                continue
            for key in ("timestamp", "event"):
                if key not in event:
                    errors.append(f"timeline[{index}]: missing {key}")

    actions = document.get("actions")
    if isinstance(actions, list):
        for index, action in enumerate(actions):
            if not isinstance(action, dict):
                errors.append(f"actions[{index}]: expected object")
                continue
            for key in ("action", "owner", "status"):
                if key not in action:
                    errors.append(f"actions[{index}]: missing {key}")

    return errors


def main(argv: list[str]) -> int:
    """Проверить переданные файлы, вернуть код выхода."""
    if not argv:
        print("usage: validate.py <report.json> [...]", file=sys.stderr)
        return 2

    failed = False
    for raw in argv:
        path = Path(raw)
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"{path}: {exc}", file=sys.stderr)
            failed = True
            continue

        if not isinstance(document, dict):
            print(f"{path}: root must be an object", file=sys.stderr)
            failed = True
            continue

        errors = validate(document)
        if errors:
            failed = True
            for error in errors:
                print(f"{path}: {error}", file=sys.stderr)
        else:
            print(f"{path}: ok")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
