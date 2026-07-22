from fastapi import FastAPI, HTTPException
import subprocess
import json
import sys
import os

app = FastAPI()

# ဆာဗာ စတင် Run တဲ့အခါ yt-dlp ကို အလိုအလျောက် Latest Version သို့ Update လုပ်ရန်
try:
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"], capture_output=True, text=True, timeout=20)
    print("yt-dlp auto-upgrade checked/completed successfully.")
except Exception as e:
    print(f"Auto-upgrade failed: {e}")

@app.get("/")
def home():
    return {"message": "Render YT-DLP API with Bot Bypass & Cookie Support is running successfully!"}

@app.get("/get-link")
def get_video_link(url: str):
    try:
        # yt-dlp command တည်ဆောက်ခြင်း (Bot Detection ကျော်လွှားရန် User-Agent ထည့်သွင်းထားသည်)
        cmd = [
            "yt-dlp", 
            "-j", 
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            url
        ]
        
        # GitHub Repository ထဲတွင် cookies.txt သို့မဟုတ် autocookies.txt ရှိမရှိ စစ်ဆေးပြီး Bot Bypass အတွက် ထည့်သုံးရန်
        cookie_path = os.path.join(os.getcwd(), "cookies.txt")
        auto_cookie_path = os.path.join(os.getcwd(), "autocookies.txt")
        
        if os.path.exists(cookie_path):
            cmd.extend(["--cookies", cookie_path])
        elif os.path.exists(auto_cookie_path):
            cmd.extend(["--cookies", auto_cookie_path])
        
        # yt-dlp ဖြင့် အချက်အလက်များ လှမ်းထုတ်ခြင်း
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
