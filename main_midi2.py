import HIDInput
import mido
import threading
import time

MIDI_PORT_NAME = "Virtual Drum Kit 1"
midi_out = mido.open_output(MIDI_PORT_NAME)

def send_note_on(note, velocity=100, channel=9):
    msg = mido.Message('note_on', note=note, velocity=velocity, channel=channel)
    midi_out.send(msg)

def send_note_off(note, channel=9):
    msg = mido.Message('note_off', note=note, velocity=0, channel=channel)
    midi_out.send(msg)

def send_note_on_off(note, velocity=100, channel=9, duration=0.1):
    def worker():
        send_note_on(note, velocity, channel)
        time.sleep(duration)
        send_note_off(note, channel)
    threading.Thread(target=worker, daemon=True).start()

toms_to_midi_note = {
    43: 38,  
    44: 45,  
    45: 48,  
    46: 41,  
}

cymbals_to_midi_note = {
    47: 22,  
    48: 51,  
    49: 49,  
}


RIGHT_PEDAL_NOTE = 33  
LEFT_PEDAL_NOTE = 44   

face_button_exact_map = {
}

control_button_bitmask_map = {
    16: 64,  
    32: 65,  
}

GUIDE_NOTE = 68

dpad_map = {
    0: 69,  
    1: 70,  
    2: 71,  
    3: 72,  
    4: 73, 
    5: 74,  
    6: 75,  
    7: 76,  
}

prev_pedal_state = 0
pedal_note_state = {'left': False, 'right': False}
last_data = None
prev_buttons = set()

def scale_255_to_127(value):
    return max(0, min(127, int(value * 127 / 255)))

def handle_drums_and_cymbals(data):
    active_hit = False
    for byte_index, midi_note in toms_to_midi_note.items():
        if byte_index < len(data):
            raw_velocity = data[byte_index]
            if raw_velocity > 0:
                scaled = scale_255_to_127(raw_velocity)
                send_note_on_off(midi_note, scaled)
                active_hit = True

    for byte_index, midi_note in cymbals_to_midi_note.items():
        if byte_index < len(data):
            raw_velocity = data[byte_index]
            if raw_velocity > 0:
                scaled = scale_255_to_127(raw_velocity)
                send_note_on_off(midi_note, scaled)
                active_hit = True

    return active_hit

def handle_pedals(data):
    global pedal_note_state

    pedal_val = data[6] if len(data) > 6 else 0

    right_pressed = (pedal_val & 1) != 0
    left_pressed = (pedal_val & 2) != 0

    if right_pressed and not pedal_note_state['right']:
        send_note_on(RIGHT_PEDAL_NOTE, velocity=100)
        pedal_note_state['right'] = True
    elif not right_pressed and pedal_note_state['right']:
        send_note_off(RIGHT_PEDAL_NOTE)
        pedal_note_state['right'] = False

    if left_pressed and not pedal_note_state['left']:
        send_note_on(LEFT_PEDAL_NOTE, velocity=100)
        pedal_note_state['left'] = True
    elif not left_pressed and pedal_note_state['left']:
        send_note_off(LEFT_PEDAL_NOTE)
        pedal_note_state['left'] = False

def handle_buttons_and_dpad(data):
    pressed = set()

    byte5 = data[5] if len(data) > 5 else 0

    byte6 = data[6] if len(data) > 6 else 0
    byte7 = data[7] if len(data) > 7 else 0
    for mask, note in control_button_bitmask_map.items():
        if byte6 & mask:
            pressed.add(note)
    if byte7 & 0x01:
        pressed.add(GUIDE_NOTE)

    dpad_val = byte5 & 0x0F
    if dpad_val in dpad_map:
        pressed.add(dpad_map[dpad_val])

    return pressed

def sample_handler(data):
    global last_data, prev_buttons

    active_hit = handle_drums_and_cymbals(data)
    handle_pedals(data)

    pressed = handle_buttons_and_dpad(data)

    for note in prev_buttons - pressed:
        send_note_off(note)
    for note in pressed - prev_buttons:
        send_note_on(note)
    prev_buttons = pressed

    if last_data is None:
        last_data = list(data)
    else:
        changes = []
        for i in range(min(len(data), len(last_data))):
            if data[i] != last_data[i]:
                changes.append((i, last_data[i], data[i]))
        if changes:
            print("\nByte Changes Detected:")
            for i, before, after in changes:
                print(f"Byte[{i}]: {before} -> {after}")
            print("-" * 40)
        last_data = list(data)

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
