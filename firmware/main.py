import board
import busio
import displayio
import terminalio
from adafruit_display_text import label

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import MatrixScanner
from kmk.scanners import DiodeOrientation
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.modules.macros import Macros, Press, Release, Tap
from kmk.extensions.rgb import RGB
from kmk.extensions.OLED import OLED
from kmk.extensions.OLED.renderer import draw_text

keyboard = KMKKeyboard()

animation_modes = ["rainbow", "swirl", "breathing", "cycle", "solid"]
current_mode_index = 0

keyboard.matrix = MatrixScanner(
    column_pins=(board.A0, board.A1, board.A2),  
    row_pins=(board.GP0, board.GP2, board.GP1), 
    diode_orientation=DiodeOrientation.COL2ROW
)

encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)
encoder_handler.pins = ((board.GP3, board.GP4),)
encoder_handler.map = [((KC.VOLD, KC.VOLU),)] # vol down, vol up

macros = Macros()
keyboard.modules.append(macros)

emoji_macro = macros.macro(
    name='EMOJI',
    sequence=[KC.LGUI(KC.DOT)]  # Windows + .
)

def switch_rgb_mode():
    global current_mode_index
    current_mode_index = (current_mode_index + 1) % len(animation_modes)
    rgb_ext.animation_mode = animation_modes[current_mode_index]
    print(f"Switched to RGB mode: {rgb_ext.animation_mode}")
    oled_ext.renderer = draw_text("Mode: " + rgb_ext.animation_mode)

switch_rgb_macro = Macro(
    name='SWITCH_RGB',
    on_press=[switch_rgb_mode]
)

rgb_ext = RGB(
    pixel_pin=board.A3, 
    num_pixels=9,
    hue_default=0,
    sat_default=255,
    val_default=50,
    animation_speed=2,
    animation_mode = "rainbow"
)
keyboard.extensions.append(rgb_ext)

oled_ext = OLED(
    i2c=board.I2C(), 
    width=128,
    height=32,
    renderers=[draw_text(":)")]
)
keyboard.extensions.append(oled_ext)

# --- Keymap Layout ---
keyboard.keymap = [
    [KC.NO, KC.MUTE, KC.MB_TOGGLE],       # Row 1: (rotary enc), mute, cam toggle
    [KC.MPRV, KC.MPLY, KC.MNXT],          # Row 2: prev, play/pause, next
    [KC.PSCREEN, switch_rgb_macro, emoji_macro],    # Row 3: screenshot, RGB, emoji
]

def sparkle_display():
    splash = displayio.Group()
    sparkle = label.Label(terminalio.FONT, text="✨😊✨", color=0xFFFFFF, x=30, y=15)
    splash.append(sparkle)
    oled_ext.display.show(splash)

if __name__ == '__main__':
    keyboard.go()