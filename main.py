from fastapi import FastAPI, HTTPException
import subprocess
import json
import sys
import os

app = FastAPI()

# ဆာဗာ စတင်ချိန်တွင် yt-dlp နှင့် Deno (JS Runtime) ကို အလိုအလျောက် တပ်ဆင်ရန်
try:
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"], capture_output=True, text=True, timeout=20)
    # Render ပေါ်တွင် Deno မရှိပါက အလိုအလျောက် Download လုပ်ပြီး Install လုပ်ပေးရန် (JS Runtime Error ဖြေရှင်းရန်)
    subprocess.run("curl -fsSL https://deno.land/install.sh | sh", shell=True, capture_output=True, text=True, timeout=30)
except Exception as e:
    print(f"Setup warning: {e}")

@app.get("/")
def home():
    return {"message": "Render YT-DLP API with Deno & Cookie Support is running!"}

@app.get("/get-link")
def get_video_link(url: str):
    try:
        # Deno path ကို Environment ထဲသို့ ထည့်ပေးခြင်း
        deno_path = os.path.expanduser("~/.deno/bin/deno")
        
        cmd = [
            "yt-dlp", 
            "-j", 
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            url
        ]
        
        # Deno ရှိပါက command ထဲသို့ ထည့်ပေးရန်
        if os.path.exists(deno_path):
            cmd.extend(["--js-runtimes", deno_path])

        # Cookie ဖိုင် ရှိမရှိ စစ်ဆေးပြီး ထည့်သုံးရန်
        cookie_path = os.path.join(os.getcwd(), "cookies.txt")
        auto_cookie_path = os.path.join(os.getcwd(), "autocookies.txt")
        
        if os.path.exists(cookie_path):
            cmd.extend(["--cookies", cookie_path])
        elif os.path.exists(auto_cookie_path):
            cmd.extend(["--cookies", auto_cookie_path])
        
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
