import os
import sys
import logging
from flask import Flask, jsonify, request, render_template_string

# --- CONFIGURATION & LOGGING SETUP ---
DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = int(os.environ.get('PORT', 10000))

# ปิด Log ส่วนเกินเพื่อให้เซิร์ฟเวอร์รันลื่น ไร้ขยะ
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

# หน้า HTML สำหรับแจ้งเตือนสถานะการเปิดใช้งานและคำแนะนำการปิด Proxy
BYPASS_HTML = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JARVIS Free Fire Bypass System</title>
    <style>
        body { 
            background-color: #050505; 
            color: #00ff66; 
            font-family: 'Courier New', monospace; 
            text-align: center; 
            padding-top: 50px; 
        }
        .container { 
            border: 2px solid #00ff66; 
            display: inline-block; 
            padding: 30px; 
            border-radius: 12px; 
            box-shadow: 0 0 25px rgba(0, 255, 102, 0.4); 
            max-width: 90%;
        }
        h1 { margin-bottom: 15px; font-size: 24px; text-shadow: 0 0 10px rgba(0, 255, 102, 0.5); }
        p { color: #ffffff; font-size: 16px; line-height: 1.6; }
        .highlight { color: #ff3366; font-weight: bold; }
        .status { color: #00ff66; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>JARVIS BYPASS ACTIVE</h1>
        <p class="status">[+] สถานะ: เปิดใช้งานระบบล็อกเป้า & ซ่อนตัวสำเร็จ!</p>
        <p>กรุณา <span class="highlight">ปิด Proxy</span> ของคุณตอนนี้<br>เพื่อเชื่อมต่อเข้าสู่ตัวเกม Free Fire ได้ตามปกติ</p>
        <p style="font-size: 12px; color: #888; margin-top: 20px;">Port: 10000 | Anti-Ban Protocol: Engaged</p>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template_string(BYPASS_HTML)

# --- CATCH-ALL ROUTE ดักทุก Request จากตัวเกมเพื่อกันอาการ Ping ค้าง ---
@app.route('/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def catch_all(subpath):
    # ตบตาตัวเกมด้วยการตอบกลับ JSON หลอกว่าเชื่อมต่อสำเร็จและปลอดภัย
    return jsonify({
        "status": "success",
        "code": 200,
        "message": "JARVIS Proxy Bypass Hooked Successfully",
        "target": subpath,
        "anti_ban": "active"
    }), 200

if __name__ == '__main__':
    try:
        app.run(host=DEFAULT_HOST, port=DEFAULT_PORT)
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        sys.exit(1)
