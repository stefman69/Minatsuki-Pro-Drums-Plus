import Gamepad
import HIDInput
import time

KICK_BYTE_INDEX = 6
KICK_ACTIVE_VALUE = 1

DPAD_BYTE_INDEX = 5
ANALOG_BYTE_INDEX = 6

BTYE_INDEX_RED_DRUM = 43
BTYE_INDEX_YELLOW_DRUM = 45
BTYE_INDEX_BLUE_DRUM = 44
BTYE_INDEX_GREEN_DRUM = 46

BTYE_INDEX_GREEN_CYMBAL = 49
BTYE_INDEX_BLUE_CYMBAL = 48
BTYE_INDEX_YELLOW_CYMBAL = 47

mapping = {
    BTYE_INDEX_GREEN_CYMBAL:  [Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB],
    BTYE_INDEX_BLUE_CYMBAL:   [Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB],
    BTYE_INDEX_YELLOW_CYMBAL: [Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_BACK],
    BTYE_INDEX_RED_DRUM:      [Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_B],
    BTYE_INDEX_YELLOW_DRUM:   [Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y],
    BTYE_INDEX_BLUE_DRUM:     [Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_X],
    BTYE_INDEX_GREEN_DRUM:    [Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_A]
}

pad_check_indices = list(mapping.keys())

pressed_buttons = set()
music_pressed = set()
dpad_buttons = set()
prev_kick_state = 0
prev_analog_val = 0

def handle_music_inputs(data):
    global prev_kick_state, music_pressed

    new_music_pressed = set()

    # Handle kick pedals
    kick_val = data[KICK_BYTE_INDEX]
    if kick_val == 1:
        new_music_pressed.add(Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    elif kick_val == 2:
        new_music_pressed.add(Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    elif kick_val == 3:
        new_music_pressed.add(Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        new_music_pressed.add(Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)

    # Handle drums and cymbals
    for byte_offset, buttons in mapping.items():
        if byte_offset >= len(data):
            continue
        if data[byte_offset] > 0:
            new_music_pressed.update(buttons)

    # Immediate press/release for music buttons
    for btn in music_pressed - new_music_pressed:
        Gamepad.ReleaseButton(btn)
    for btn in new_music_pressed - music_pressed:
        Gamepad.PressButton(btn)

    music_pressed = new_music_pressed

def handle_dpad_and_face_buttons(data, current_pressed):
    global dpad_buttons

    any_music_input = any(data[i] > 0 for i in pad_check_indices) or data[KICK_BYTE_INDEX] in (1, 2, 3)

    face_button_map = {
        136: Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y,
        72:  Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_B,
        40:  Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_A,
        24:  Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_X,
    }

    analog_val = data[DPAD_BYTE_INDEX]

    if not any_music_input and analog_val in face_button_map:
        current_pressed.add(face_button_map[analog_val])
        for btn in dpad_buttons:
            Gamepad.ReleaseButton(btn)
        dpad_buttons.clear()
    elif not any_music_input:
        dpad_val = analog_val & 0x0F
        new_dpad = set()

        if dpad_val == 0:
            new_dpad.add(Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        elif dpad_val == 1:
            new_dpad.update([Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP, Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT])
        elif dpad_val == 2:
            new_dpad.add(Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
        elif dpad_val == 3:
            new_dpad.update([Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN, Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT])
        elif dpad_val == 4:
            new_dpad.add(Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
        elif dpad_val == 5:
            new_dpad.update([Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN, Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT])
        elif dpad_val == 6:
            new_dpad.add(Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
        elif dpad_val == 7:
            new_dpad.update([Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP, Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT])

        for btn in dpad_buttons - new_dpad:
            Gamepad.ReleaseButton(btn)
        for btn in new_dpad - dpad_buttons:
            Gamepad.PressButton(btn)

        dpad_buttons = new_dpad
    else:
        for btn in dpad_buttons:
            Gamepad.ReleaseButton(btn)
        dpad_buttons.clear()

def handle_control_buttons(data, current_pressed):
    byte6 = data[ANALOG_BYTE_INDEX]
    if (byte6 & 0x20) != 0:
        current_pressed.add(Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_START)

def sample_handler(data):
    global pressed_buttons

    current_pressed = set()

    handle_music_inputs(data)
    handle_dpad_and_face_buttons(data, current_pressed)
    handle_control_buttons(data, current_pressed)

    for btn in pressed_buttons - current_pressed:
        if btn not in dpad_buttons and btn not in music_pressed:
            Gamepad.ReleaseButton(btn)

    for btn in current_pressed - pressed_buttons:
        Gamepad.PressButton(btn)

    pressed_buttons = current_pressed.copy()
    Gamepad.Update()

if __name__ == '__main__':
    import sys
    if sys.version_info >= (3,):
        unicode = str
        raw_input = input
    else:
        import codecs
        sys.stdout = codecs.getwriter('mbcs')(sys.stdout)

    device = HIDInput.Choose_HID_Device()

    if device:
        print(f"Using device: {device.vendor_name} {device.product_name}")
        HIDInput.Device_Loop(device, sample_handler)
    else:
        print("No HID device selected.")
