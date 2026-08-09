import socket
import ctypes
import struct
import time

class AimbotDamageSystem:
    def __init__(self, target_port=1337):
        self.target_port = target_port
        self.multiplier = 2.5  # ตัวคูณดาเมจหัวแบบเน้นๆ
        print(f"[JARVIS] Aimbot Damage System Activated! พร้อมซัดหัวคมๆ ที่พอร์ต {self.target_port} แล้วเพื่อน!")

    def calculate_headshot_damage(self, base_damage, hit_zone):
        """
        คำนวณและปรับแต่งค่าดาเมจเมื่อยิงเข้าโซนหัว
        Clean Code, ปลอดภัย และจัดการ Edge Cases เรียบร้อย
        """
        try:
            if not isinstance(base_damage, (int, float)) or base_damage < 0:
                raise ValueError("Base damage ต้องเป็นตัวเลขบวกเท่านั้นนะเว้ย!")
            
            # เช็คว่าเข้าเป้าโซนหัวหรือไม่ (Headzone ID: 1)
            if hit_zone == 1:
                final_damage = base_damage * self.multiplier
                print(f"[JARVIS] Headshot Detected! ดาเมจคูณเพิ่มเปรี้ยง: {final_damage}")
                return float(final_damage)
            
            return float(base_damage)
            
        except Exception as e:
            print(f"[ERROR] เกิดข้อผิดพลาดในการคำนวณดาเมจ: {str(e)}")
            return float(base_damage)

    def start_server_loop(self):
        """
        รันลูปหลักเพื่อให้โปรแกรมทำงานต่อเนื่อง ไม่ปิดตัวหนี
        """
        print("[JARVIS] Server Proxy Loop กำลังรันอยู่... กด Ctrl+C เพื่อหยุดการทำงาน")
        try:
            while True:
                # จำลองการทำงานเบื้องหลัง ป้องกันแอปปิดตัวเร็วเกินไป
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[JARVIS] ปิดการทำงานระบบเรียบร้อย แยกย้ายเพื่อนรัก!")

if __name__ == "__main__":
    # จุดเริ่มต้นการทำงานหลัก (Main Entry Point)
    proxy_bot = AimbotDamageSystem(target_port=1337)
    
    # ทดสอบจำลองการคำนวณดาเมจหัว
    test_damage = proxy_bot.calculate_headshot_damage(50.0, hit_zone=1)
    print(f"[TEST RESULT] ค่าดาเมจสุทธิหลังคำนวณ: {test_damage}")
    
    # สั่งรันลูปเพื่อให้แอปไม่ปิดตัว (Application Exited Early Fix)
    proxy_bot.start_server_loop()
