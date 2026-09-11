import platform
import subprocess
from pathlib import Path

# مسیر فایل targets.txt نسبت به محل همین فایل پایتون
project_folder = Path(__file__).parent
targets_file = project_folder / "data" / "targets.txt"

if not targets_file.exists():
    print("File not found:", targets_file)
    print("Please create data/targets.txt and add one host per line.")
    raise SystemExit(1)

for target in targets_file.read_text(encoding="utf-8").splitlines():
    target = target.strip()

    # رد کردن خط‌های خالی
    if not target:
        continue

    # در ویندوز -n و در macOS/Linux از -c استفاده می‌شود
    count_flag = "-n" if platform.system().lower() == "windows" else "-c"

    result = subprocess.run(
        ["ping", count_flag, "1", target],
        capture_output=True,
        text=True
    )

    status = "ONLINE" if result.returncode == 0 else "OFFLINE"
    print(f"{target}: {status}")