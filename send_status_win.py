import sys, time, psutil, serial

# Ajusta para a tua porta COM
PORT = "COM6"
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1)
print(f"[OK] Connected to {PORT} @ {BAUD}")

def get_time_cpu_ram():
    now = time.strftime("%H:%M")
    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory().percent
    return f"{now},{cpu:.1f},{ram:.1f}\n"

try:
    while True:
        line = get_time_cpu_ram()
        ser.write(line.encode())
        # print(line.strip())  # descomenta para debug
        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nStopped by user")

finally:
    ser.close()
    print("Serial closed")
