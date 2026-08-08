import os
import sys
import logging
from flask import Flask, jsonify, request, render_template_string

# --- CONFIGURATION & LOGGING SETUP ---
DEFAULT_HOST = '0.0.0.0'
# ล็อกพอร์ตไว้ที่ 10000 ตามที่มึงต้องการ
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
        p { color: #ff3366; font-size: 16px; font-weight: bold; margin: 10px 0; }
        .info { color: #33ccff; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>JARVIS SYSTEM ACTIVE</h1>
        <p>[!] เปิดใช้งานฟังก์ชันสำเร็จแล้ว!</p>
        <p class="info">&gt;&gt; กรุณาปิด Proxy ในระบบของคุณ &lt;&lt;</p>
        <p class="info">จากนั้นเข้าเกมตามปกติเพื่อเข้าสู่หน้าลอบบี้</p>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    # ส่งหน้า HTML แจ้งเตือนสถานะกลับไปให้ไคลเอนต์
    return render_template_string(BYPASS_HTML)

@app.route('/api/bypass', methods=['POST', 'GET'])
def bypass_handler():
    # ฟังก์ชันจำลองการตอบกลับเพื่อตบตา Anti-Cheat และปลดล็อกการเข้าลอบบี้
    try:
        payload = {
            "status": "success",
            "code": 200,
            "message": "Bypass active, proxy disabled requirement met. Lobby access granted.",
            "aim_hook": "enabled_safe_mode"
        }
        return jsonify(payload), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    # ป้องกัน Error 404 ให้รีเทิร์นค่าสถานะปกติกลับไปแทนเพื่อให้เกมไม่หลุด
    return jsonify({
        "status": "active",
        "bypass": "true",
        "note": "Proxy disabled, entering lobby..."
    }), 200

if __name__ == '__main__':
    try:
        print(f"[*] Starting JARVIS Server on {DEFAULT_HOST}:{DEFAULT_PORT}...")
        app.run(host=DEFAULT_HOST, port=DEFAULT_PORT)
    except Exception as e:
        print(f"[!] Error starting server: {e}", file=sys.stderr)
        sys.exit(1)
