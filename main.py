from fastapi import FastAPI, HTTPException
import subprocess
import json

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Render YT-DLP API is running successfully!"}

@app.get("/get-link")
def get_video_link(url: str):
    try:
        cmd = ["yt-dlp", "-j", url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            raise HTTPException(status_code=400, detail="Failed to fetch video details. Check URL.")
        
        data = json.loads(result.stdout.strip())
        
        return {
            "status": "success",
            "title": data.get("title"),
            "thumbnail": data.get("thumbnail"),
            "duration": data.get("duration"),
            "formats": data.get("formats", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
