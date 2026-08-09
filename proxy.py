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
            return float(base_damage) # Fallback กลับค่าเดิม ป้องกันเกมหลุด

    def inject_damage_packet(self, client_socket, base_damage, hit_zone):
        """
        แพ็กเกจส่งข้อมูลดาเมจเข้าสู่เซิร์ฟเวอร์แบบเรียลไทม์
        """
        try:
            actual_damage = self.calculate_headshot_damage(base_damage, hit_zone)
            # แปลงข้อมูลเป็นไบต์เพื่อส่งผ่าน Socket
            packet_data = struct.pack('!f', actual_damage)
            client_socket.sendall(packet_data)
        except socket.error as se:
            print(f"[SOCKET ERROR] ส่งแพ็กเกจพัง: {str(se)}")
        except Exception as e:
            print(f"[CRITICAL ERROR] ระเบิดกลางอากาศ: {str(e)}")

# ตัวอย่างการเรียกใช้งานร่วมกับ proxy หลัก
if __name__ == "__main__":
    aimbot = AimbotDamageSystem()
    # สมมติว่ายิงเข้าหัว (hit_zone = 1) ดาเมจพื้นฐาน 50
    # aimbot.calculate_headshot_damage(50, 1)
