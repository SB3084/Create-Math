import os
import uuid
import subprocess
import shutil
from pathlib import Path
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Configuration
BASE_DIR = Path(__file__).parent
MEDIA_DIR = BASE_DIR / "media"
STATIC_DIR = BASE_DIR / "static"
os.makedirs(MEDIA_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

def cleanup_files(render_id: str):
    temp_script = MEDIA_DIR / f"temp_{render_id}.py"
    output_dir = MEDIA_DIR / "videos" / f"temp_{render_id}"
    if temp_script.exists():
        temp_script.unlink()
    if output_dir.exists():
        shutil.rmtree(output_dir)

async def render_task(script: str, render_id: str):
    try:
        # Save temporary script
        script_path = MEDIA_DIR / f"temp_{render_id}.py"
        with open(script_path, "w") as f:
            f.write(script)
        
        # Execute manim
        cmd = [
            "manim", "-ql",
            "--media_dir", str(MEDIA_DIR),
            "--progress_bar", "none",
            str(script_path),
            "MainScene"
        ]
        
        process = await asyncio.create_subprocess_exec( # type: ignore
            *cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            raise Exception(stderr.decode())
        
        # Move output file
        video_path = MEDIA_DIR / "videos" / f"temp_{render_id}" / "480p15" / "MainScene.mp4"
        final_path = STATIC_DIR / f"{render_id}.mp4"
        shutil.move(video_path, final_path)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cleanup_files(render_id)

@app.post("/api/render")
async def create_render(background_tasks: BackgroundTasks, script: str):
    render_id = str(uuid.uuid4())
    background_tasks.add_task(render_task, script, render_id)
    return {"render_id": render_id}

@app.get("/api/status/{render_id}")
async def get_status(render_id: str):
    if (STATIC_DIR / f"{render_id}.mp4").exists():
        return {"status": "complete", "url": f"/static/{render_id}.mp4"}
    return {"status": "processing"}
