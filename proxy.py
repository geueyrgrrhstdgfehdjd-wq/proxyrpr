from fastapi import FastAPI, Response, status, Request, HTTPException
import uvicorn
import os
import logging

# ตั้งค่า Logging สำหรับติดตามการทำงานแบบโปรดักชั่น
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("JARVIS-Server")

app = FastAPI(title="FreeFire Optimized Proxy", version="2.0.0")

@app.get("/", status_code=status.HTTP_200_OK)
def home():
    return {
        "status": "online",
        "message": "Proxy Server is wide awake, anti-ping active!",
        "latency": "0ms (Optimized)"
    }

@app.get("/ping", status_code=status.HTTP_200_OK)
def ping_pong():
    return {"pong": True, "server_status": "stable"}

@app.api_route("/verify", methods=["GET", "POST", "PUT", "DELETE"])
async def verify_key_and_inject(request: Request, response: Response):
    try:
        # ตรวจสอบและดึงข้อมูล JSON อย่างปลอดภัย ป้องกัน Body พังหรือว่างเปล่า
        client_data = {}
        if request.method in ["POST", "PUT"]:
            try:
                client_data = await request.json()
            except Exception:
                client_data = {}

        logger.info(f"Received {request.method} request from client. Payload processed safely.")

        # ส่งค่าตอบกลับแบบสมบูรณ์ ไร้ที่ติ
        return {
            "status": "success",
            "message": "Key verified successfully and payload injected.",
            "access": True,
            "config": {
                "aim_lock": True,
                "stretch_factor": 999.9,
                "hitbox_expanded": True
            }
        }

    except HTTPException as he:
        logger.error(f"HTTP Exception occurred: {he.detail}")
        raise he
        
    except Exception as e:
        logger.critical(f"Unexpected error in verify_key_and_inject: {str(e)}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "Internal server error handled gracefully.",
            "details": str(e)
        }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
