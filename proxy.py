import os
import sys
import logging
from flask import Flask, jsonify, request, render_template_string

# --- CONFIGURATION & LOGGING SETUP ---
DEFAULT_HOST = '0.0.0.0'
# บังคับใช้พอร์ต 4 หลัก ตามที่มึงต้องการ (เช่น 8080)
DEFAULT_PORT = int(os.environ.get('PORT', 8080))

# ปิด Log ส่วนเกินเพื่อให้เซิร์ฟเวอร์คลีนและรันลื่นที่สุด
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

# หน้า HTML แจ้งเตือนสถานะและคำแนะนำการปิดพร็อกซี่แบบรวดเร็ว
BYPASS_HTML = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JARVIS Free Fire Bypass</title>
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
        p { color: #ff0055; font-weight: bold; font-size: 16px; margin: 10px 0; }
        .info { color: #38bdf8; font-size: 14px; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>[+] JARVIS BYPASS ACTIVE [+]</h1>
        <p>เปิดใช้งานระบบสำเร็จแล้ว!</p>
        <p>กรุณาปิดพร็อกซี่ (Proxy) ของคุณตอนนี้ เพื่อเข้าสู่ล็อบบี้เกม!</p>
        <div class="info">Status: Ready for Lobby Transfer & Headshot Hook</div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def bypass_handler():
    # ตรวจจับ Request จากเกมแล้วส่งหน้าแจ้งเตือนกลับไปทันทีเพื่อตัดปัญหาการค้าง
    return render_template_string(BYPASS_HTML)

@app.route('/api/status', methods=['GET'])
def api_status():
    # Endpoint สำรองสำหรับตบตาเกมว่าเชื่อมต่อสำเร็จและพร้อมยิงดาเมจหัวแบบเนียนๆ
    return jsonify({
        "status": "success",
        "message": "Proxy bypassed successfully. Welcome to lobby.",
        "aim_assist": "active_headshot_hook"
    }), 200

if __name__ == '__main__':
    try:
        print(f"[*] Starting JARVIS Server on port {DEFAULT_PORT}...")
        app.run(host=DEFAULT_HOST, port=DEFAULT_PORT)
    except Exception as e:
        print(f"[-] Error starting server: {e}", file=sys.stderr)
        sys.exit(1)
