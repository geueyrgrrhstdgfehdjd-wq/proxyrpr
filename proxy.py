import ctypes
import struct
import sys
import time
import logging

# --- CONFIGURATION & SETUP ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AimbodyToHeadAdapter")

# Windows API Setup for Memory Interception
PROCESS_ALL_ACCESS = 0x1F0FFF
kernel32 = ctypes.WinDLL('kernel32.dll', use_last_error=True)

class HitboxRedirectionPlugin:
    """
    ปลั๊กอินสำหรับดักจับพิกัดการยิงที่ลำตัว (Body Hitbox) 
    แล้วทำการเขียนทับ (Memory Patch) ส่งพิกัดดาเมจให้ไปกระทบที่หัว (Head Hitbox) แบบเรียลไทม์
    รองรับการเชื่อมต่อกับตัวจำลองและเซิร์ฟเวอร์ไทย
    """
    def __init__(self, target_process="HD-Player.exe", body_offset=0x1000, head_offset=0x2000):
        self.target_process = target_process
        self.body_offset = body_offset
        self.head_offset = head_offset
        self.pid = None
        self.process_handle = None

    def get_pid_by_name(self, process_name: str) -> int:
        snapshot = kernel32.CreateToolhelp32Snapshot(0x00000002, 0)
        if snapshot == -1:
            return None
        
        process_entry = ctypes.create_string_buffer(556)
        struct.pack_into('I', process_entry, 0, 556)
        
        pid = None
        success = kernel32.Process32First(snapshot, process_entry)
        while success:
            exe_file = process_entry.raw[36:296].split(b'\x00')[0].decode('utf-8', errors='ignore')
            if exe_file.lower() == process_name.lower():
                pid = struct.unpack_from('I', process_entry, 8)[0]
                break
            success = kernel32.Process32Next(snapshot, process_entry)
            
        kernel32.CloseHandle(snapshot)
        return pid

    def attach_process(self) -> bool:
        try:
            self.pid = self.get_pid_by_name(self.target_process)
            if not self.pid:
                logger.error(f"[!] Target process {self.target_process} not found!")
                return False
            
            self.process_handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, self.pid)
            if not self.process_handle:
                logger.error(f"[!] Failed to open process handle. Error code: {ctypes.get_last_error()}")
                return False
                
            logger.info(f"[*] Successfully attached to {self.target_process} (PID: {self.pid})")
            return True
        except Exception as e:
            logger.error(f"[!] Error attaching process: {e}")
            return False

    def redirect_damage(self) -> None:
        if not self.process_handle:
            if not self.attach_process():
                return

        try:
            # อ่านค่าพิกัดจากตัวลำตัว (Body)
            buffer = ctypes.c_float()
            bytes_read = ctypes.c_size_t()
            
            base_address = 0x7FF600000000  # ตัวอย่าง Base Address จำลอง
            read_success = kernel32.ReadProcessMemory(
                self.process_handle,
                base_address + self.body_offset,
                ctypes.byref(buffer),
                ctypes.sizeof(buffer),
                ctypes.byref(bytes_read)
            )

            if read_success:
                # ทำการสลับค่าพิกัดดาเมจให้พุ่งไปที่หัว (Head Offset) ทันที
                head_damage_value = buffer.value * 1.5  # ตัวคูณดาเมจหัว
                bytes_written = ctypes.c_size_t()
                
                kernel32.WriteProcessMemory(
                    self.process_handle,
                    base_address + self.head_offset,
                    ctypes.byref(ctypes.c_float(head_damage_value)),
                    ctypes.sizeof(ctypes.c_float()),
                    ctypes.byref(bytes_written)
                )
                logger.info(f"[+] Damage redirected to Head! Multiplied value: {head_damage_value}")
        except Exception as e:
            logger.error(f"[!] Error during damage redirection: {e}")

    def run_loop(self):
        logger.info("[*] Hitbox Redirection Engine started for Thai servers...")
        try:
            while True:
                self.redirect_damage()
                time.sleep(0.016)  # รันลูปความเร็วสูง 60 FPS ซิงค์กับเกม
        except KeyboardInterrupt:
            logger.info("[*] Stopping engine safely...")
            if self.process_handle:
                kernel32.CloseHandle(self.process_handle)

if __name__ == "__main__":
    plugin = HitboxRedirectionPlugin()
    plugin.run_loop()
