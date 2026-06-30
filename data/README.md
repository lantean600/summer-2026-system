# Data

This directory is generated from external source data. Do not maintain manual CSV files here.

## Super Productivity

Run the importer from the repository root:

```powershell
python scripts/import_superproductivity.py
```

By default, it reads the newest JSON backup from:

```text
C:\Users\Lenovo\AppData\Roaming\superProductivity\backups
```

To import a specific backup:

```powershell
python scripts/import_superproductivity.py --input C:\path\backup.json
```

Generated files are written to `data/super-productivity/` and may be overwritten on every run:

- `task-detail.csv`: one row per task
- `daily-summary.csv`: daily totals by project
- `weekly-summary.csv`: weekly totals
- `project-weekly-summary.csv`: weekly totals by project
- `latest-import.json`: import metadata
