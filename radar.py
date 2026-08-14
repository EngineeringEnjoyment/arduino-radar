import sys
import subprocess

# -------------------------------------------------------------------
# 1. AUTO-CHECK & AUTO-INSTALL MISSING LIBRARIES
# -------------------------------------------------------------------
#def install_if_missing(package_name, import_name=None):
#    if import_name is None:
#        import_name = package_name
#    try:
#        __import__(import_name)
#    except ImportError:
#        print(f"[SETUP] '{package_name}' not found. Installing now...")
#        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
#
#install_if_missing("pygame")
#install_if_missing("pyserial", "serial")

import pygame
import serial
import serial.tools.list_ports
import math

# -------------------------------------------------------------------
# 2. AUTO-DETECT ARDUINO COM PORT
# -------------------------------------------------------------------
def auto_detect_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # Search for typical Arduino/USB-Serial device signatures
        desc = port.description.lower()
        if "arduino" in desc or "ch340" in desc or "usb" in desc or "ftdi" in desc:
            print(f"[SERIAL] Auto-detected device on: {port.device}")
            return port.device
    if ports:
        print(f"[SERIAL] Defaulting to available port: {ports[0].device}")
        return ports[0].device
    return None

# -------------------------------------------------------------------
# 3. CONFIGURATION & PYGAME INITIALIZATION
# -------------------------------------------------------------------
WIDTH, HEIGHT = 1280, 720
CENTER_X, CENTER_Y = 640, 650

GREEN = (98, 245, 31)
SWEEP_GREEN = (30, 250, 60)
RED = (255, 10, 10)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Self-Healing Ultrasonic Radar Visualizer")
clock = pygame.time.Clock()

font_large = pygame.font.SysFont("ocr a extended", 26)
font_medium = pygame.font.SysFont("ocr a extended", 18)

fade_surface = pygame.Surface((WIDTH, 660))
fade_surface.set_alpha(4)
fade_surface.fill(BLACK)

# Attempt Serial Connection
com_port = auto_detect_port()
ser = None
simulation_mode = False

if com_port:
    try:
        ser = serial.Serial(com_port, 9600, timeout=0.1)
        print(f"[SERIAL] Connected to {com_port} successfully.")
    except Exception as e:
        print(f"[SERIAL WARNING] Could not open {com_port}: {e}")
        simulation_mode = True
else:
        print("[SERIAL WARNING] No Arduino found. Launching in Simulation Mode.")
        simulation_mode = True

# Global radar state
i_angle = 15
i_distance = 25
sweep_dir = 1
buffer = ""

# -------------------------------------------------------------------
# 4. DRAWING FUNCTIONS
# -------------------------------------------------------------------
def draw_radar():
    radii = [140, 280, 420, 560]
    for r in radii:
        rect = pygame.Rect(CENTER_X - r, CENTER_Y - r, 2 * r, 2 * r)
        pygame.draw.arc(screen, GREEN, rect, 0, math.pi, 2)

    for a in [0, 30, 60, 90, 120, 150, 180]:
        rad = math.radians(a)
        x = CENTER_X + int(580 * math.cos(rad))
        y = CENTER_Y - int(580 * math.sin(rad))
        pygame.draw.line(screen, GREEN, (CENTER_X, CENTER_Y), (x, y), 2)

def draw_line(angle):
    rad = math.radians(angle)
    x = CENTER_X + int(580 * math.cos(rad))
    y = CENTER_Y - int(580 * math.sin(rad))
    pygame.draw.line(screen, SWEEP_GREEN, (CENTER_X, CENTER_Y), (x, y), 5)

def draw_object(angle, distance):
    if distance < 40:
        pix_distance = distance * 14.0
        rad = math.radians(angle)
        x1 = CENTER_X + int(pix_distance * math.cos(rad))
        y1 = CENTER_Y - int(pix_distance * math.sin(rad))
        x2 = CENTER_X + int(580 * math.cos(rad))
        y2 = CENTER_Y - int(580 * math.sin(rad))
        pygame.draw.line(screen, RED, (x1, y1), (x2, y2), 6)

def draw_text(angle, distance, is_sim):
    pygame.draw.rect(screen, BLACK, (0, 660, WIDTH, 60))

    status = "Out of Range" if distance >= 40 else "In Range"
    mode_text = "[SIMULATION MODE]" if is_sim else f"[PORT: {com_port}]"

    screen.blit(font_medium.render("10cm", True, GREEN), (780, 635))
    screen.blit(font_medium.render("20cm", True, GREEN), (920, 635))
    screen.blit(font_medium.render("30cm", True, GREEN), (1060, 635))
    screen.blit(font_medium.render("40cm", True, GREEN), (1200, 635))

    screen.blit(font_large.render(f"Object: {status}", True, GREEN), (30, 675))
    screen.blit(font_large.render(f"Angle: {angle}°", True, GREEN), (480, 675))
    
    dist_str = f"Distance: {distance} cm" if distance < 40 else "Distance: --"
    screen.blit(font_large.render(dist_str, True, GREEN), (750, 675))
    
    # Mode Indicator
    screen.blit(font_medium.render(mode_text, True, (200, 200, 0) if is_sim else GREEN), (1050, 675))

# -------------------------------------------------------------------
# 5. MAIN EVENT & RENDER LOOP
# -------------------------------------------------------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # --- SERIAL DATA READ WITH FULL ERROR PROTECTION ---
    if ser and ser.is_open:
        try:
            while ser.in_waiting > 0:
                char = ser.read().decode('utf-8', errors='ignore')
                if char == '.':
                    if ',' in buffer:
                        parts = buffer.split(',')
                        i_angle = int(parts[0])
                        i_distance = int(parts[1])
                    buffer = ""
                else:
                    buffer += char
        except (ValueError, serial.SerialException):
            buffer = ""  # Discard corrupt packet and continue
        except Exception:
            # Fallback to simulation mode if device is pulled mid-run
            ser = None
            simulation_mode = True

    # --- SIMULATION FALLBACK LOGIC ---
    if simulation_mode:
        i_angle += sweep_dir
        if i_angle >= 165 or i_angle <= 15:
            sweep_dir *= -1
        # Generate simulated readings
        i_distance = 18 if 60 <= i_angle <= 100 else 50

    # --- RENDER FRAME ---
    screen.blit(fade_surface, (0, 0))
    draw_radar()
    draw_line(i_angle)
    draw_object(i_angle, i_distance)
    draw_text(i_angle, i_distance, simulation_mode)

    pygame.display.flip()
    clock.tick(30 if simulation_mode else 60)

# Clean Exit
if ser and ser.is_open:
    ser.close()
pygame.quit()
sys.exit()