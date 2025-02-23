import os
import uuid
import subprocess
import shutil
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()
BASE_DIR = Path(__file__).parent.resolve()
MEDIA_DIR = BASE_DIR / "media"
STATIC_DIR = BASE_DIR / "static"

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories
MEDIA_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

def cleanup_temp_files(temp_script: Path, output_dir: Path):
    """Clean up temporary files after rendering"""
    if temp_script.exists():
        temp_script.unlink()
    if output_dir.exists():
        shutil.rmtree(output_dir)

async def render_manim(script: str, render_id: str):
    """Execute manim render command"""
    temp_script = MEDIA_DIR / f"temp_{render_id}.py"
    output_dir = MEDIA_DIR / "videos"
    
    try:
        # Save temporary script
        with open(temp_script, "w") as f:
            f.write(script)
        
        # Run manim command
        cmd = [
            "manim",
            "-ql",
            "--progress_bar", "none",
            "--media_dir", str(MEDIA_DIR),
            str(temp_script),
            "MainScene"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)

        # Find generated video
        video_path = output_dir / f"temp_{render_id}" / "480p15" / "MainScene.mp4"
        if not video_path.exists():
            raise HTTPException(status_code=500, detail="Output video not found")

        # Move to static directory
        final_path = STATIC_DIR / f"output_{render_id}.mp4"
        shutil.move(str(video_path), str(final_path))
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cleanup_temp_files(temp_script, output_dir / f"temp_{render_id}")

@app.post("/api/render")
async def render_animation(background_tasks: BackgroundTasks, script: str):
    render_id = str(uuid.uuid4())
    background_tasks.add_task(render_manim, script, render_id)
    return {"render_id": render_id}

@app.get("/api/status/{render_id}")
async def check_status(render_id: str):
    video_path = STATIC_DIR / f"output_{render_id}.mp4"
    if video_path.exists():
        return {"status": "complete", "url": f"/static/output_{render_id}.mp4"}
    return {"status": "processing"}