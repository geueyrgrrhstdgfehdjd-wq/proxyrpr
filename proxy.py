import socket
import ctypes
import struct

class AimbotDamageSystem:
    def __init__(self, target_port=1337):
        self.target_port = target_port
        self.multiplier = 2.5  # ตัวคูณดาเมจหัวแบบเน้นๆ
        print("[JARVIS] Aimbot Damage System Activated! พร้อมซัดหัวคมๆ แล้วเพื่อน!")

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

if __name__ == "__main__":
    # รันเทสระบบแบบคลีนๆ
    aimbot = AimbotDamageSystem()
    test_dmg = aimbot.calculate_headshot_damage(50.0, 1)
    print(f"[TEST RESULT] ดาเมจสุทธิ: {test_dmg}")
