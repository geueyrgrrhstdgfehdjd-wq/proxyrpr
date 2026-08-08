import pymem
import pymem.process
import asyncio
import aiohttp
import pygame
import sys
import ctypes

# --- CONFIGURATION ---
EMULATOR_PROCESS = "HD-Player.exe"
PLAYER_LIST_OFFSET = 0x1A2B3C40
POS_X_OFFSET = 0x10
POS_Y_OFFSET = 0x14
POS_Z_OFFSET = 0x18
MAX_PLAYERS = 50

# --- WINDOW CONFIG ---
WIDTH, HEIGHT = 800, 600

# --- ANTI-DETECTION BYPASS (Windows API) ---
def hide_window_from_capture(hwnd):
    try:
        # WDA_EXCLUDEFROMCAPTURE = 0x00000011
        ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, 0x00000011)
    except Exception as e:
        print(f"[-] Bypass Warning: {e}")

# --- NETWORK OPTIMIZATION ---
async def fetch_game_state_async():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('http://127.0.0.1:8080/ping_sync', timeout=0.1) as response:
                return await response.text()
        except Exception:
            return None

# --- MAIN ESP ENGINE ---
async def run_esp_overlay():
    print("[+] Initializing JARVIS Optimized Python ESP & Anti-Cheat Bypass...")
    
    pm = None
    while pm is None:
        try:
            pm = pymem.Pymem(EMULATOR_PROCESS)
            print(f"[+] Successfully attached to {EMULATOR_PROCESS}")
        except pymem.exception.ProcessNotFound:
            print(f"[-] Waiting for {EMULATOR_PROCESS} to start... Retrying in 2 seconds.")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"[-] Unexpected error attaching to process: {e}")
            await asyncio.sleep(2)

    try:
        game_module = pymem.process.module_from_name(pm.process_handle, EMULATOR_PROCESS).lpBaseOfDll
        print(f"[+] Module base address found: hex({game_module})")
    except Exception as e:
        print(f"[-] Failed to get module base: {e}")
        game_module = 0

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME | pygame.SRCALPHA)
    pygame.display.set_caption("JARVIS ESP Overlay")
    
    # Get HWND for Windows API Bypass
    hwnd = pygame.display.get_wm_info()["window"]
    hide_window_from_capture(hwnd)
    
    # Make window transparent / click-through (Windows specific)
    try:
        styles = ctypes.windll.user32.GetWindowLongW(hwnd, -20) # GWL_EXSTYLE
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, styles | 0x80000 | 0x20) # WS_EX_LAYERED | WS_EX_TRANSPARENT
        print("[+] Window set to transparent and click-through successfully.")
    except Exception as e:
        print(f"[-] Failed to set window styles: {e}")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)

    running = True
    while running:
        # Handle Pygame Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running =False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Fetch network state asynchronously
        network_data = await fetch_game_state_async()

        # Clear screen (Transparent background)
        screen.fill((0, 0, 0, 0))

        # Render simulated ESP boxes & text
        try:
            for i in range(10):  # Simulated 10 players for testing
                # ในการใช้งานจริงต้องอ่านค่าจากMemory ตรงนี้
                x = 100 + (i * 50)
                y = 100 + (i * 30)
                
                # Draw Box
                pygame.draw.rect(screen, (255, 0, 0), (x, y, 40, 80), 2)
                
                # Draw Text
                text_surface = font.render(f"Player_{i+1}", True, (0, 255, 0))
                screen.blit(text_surface, (x, y - 20))
        except Exception as e:
            print(f"[-] Render Error: {e}")

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0.001) # Yield control back to event loop

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        asyncio.run(run_esp_overlay())
    except KeyboardInterrupt:
        print("\n[!] Program terminated by user.")
        pygame.quit()
        sys.exit()
