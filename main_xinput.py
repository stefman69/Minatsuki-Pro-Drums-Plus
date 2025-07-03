import Gamepad
import HIDInput
import time

prev_input_data = None
KICK_BYTE_INDEX = 6
KICK_ACTIVE_VALUE = 1
GUIDE_BYTE_INDEX = 7
GUIDE_ACTIVE_MASK = 0x01

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
    BTYE_INDEX_GREEN_CYMBAL: [Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_A, Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB],
    BTYE_INDEX_BLUE_CYMBAL:  [Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_X, Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB],
    BTYE_INDEX_YELLOW_CYMBAL:[Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y, Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB],
    BTYE_INDEX_RED_DRUM:     [Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_B],
    BTYE_INDEX_YELLOW_DRUM:  [Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y],
    BTYE_INDEX_BLUE_DRUM:    [Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_X],
    BTYE_INDEX_GREEN_DRUM:   [Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_A]
}

pad_check_indices = list(mapping.keys())

pressed_buttons = set()
dpad_buttons = set()
prev_dpad = -1
prev_kick_state = 0
prev_guide_state = 0
prev_analog_val = 0

prev_start_state = False
prev_back_state = False

def handle_music_inputs(data, current_pressed):
    global prev_kick_state

    kick_val = data[KICK_BYTE_INDEX]

    if kick_val == 1:  
        current_pressed.add(Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    elif kick_val == 2:  
        current_pressed.add(Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    elif kick_val == 3:  
        current_pressed.add(Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        current_pressed.add(Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)

    for byte_offset, buttons in mapping.items():
        if byte_offset >= len(data):
            continue
        if data[byte_offset] > 0:
            current_pressed.update(buttons)

    prev_kick_state = kick_val
    

def handle_dpad_and_face_buttons(data, current_pressed):
    global prev_dpad, prev_analog_val, dpad_buttons, last_dpad_val

    analog_val = data[DPAD_BYTE_INDEX]
    dpad_val = analog_val & 0x0F

    face_button_map = {
        136: Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y,
        72:  Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_B,
        40:  Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_A,
        24:  Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_X,
    }

    analog_val = data[DPAD_BYTE_INDEX]
    if analog_val in face_button_map:
        current_pressed.add(face_button_map[analog_val])
        for btn in dpad_buttons:
            Gamepad.ReleaseButton(btn)
        dpad_buttons.clear()
    elif sum(data[i] for i in pad_check_indices) == 0:
        dpad_val = analog_val & 0x0F
        new_dpad = set()

        if dpad_val == 0:
            new_dpad.add(Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        elif dpad_val == 1:
            new_dpad.update([Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP, Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT])
        elif dpad_val == 2:
            new_dpad.update([Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN, Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT])
        elif dpad_val == 3:
            new_dpad.add(Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
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

    prev_analog_val = analog_val

def handle_control_buttons(data, current_pressed):
    byte6 = data[ANALOG_BYTE_INDEX] 
    byte7 = data[GUIDE_BYTE_INDEX] 

    control_button_map = {
        0x10: Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
        0x20: Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_START,
    }

    for mask, btn in control_button_map.items():
        if (byte6 & mask) != 0:
            current_pressed.add(btn)

    if (byte7 & GUIDE_ACTIVE_MASK) != 0:
        current_pressed.add(Gamepad.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE)
        
# This is for printing input data, as is the second line in the next fuction
#def debug_print_input_changes(data):
    #global prev_input_data
    #if prev_input_data is None:
        #prev_input_data = list(data)
        #return

    #for i, (old, new) in enumerate(zip(prev_input_data, data)):
        #if old != new:
            #print(f"Byte {i} changed from {old} to {new}")

    #prev_input_data = list(data)

def sample_handler(data):
    global pressed_buttons, prev_start_state, prev_back_state

    #debug_print_input_changes(data) 

    byte6 = data[ANALOG_BYTE_INDEX]

    start_pressed = (byte6 & 0x20) != 0
    back_pressed = (byte6 & 0x10) != 0

    prev_start_state = start_pressed
    prev_back_state = back_pressed

    current_pressed = set()


    handle_music_inputs(data, current_pressed)

    handle_dpad_and_face_buttons(data, current_pressed)

    handle_control_buttons(data, current_pressed)

    for btn in pressed_buttons - current_pressed:
        if btn not in dpad_buttons:
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
