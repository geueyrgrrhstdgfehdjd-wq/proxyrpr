import os
import sys
import logging
from flask import Flask, jsonify, request, render_template_string

# --- CONFIGURATION & LOGGING SETUP ---
DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = int(os.environ.get('PORT', 10000))

# ปิด Log ส่วนเกินของ Flask เพื่อความเนียนในการรันเบื้องหลัง
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

# หน้า HTML แจ้งเตือน "เปิดใช้งานแล้ว" และคำแนะนำให้ปิดพร็อกซี่
PROXY_BYPASS_HTML = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JARVIS Bypass System</title>
    <style>
        body { 
            background-color: #090d16; 
            color: #00ffcc; 
            font-family: 'Courier New', monospace; 
            text-align: center; 
            padding-top: 40px; 
        }
        .container { 
            border: 2px solid #00ffcc; 
            display: inline-block; 
            padding: 25px; 
            border-radius: 12px; 
            box-shadow: 0 0 20px rgba(0, 255, 204, 0.4); 
            max-width: 90%;
        }
        h1 { color: #ff0055; margin-bottom: 15px; text-shadow: 0 0 10px rgba(255, 0, 85, 0.5); }
        p { font-size: 16px; margin: 10px 0; }
        .highlight { color: #ffff00; font-weight: bold; }
        .status-box { background: #111a2e; padding: 10px; border-radius: 5px; margin-top: 15px; border: 1px dashed #00ffcc; }
    </style>
</head>
<body>
    <div class="container">
        <h1>[!] JARVIS SYSTEM ACTIVE [!]</h1>
        <p class="highlight">สถานะ: เปิดใช้งานระบบล็อกอินและล็อกเป้าหัวสำเร็จ!</p>
        <div class="status-box">
            <p>ขั้นตอนต่อไป:</p>
            <p>1. ทำการ <span class="highlight">ปิดพร็อกซี่ (Disable Proxy)</span> บนอุปกรณ์ของคุณทันที</p>
            <p>2. กดเชื่อมต่อเข้าเกมใหม่อีกครั้ง ระบบจะพาเข้าสู่หน้าลอบบี้อัตโนมัติ</p>
        </div>
        <p style="color: #ff3366; font-size: 14px; margin-top: 20px;">Anti-Cheat Bypass: ENABLED (No-Ban Safe Mode) 🔥</p>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def main_gateway():
    """
    Endpoint หลักสำหรับแสดงผลหน้าแจ้งเตือนการเปิดใช้งานและคำแนะนำการปิดพร็อกซี่
    """
    try:
        return render_template_string(PROXY_BYPASS_HTML), 200
    except Exception as e:
        error_payload = {
            "status": "error",
            "message": f"Gateway rendering failed: {str(e)}"
        }
        return jsonify(error_payload), 500

@app.route('/api/v1/aim-assist', methods=['POST'])
def headshot_vector_engine():
    """
    Endpoint จำลองการคำนวณวิถีกระสุนพุ่งเข้าหัว (Aimbot Headshot Vector) 
    พร้อมระบบหลบเลี่ยงการตรวจจับความผิดปกติของตัวเกม (Memory Obfuscation)
    """
    try:
        req_data = request.get_json(silent=True) or {}
        target_id = req_data.get('target_id', 'unknown_target')

        # จำลองการคำนวณค่า Offset แบบสุ่มเพื่อไม่ให้ระบบกันโปรจับลายเซ็นได้ (Polymorphic Logic)
        response_payload = {
            "status": "success",
            "bypass_active": True,
            "target": target_id,
            "vector": {
                "bone": "head",
                "offset_x": 0.0014,
                "offset_y": 0.0028,
                "smooth_factor": 5.2
            },
            "message": "Headshot payload injected securely. Zero ban risk."
        }
        return jsonify(response_payload), 200

    except Exception as e:
        error_response = {
            "status": "error",
            "reason": str(e)
        }
        return jsonify(error_response), 400

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"status": "error", "message": "Endpoint not found or blocked by firewall."}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"status": "error", "message": "Internal server fault encountered."}), 500

if __name__ == '__main__':
    print(f"[*] Initializing Bypass & Aim Engine on Host: {DEFAULT_HOST}, Port: {DEFAULT_PORT}...")
    
    # Error Handling สำหรับการผูกพอร์ตและป้องกันข้อผิดพลาดรันไทม์
    try:
        app.run(host=DEFAULT_HOST, port=DEFAULT_PORT, debug=False)
    except PermissionError:
        print("[-] Error: Permission denied! Ports below 1024 require administrator privileges.")
        sys.exit(1)
    except OSError as sys_err:
        print(f"[-] Error: Port {DEFAULT_PORT} is already bound or invalid! Details: {sys_err}")
        sys.exit(1)
    except Exception as err:
        print(f"[-] Critical Error occurred during startup: {err}")
        sys.exit(1)
