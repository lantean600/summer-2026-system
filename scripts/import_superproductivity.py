#!/usr/bin/env python3
"""Import Super Productivity backup data into repo CSV summaries."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


DEFAULT_BACKUP_DIR = Path.home() / "AppData" / "Roaming" / "superProductivity" / "backups"
OUT_DIR = Path("data") / "super-productivity"

TASK_DETAIL_FIELDS = [
    "source_file",
    "imported_at",
    "week",
    "task_id",
    "title",
    "project_id",
    "project_title",
    "is_done",
    "created_at",
    "due_at",
    "done_at",
    "estimate_minutes",
    "actual_minutes",
    "repeat_cfg_id",
    "notes",
]

DAILY_FIELDS = [
    "date",
    "week",
    "project_title",
    "total_tasks",
    "done_tasks",
    "estimate_minutes",
    "actual_minutes",
]

WEEKLY_FIELDS = [
    "week",
    "start_date",
    "end_date",
    "total_tasks",
    "done_tasks",
    "completion_rate",
    "estimate_minutes",
    "actual_minutes",
]

PROJECT_WEEKLY_FIELDS = [
    "week",
    "project_title",
    "total_tasks",
    "done_tasks",
    "completion_rate",
    "estimate_minutes",
    "actual_minutes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import the newest Super Productivity JSON backup into data/super-productivity."
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Specific Super Productivity backup JSON file. Defaults to newest backup.",
    )
    parser.add_argument(
        "--backup-dir",
        type=Path,
        default=DEFAULT_BACKUP_DIR,
        help=f"Backup directory to scan when --input is omitted. Default: {DEFAULT_BACKUP_DIR}",
    )
    return parser.parse_args()


def newest_backup(backup_dir: Path) -> Path:
    if not backup_dir.exists():
        raise FileNotFoundError(f"Backup directory not found: {backup_dir}")
    files = [path for path in backup_dir.glob("*.json") if path.is_file()]
    if not files:
        raise FileNotFoundError(f"No JSON backups found in: {backup_dir}")
    return max(files, key=lambda path: path.stat().st_mtime)


def ms_to_dt(value: Any) -> datetime | None:
    if value in (None, "", 0):
        return None
    try:
        return datetime.fromtimestamp(int(value) / 1000).astimezone()
    except (TypeError, ValueError, OSError):
        return None


def dt_text(value: Any) -> str:
    dt = ms_to_dt(value)
    return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else ""


def minutes(value: Any) -> int:
    try:
        return round(int(value or 0) / 60000)
    except (TypeError, ValueError):
        return 0


def day_from_ms(value: Any) -> str:
    dt = ms_to_dt(value)
    return dt.strftime("%Y-%m-%d") if dt else ""


def week_from_day(day: str) -> str:
    if not day:
        return ""
    date_value = datetime.strptime(day, "%Y-%m-%d").date()
    iso = date_value.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def week_bounds(week: str) -> tuple[str, str]:
    if not week:
        return "", ""
    year_text, week_text = week.split("-W")
    monday = datetime.fromisocalendar(int(year_text), int(week_text), 1).date()
    sunday = monday + timedelta(days=6)
    return monday.isoformat(), sunday.isoformat()


def completion_rate(done: int, total: int) -> str:
    if not total:
        return "0.00"
    return f"{done / total:.2f}"


def entity_values(section: dict[str, Any] | None) -> list[dict[str, Any]]:
    entities = (section or {}).get("entities") or {}
    return [value for value in entities.values() if isinstance(value, dict)]


def collect_tasks(data: dict[str, Any]) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    tasks.extend(entity_values(data.get("task")))
    tasks.extend(entity_values((data.get("archiveYoung") or {}).get("task")))
    tasks.extend(entity_values((data.get("archiveOld") or {}).get("task")))

    unique: dict[str, dict[str, Any]] = {}
    for task in tasks:
        task_id = task.get("id")
        if task_id:
            unique[task_id] = task
    return list(unique.values())


def project_titles(data: dict[str, Any]) -> dict[str, str]:
    return {
        project.get("id", ""): project.get("title") or project.get("id", "")
        for project in entity_values(data.get("project"))
    }


def task_day(task: dict[str, Any]) -> str:
    for key in ("dueWithTime", "doneOn", "created"):
        day = day_from_ms(task.get(key))
        if day:
            return day
    return ""


def actual_minutes(task: dict[str, Any]) -> int:
    time_spent = minutes(task.get("timeSpent"))
    if time_spent:
        return time_spent
    by_day = task.get("timeSpentOnDay") or {}
    if isinstance(by_day, dict):
        return sum(minutes(value) for value in by_day.values())
    return 0


def add_actual_by_day(
    daily: dict[tuple[str, str], dict[str, Any]],
    task: dict[str, Any],
    default_day: str,
    project_title: str,
) -> None:
    by_day = task.get("timeSpentOnDay") or {}
    if isinstance(by_day, dict) and by_day:
        for day, spent_ms in by_day.items():
            daily[(day, project_title)]["actual_minutes"] += minutes(spent_ms)
        return
    daily[(default_day, project_title)]["actual_minutes"] += minutes(task.get("timeSpent"))


def round_row(row: dict[str, Any], fields: list[str]) -> dict[str, Any]:
    return {field: row.get(field, "") for field in fields}


def write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(round_row(row, fields))


def main() -> None:
    args = parse_args()
    source = args.input if args.input else newest_backup(args.backup_dir)
    source = source.resolve()
    imported_at = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")

    with source.open("r", encoding="utf-8-sig") as file:
        backup = json.load(file)

    data = backup.get("data") if isinstance(backup.get("data"), dict) else backup
    projects = project_titles(data)
    tasks = collect_tasks(data)

    detail_rows: list[dict[str, Any]] = []
    daily = defaultdict(lambda: {"total_tasks": 0, "done_tasks": 0, "estimate_minutes": 0, "actual_minutes": 0})

    for task in tasks:
        project_id = task.get("projectId") or ""
        project_title = projects.get(project_id, project_id or "Unknown")
        day = task_day(task)
        week = week_from_day(day)
        is_done = bool(task.get("isDone"))
        estimate = minutes(task.get("timeEstimate"))

        detail_rows.append(
            {
                "source_file": source.name,
                "imported_at": imported_at,
                "week": week,
                "task_id": task.get("id", ""),
                "title": task.get("title", ""),
                "project_id": project_id,
                "project_title": project_title,
                "is_done": str(is_done).lower(),
                "created_at": dt_text(task.get("created")),
                "due_at": dt_text(task.get("dueWithTime")),
                "done_at": dt_text(task.get("doneOn")),
                "estimate_minutes": estimate,
                "actual_minutes": actual_minutes(task),
                "repeat_cfg_id": task.get("repeatCfgId", ""),
                "notes": task.get("notes", ""),
            }
        )

        daily[(day, project_title)]["total_tasks"] += 1
        daily[(day, project_title)]["done_tasks"] += 1 if is_done else 0
        daily[(day, project_title)]["estimate_minutes"] += estimate
        add_actual_by_day(daily, task, day, project_title)

    daily_rows = [
        {
            "date": day,
            "week": week_from_day(day),
            "project_title": project_title,
            **values,
        }
        for (day, project_title), values in daily.items()
    ]
    daily_rows.sort(key=lambda row: (row["date"], row["project_title"]))

    weekly = defaultdict(lambda: {"total_tasks": 0, "done_tasks": 0, "estimate_minutes": 0, "actual_minutes": 0})
    project_weekly = defaultdict(lambda: {"total_tasks": 0, "done_tasks": 0, "estimate_minutes": 0, "actual_minutes": 0})
    for row in daily_rows:
        week = row["week"]
        weekly[week]["total_tasks"] += row["total_tasks"]
        weekly[week]["done_tasks"] += row["done_tasks"]
        weekly[week]["estimate_minutes"] += row["estimate_minutes"]
        weekly[week]["actual_minutes"] += row["actual_minutes"]

        key = (week, row["project_title"])
        project_weekly[key]["total_tasks"] += row["total_tasks"]
        project_weekly[key]["done_tasks"] += row["done_tasks"]
        project_weekly[key]["estimate_minutes"] += row["estimate_minutes"]
        project_weekly[key]["actual_minutes"] += row["actual_minutes"]

    weekly_rows = []
    for week, values in weekly.items():
        start_date, end_date = week_bounds(week)
        weekly_rows.append(
            {
                "week": week,
                "start_date": start_date,
                "end_date": end_date,
                **values,
                "completion_rate": completion_rate(values["done_tasks"], values["total_tasks"]),
            }
        )
    weekly_rows.sort(key=lambda row: row["week"])

    project_weekly_rows = []
    for (week, project_title), values in project_weekly.items():
        project_weekly_rows.append(
            {
                "week": week,
                "project_title": project_title,
                **values,
                "completion_rate": completion_rate(values["done_tasks"], values["total_tasks"]),
            }
        )
    project_weekly_rows.sort(key=lambda row: (row["week"], row["project_title"]))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(OUT_DIR / "task-detail.csv", TASK_DETAIL_FIELDS, detail_rows)
    write_csv(OUT_DIR / "daily-summary.csv", DAILY_FIELDS, daily_rows)
    write_csv(OUT_DIR / "weekly-summary.csv", WEEKLY_FIELDS, weekly_rows)
    write_csv(OUT_DIR / "project-weekly-summary.csv", PROJECT_WEEKLY_FIELDS, project_weekly_rows)
    (OUT_DIR / "latest-import.json").write_text(
        json.dumps(
            {
                "source_file": str(source),
                "imported_at": imported_at,
                "task_count": len(detail_rows),
                "daily_rows": len(daily_rows),
                "weekly_rows": len(weekly_rows),
                "project_weekly_rows": len(project_weekly_rows),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"Imported {len(detail_rows)} tasks from {source}")
    print(f"Wrote {OUT_DIR}")


if __name__ == "__main__":
    main()
