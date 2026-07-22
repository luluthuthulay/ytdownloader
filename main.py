from fastapi import FastAPI, HTTPException
import subprocess
import json
import sys

app = FastAPI()

# ဆာဗာ စတင် Run တဲ့အခါ (သို့မဟုတ် Restart ဖြစ်တဲ့အခါ) yt-dlp ကို အလိုအလျောက် Latest Version သို့ Update လုပ်ရန်
try:
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"], capture_output=True, text=True, timeout=20)
    print("yt-dlp auto-upgrade checked/completed successfully.")
except Exception as e:
    print(f"Auto-upgrade failed: {e}")

@app.get("/")
def home():
    return {"message": "Render YT-DLP API is running with Auto-Update enabled!"}

@app.get("/get-link")
def get_video_link(url: str):
    try:
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
