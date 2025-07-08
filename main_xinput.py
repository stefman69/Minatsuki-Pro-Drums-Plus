import Gamepad
import HIDInput

BTYE_INDEX_RED_DRUM = 43
BTYE_INDEX_YELLOW_DRUM = 45
BTYE_INDEX_BLUE_DRUM = 44
BTYE_INDEX_GREEN_DRUM = 46

BTYE_INDEX_GREEN_CYMBAL = 49
BTYE_INDEX_BLUE_CYMBAL = 48
BTYE_INDEX_YELLOW_CYMBAL = 47

BTYE_INDEX_ANALOG = 6
BTYE_INDEX_DPAD = 5
BTYE_INDEX_GUIDE = 7

VALUE_SHARE = 16
VALUE_OPTIONS = 32
VALUE_TRIANGLE = 136
VALUE_CIRCLE = 72
VALUE_CROSS = 40
VALUE_SQUARE = 24

music_mapping = {
    BTYE_INDEX_GREEN_CYMBAL: [Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_A, Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB],
    BTYE_INDEX_BLUE_CYMBAL:  [Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_X, Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB],
    BTYE_INDEX_YELLOW_CYMBAL:[Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y, Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB],
    BTYE_INDEX_RED_DRUM:     [Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_B],
    BTYE_INDEX_YELLOW_DRUM:  [Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y],
    BTYE_INDEX_BLUE_DRUM:    [Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_X],
    BTYE_INDEX_GREEN_DRUM:   [Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_A]
}

prev_pedal_val = 0
prev_data = None
prev_analog_value = None
music_keys_list = list(music_mapping)
music_isHit_list = [0] * len(music_keys_list)
face_button_pressed = set()

dPadCheckList = list(music_mapping.keys())

analog_mapping = {
    VALUE_OPTIONS: Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_START,
    VALUE_SHARE:   Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
    VALUE_TRIANGLE: Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
    VALUE_CIRCLE:   Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
    VALUE_CROSS:    Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
    VALUE_SQUARE:   Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
}

pressed_buttons = set()
dpad_buttons = set()

face_button_press_map = {
    VALUE_TRIANGLE: Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y,
    VALUE_CIRCLE:   Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_B,
    VALUE_CROSS:    Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_A,
    VALUE_SQUARE:   Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_X,
}

def handle_music_inputs(data, current_pressed):
    pedal_val = data[6]

    if pedal_val == 1:
        current_pressed.add(Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    elif pedal_val == 2:
        current_pressed.add(Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    elif pedal_val == 3:
        current_pressed.add(Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        current_pressed.add(Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)

    for index, byte_offset in enumerate(music_mapping):
        if byte_offset >= len(data):
            continue

        detection = data[byte_offset]
        button = music_mapping[byte_offset]

        if detection > 0 and music_isHit_list[index] != detection:
            Gamepad.PressButtonOnce(button)
            music_isHit_list[index] = detection
        elif detection == 0:
            music_isHit_list[index] = 0

def handle_control_inputs(data, current_pressed):
    analog_val = data[BTYE_INDEX_ANALOG]
    guide_val = data[BTYE_INDEX_GUIDE]

    if analog_val & VALUE_OPTIONS:
        current_pressed.add(Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_START)
    if analog_val & VALUE_SHARE:
        current_pressed.add(Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_BACK)

    if guide_val & 0x01:
        current_pressed.add(Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE)

    if analog_val in face_button_press_map:
        Gamepad.PressButtonOnce(face_button_press_map[analog_val])

def handle_dpad(data):
    global dpad_buttons

    analog_val = data[BTYE_INDEX_DPAD]
    summed = sum(data[i] for i in dPadCheckList)
    if summed > 0:
        for btn in dpad_buttons:
            Gamepad.ReleaseButton(btn)
        dpad_buttons.clear()
        return

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

def handle_face_buttons(data):
    analog_val = data[BTYE_INDEX_ANALOG]

    face_map = {
        VALUE_TRIANGLE: Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y,
        VALUE_CIRCLE:   Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_B,
        VALUE_CROSS:    Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_A,
        VALUE_SQUARE:   Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_X,
    }

    prev_analog_val = analog_val

    any_music_active = any(data[i] > 0 for i in music_mapping.keys())
    if any_music_active:
        for btn in list(face_button_pressed):
            Gamepad.ReleaseButton(btn)
        face_button_pressed.clear()
        return

    if analog_val in face_map:
        btn = face_map[analog_val]
        if btn not in face_button_pressed:
            Gamepad.PressButton(btn)
            face_button_pressed.add(btn)
    else:
        for btn in list(face_button_pressed):
            Gamepad.ReleaseButton(btn)
        face_button_pressed.clear()

def handle_dpad_and_face_buttons(data, current_pressed):
    global dpad_buttons

    face_button_map = {
        136: Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y,  
        72:  Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_B,  
        40:  Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_A,  
        24:  Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_X,  
    }

    byte5_val = data[BTYE_INDEX_DPAD]

    if byte5_val in face_button_map:
        for btn in dpad_buttons:
            Gamepad.ReleaseButton(btn)
        dpad_buttons.clear()
        current_pressed.add(face_button_map[byte5_val])
    else:
        summed = sum(data[i] for i in dPadCheckList)
        if summed > 0:
            for btn in dpad_buttons:
                Gamepad.ReleaseButton(btn)
            dpad_buttons.clear()
            return

        dpad_val = byte5_val & 0x0F
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

def sample_handler(data):
    global prev_data, pressed_buttons

    if prev_data is None:
        prev_data = data[:]
        return

    current_pressed = set()

    handle_music_inputs(data, current_pressed)
    handle_control_inputs(data, current_pressed)
    handle_dpad_and_face_buttons(data, current_pressed)

    for btn in pressed_buttons - current_pressed:
        if btn not in dpad_buttons:
            Gamepad.ReleaseButton(btn)

    for btn in current_pressed - pressed_buttons:
        Gamepad.PressButton(btn)

    pressed_buttons = current_pressed.copy()
    Gamepad.Update()
    prev_data = data[:]

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

    # Debug print if needed
    #if data != prev_data:
        #changed_indices = [i for i, (a,b) in enumerate(zip(data, prev_data)) if a != b]
        #print(f"Changed bytes: {changed_indices}")
        #print(f"Data: {[data[i] for i in changed_indices]}")

