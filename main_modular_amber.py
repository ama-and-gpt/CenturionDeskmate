# main_modular_amber.py
# Dashboard receives LCD instance from main.py

def start_dashboard(lcd):
    import time, sys, select

    CRT_AMBER = 0x03F5
    BLACK = 0x0000

    H_CENTER = 40; Y_HOUR = 20
    BAR_W = 197; BAR_H = 16; BAR_X = 60; BAR_Y = 110
    LABEL_Y = BAR_Y + 1; LOAD_Y = BAR_Y + BAR_H + 6
    CPU_VAL_X = 260

    from rtc import now, set_time
    hora="--:--"; cpu=0.0; ram=0.0


    def draw_bar(x, y, value):
        v = min(max(value/100,0),1)
        width = int(BAR_W * v)
        lcd.fill_rect(x, y, BAR_W, BAR_H, BLACK)
        lcd.fill_rect(x, y, width, BAR_H, CRT_AMBER)

    while True:
             # read serial line: HH:MM,CPU,RAM
        if select.select([sys.stdin], [], [], 0)[0]:
            try:
                line = sys.stdin.readline().strip().replace("\r", "")
                parts = line.split(",")

                if len(parts) >= 3:
                    hora = parts[0]
                    cpu  = float(parts[1])
                    ram  = float(parts[2])
                    set_time(int(hora[0:2]), int(hora[3:5]))  # update RTC from USB
            except:
                pass
        else:
            hora = now()  # offline RTC fallback



        lcd.fill(BLACK)
        lcd.write_text(hora, H_CENTER, Y_HOUR, 6, CRT_AMBER)

        # CPU
        lcd.write_text("CPU", 5, LABEL_Y, 2, CRT_AMBER)
        lcd.write_text(f"{int(cpu):>3}", CPU_VAL_X, LABEL_Y, 2, CRT_AMBER)
        draw_bar(BAR_X, BAR_Y, cpu)

        load_label = "load %"
        lw = len(load_label) * 6 * 2
        lcd.write_text(load_label, BAR_X + BAR_W//2 - lw//2 + 2, LOAD_Y, 2, CRT_AMBER)

        # RAM
        yoff = 26
        lcd.fill_rect(0, LABEL_Y + 20, lcd.width, BAR_H + 16, BLACK)
        lcd.write_text("RAM", 5, LABEL_Y + yoff, 2, CRT_AMBER)
        lcd.write_text(f"{int(ram):>3}", CPU_VAL_X, LABEL_Y + yoff, 2, CRT_AMBER)
        draw_bar(BAR_X, BAR_Y + yoff, ram)
        lcd.write_text(load_label, BAR_X + BAR_W//2 - lw//2 + 2, LOAD_Y + yoff, 2, CRT_AMBER)

        lcd.show()
        time.sleep(0.03)
