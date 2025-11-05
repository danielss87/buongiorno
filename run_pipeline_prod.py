"""
Buongiorno - Production Pipeline Runner
Runs the pipeline for deployment environments (Render, etc.)
"""
import subprocess
import sys
import os
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent
pipeline_script = project_root / 'backend' / 'pipeline' / 'run_pipeline.py'

print("=" * 80)
print("🌅 BUONGIORNO - PRODUCTION PIPELINE EXECUTION")
print("=" * 80)
print(f"Project Root: {project_root}")
print(f"Pipeline Script: {pipeline_script}")
print()

# Change to pipeline directory
pipeline_dir = project_root / 'backend' / 'pipeline'
os.chdir(pipeline_dir)

print(f"Working Directory: {os.getcwd()}")
print()

# Run the pipeline
try:
    result = subprocess.run(
        [sys.executable, str(pipeline_script)],
        check=True,
        capture_output=False,
        text=True
    )
    print("\n✅ Pipeline completed successfully!")
    sys.exit(0)
except subprocess.CalledProcessError as e:
    print(f"\n❌ Pipeline failed with exit code {e.returncode}")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error running pipeline: {e}")
    sys.exit(1)
