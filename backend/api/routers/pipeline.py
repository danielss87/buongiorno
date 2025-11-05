"""
Buongiorno API - Pipeline Router
Endpoint to trigger pipeline execution manually or via webhook
"""

from fastapi import APIRouter, HTTPException, Header
import subprocess
import sys
import os
from pathlib import Path

router = APIRouter()

# Optional: Set a secret token for security
PIPELINE_SECRET = os.getenv("PIPELINE_SECRET", "")


@router.post("/pipeline/run")
async def trigger_pipeline(authorization: str = Header(None)):
    """
    Trigger the prediction pipeline manually

    Optional: Add Authorization header with secret token for security
    Example: Authorization: Bearer your-secret-token
    """

    # If secret is configured, validate it
    if PIPELINE_SECRET:
        if not authorization or authorization != f"Bearer {PIPELINE_SECRET}":
            raise HTTPException(status_code=401, detail="Invalid or missing authorization")

    try:
        # Get project root
        api_dir = Path(__file__).parent.parent
        project_root = api_dir.parent.parent
        pipeline_script = project_root / 'run_pipeline_prod.py'

        # Run pipeline in background (non-blocking)
        process = subprocess.Popen(
            [sys.executable, str(pipeline_script)],
            cwd=str(project_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        return {
            "status": "started",
            "message": "Pipeline execution started in background",
            "pid": process.pid
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start pipeline: {str(e)}")


@router.get("/pipeline/status")
async def pipeline_status():
    """
    Check if pipeline data exists and when it was last updated
    """
    try:
        api_dir = Path(__file__).parent.parent
        project_root = api_dir.parent.parent
        predictions_file = project_root / 'backend' / 'pipeline' / 'data' / 'predictions' / 'predictions_history.csv'

        if predictions_file.exists():
            from datetime import datetime
            modified_time = datetime.fromtimestamp(predictions_file.stat().st_mtime)

            return {
                "status": "available",
                "last_updated": modified_time.isoformat(),
                "file_exists": True
            }
        else:
            return {
                "status": "no_data",
                "message": "No predictions available yet. Run the pipeline first.",
                "file_exists": False
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking pipeline status: {str(e)}")
