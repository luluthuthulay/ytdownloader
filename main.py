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
        # YouTube ၏ Bot Detection ကို ရှောင်ရှားရန် User-Agent နှင့် json ဖြင့် info ဆွဲထုတ်ရန်
        cmd = [
            "yt-dlp", 
            "-j", 
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            raise HTTPException(status_code=400, detail=f"Failed to fetch: {result.stderr.strip()}")
        
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
