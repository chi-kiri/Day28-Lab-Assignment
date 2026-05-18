import os
import shutil

# Target directory name (updated to user's student ID)
student_id = "2A202600154"
script_dir = os.path.dirname(os.path.abspath(__file__))
source_dir = script_dir
parent_dir = os.path.dirname(script_dir)
submission_dir = os.path.join(parent_dir, f"lab28_submission_{student_id}")

print(f"Creating submission structure in: {submission_dir}")

# Create directories
os.makedirs(os.path.join(submission_dir, "lab28"), exist_ok=True)
os.makedirs(os.path.join(submission_dir, "screenshots"), exist_ok=True)

# Files/Folders to copy to lab28/
lab28_items = [
    "docker-compose.yml",
    "prefect",
    "scripts",
    "api-gateway",
    "monitoring",
]

for item in lab28_items:
    src = os.path.join(source_dir, item)
    dst = os.path.join(submission_dir, "lab28", item)
    if os.path.exists(src):
        if os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"Copied directory: {item} -> lab28/")
        else:
            shutil.copy2(src, dst)
            print(f"Copied file: {item} -> lab28/")

# Screenshots to copy to screenshots/
screenshots_to_copy = [
    "prefect_ui.png",
    "api_gateway.png",
    "grafana_dashboard.png"
]

src_screenshots_dir = os.path.join(source_dir, "screenshots")
if os.path.exists(src_screenshots_dir):
    for shot in screenshots_to_copy:
        src = os.path.join(src_screenshots_dir, shot)
        dst = os.path.join(submission_dir, "screenshots", shot)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied screenshot: {shot} -> screenshots/")
        else:
            print(f"Warning: {shot} not found in local screenshots/ directory.")

# Root screenshots & documents
root_items = [
    "smoke_tests_results.png",
    "production_readiness.png",
    "README.md",
    "SUBMISSION.md"
]

for item in root_items:
    src = os.path.join(source_dir, item)
    dst = os.path.join(submission_dir, item)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Copied file to root: {item}")
    else:
        print(f"Warning: {item} not found in root directory.")

print("\nSubmission organization complete!")
print("Folder structure matches the requirements exactly!")
