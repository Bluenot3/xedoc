"""Manage daily focus tasks.

This script allows you to add, list, or clear tasks stored in a JSON file
named ``focus.json`` placed in the same directory. Each task includes the
text you provide and a timestamp recorded in ISO8601 format.

Examples::

  python daily_focus.py --add "Write report"
  python daily_focus.py --list
  python daily_focus.py --clear
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
import textwrap

FOCUS_FILE = Path(__file__).with_name("focus.json")


def load_tasks() -> list[dict[str, str]]:
    if FOCUS_FILE.exists():
        try:
            data = json.loads(FOCUS_FILE.read_text())
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass
    return []


def save_tasks(tasks: list[dict[str, str]]) -> None:
    FOCUS_FILE.write_text(json.dumps(tasks, indent=2))


def add_task(text: str, tasks: list[dict[str, str]]) -> None:
    timestamp = datetime.now().replace(microsecond=0).isoformat()
    tasks.append({"text": text, "timestamp": timestamp})
    save_tasks(tasks)
    print(f"Added: {text}")


def list_tasks(tasks: list[dict[str, str]]) -> None:
    if not tasks:
        print("No tasks yet.")
        return
    for task in tasks:
        ts = task.get("timestamp", "")
        try:
            when = datetime.fromisoformat(ts).strftime("%Y-%m-%d %H:%M")
        except ValueError:
            when = ts
        print(f"\u2022 {when}  –  {task.get('text', '')}")


def clear_tasks() -> None:
    confirm = input("Erase all tasks? type 'yes' to confirm: ")
    if confirm == "yes":
        save_tasks([])
        print("Tasks cleared.")
    else:
        print("Aborted.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage a simple list of focus tasks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """Examples:
  python daily_focus.py --add \"Write report\"
  python daily_focus.py --list
  python daily_focus.py --clear"""
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--add", metavar="TEXT", help="add a new task")
    group.add_argument("--list", action="store_true", help="list tasks")
    group.add_argument("--clear", action="store_true", help="remove all tasks")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    tasks = load_tasks()
    if args.add is not None:
        add_task(args.add, tasks)
    elif args.list:
        list_tasks(tasks)
    elif args.clear:
        clear_tasks()


if __name__ == "__main__":
    main()
