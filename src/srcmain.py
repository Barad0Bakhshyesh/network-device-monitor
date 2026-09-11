import csv
import platform
import subprocess
from datetime import datetime
from pathlib import Path

# فولدری که فایل srcmain.py داخلش است
project_folder = Path(__file__).resolve().parent.parent
# مسیر فایل ورودی:
# network-device-monitor/data/targets.txt
targets_file = project_folder / "data" / "targets.txt"

# مسیر فایل خروجی:
# network-device-monitor/reports/ping_report.csv
reports_folder = project_folder / "reports"
report_file = reports_folder / "ping_report.csv"

print(f"Looking for targets here: {targets_file}")

if not targets_file.is_file():
    print("\nERROR: targets.txt was not found.")
    print("Your files must be arranged like this:")
    print("network-device-monitor/")
    print("├── srcmain.py")
    print("└── data/")
    print("    └── targets.txt")
    raise SystemExit(1)

# اگر reports وجود ندارد، خودش آن را می‌سازد
reports_folder.mkdir(exist_ok=True)

# خواندن آدرس‌ها از data/targets.txt
targets = targets_file.read_text(encoding="utf-8").splitlines()

results = []

for target in targets:
    target = target.strip()

    # خط خالی را نادیده می‌گیرد
    if not target:
        continue

    # -n برای ویندوز، -c برای Linux/macOS
    ping_count = "-n" if platform.system() == "Windows" else "-c"

    ping_result = subprocess.run(
        ["ping", ping_count, "1", target],
        capture_output=True,
        text=True
    )

    status = "ONLINE" if ping_result.returncode == 0 else "OFFLINE"

    print(f"{target}: {status}")

    results.append({
        "host": target,
        "status": status,
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# ذخیره گزارش CSV
with report_file.open("w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(
        csv_file,
        fieldnames=["host", "status", "checked_at"]
    )
    writer.writeheader()
    writer.writerows(results)

print(f"\nCSV report created: {report_file}")