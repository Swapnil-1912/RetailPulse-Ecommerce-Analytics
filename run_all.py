"""Runs Steps 1-4 in order. Stops if any step fails."""
import subprocess, sys

STEPS = [
    "notebooks/01_data_cleaning.py",
    "notebooks/02_eda.py",
    "notebooks/03_rfm_segmentation.py",
    "notebooks/04_load_to_sql.py",
]
for i, script in enumerate(STEPS, 1):
    print(f"\n===== STEP {i}: {script} =====")
    if subprocess.run([sys.executable, script]).returncode != 0:
        sys.exit(f"Step {i} failed. Fix the error above and re-run.")
print("\nAll steps done. Next: run the SQL queries, then build the Power BI dashboard (see STEPS.md).")
