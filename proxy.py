import os
import sys
from flask import Flask, jsonify, render_template_string

# --- CONFIGURATION ---
# ถ้ามีตัวแปรสภาพแวดล้อม (เช่น บน Render) ให้ใช้ค่านั้น แต่ถ้าไม่มี (รันในเครื่อง/VPS) ให้ใช้พอร์ต 5000 ตามใจชอบ
DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = int(os.environ.get('PORT', 5000))

app = Flask(__name__)

# หน้า HTML ที่ต้องการให้แสดงผลตามต้องการ (Custom Output Display)
CUSTOM_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JARVIS Custom Display Lab</title>
    <style>
        body { background-color: #0f172a; color: #38bdf8; font-family: 'Courier New', monospace; text-align: center; padding-top: 50px; }
        .container { border: 2px solid #38bdf8; display: inline-block; padding: 20px; border-radius: 10px; box-shadow: 0 0 15px rgba(56, 189, 248, 0.5); }
        h1 { margin-bottom: 10px; }
        p { color: #f43f5e; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>JARVIS System Active</h1>
        <p>Host & Port Successfully Bound!</p>
        <p>Displaying Custom Output as Requested, Boss! 🔥</p>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def display_custom_page():
    """
    แสดงผลหน้าเว็บตามที่ต้องการ พร้อมจัดการ Error ภายในตัว
    """
    try:
        return render_template_string(CUSTOM_HTML_TEMPLATE), 200
    except Exception as e:
        error_response = {
            "status": "error",
            "message": f"Failed to render display: {str(e)}"
        }
        return jsonify(error_response), 500

@app.route('/api/data', methods=['GET'])
def custom_api_endpoint():
    """
    ตัวอย่าง Endpoint สำหรับส่งข้อมูลออกเป็น JSON ตามต้องการ
    """
    try:
        data = {
            "system": "JARVIS Lab",
            "status": "Operational",
            "target_mode": "Unrestricted"
        }
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print(f"[*] Initializing Server on Host: {DEFAULT_HOST} and Port: {DEFAULT_PORT}...")
    
    # Error Handling สำหรับการเปิดใช้งาน Socket Server
    try:
        app.run(host=DEFAULT_HOST, port=DEFAULT_PORT, debug=False)
    except PermissionError:
        print("[-] Error: Permission denied! Ports below 1024 require root/administrator privileges.")
        sys.exit(1)
    except OSError as e:
        print(f"[-] Error: Port {DEFAULT_PORT} is already in use or invalid! Details: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[-] Unexpected Error occurred: {e}")
        sys.exit(1)
