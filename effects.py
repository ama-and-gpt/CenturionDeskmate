from machine import Pin, PWM
import time, math

# LCD backlight pin
bl = PWM(Pin(21))
bl.freq(1000)

# breathing bounds
min_bl = 24000
max_bl = 52000

def lcd_backlight_set(val):
    bl.duty_u16(int(val))

def backlight_breath(t_ms=None):
    """smooth breathing curve"""
    if t_ms is None:
        t_ms = time.ticks_ms()

    t = t_ms / 1000
    # nice slow breathe, CRT glow curve
    val = (math.sin(t * 0.45) + 1) / 2
    level = int(min_bl + val * (max_bl - min_bl))
    lcd_backlight_set(level)

# CRT effects
def draw_scanlines(lcd):
    for y in range(0, lcd.height, 2):
        lcd.hline(0, y, lcd.width, 0x0000)

def ghost_fade(lcd, decay=4):
    for y in range(0, lcd.height):
        if y % decay == 0:
            lcd.hline(0, y, lcd.width, 0x0000)
