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


cymbal_states = {index: False for index in cymbals_to_midi_note}
pedal_note_state = {'left': False, 'right': False}
hi_hat_pedal_held = False  
last_data = None
prev_buttons = set()

RIGHT_PEDAL_NOTE = 33
LEFT_PEDAL_NOTE = 44

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

def scale_255_to_127(value):
    return max(0, min(127, int(value * 127 / 255)))

def handle_drums_and_cymbals(data):
    global hi_hat_pedal_held
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
            velocity = data[byte_index]

            if byte_index == 47:  
                mapped_note = 42 if hi_hat_pedal_held else 46
            else:
                mapped_note = midi_note  
    
            if velocity > 0 and not cymbal_states[byte_index]:
                cymbal_states[byte_index] = True
                send_note_on_off(mapped_note, velocity)
                active_hit = True
            elif velocity == 0 and cymbal_states[byte_index]:
                cymbal_states[byte_index] = False


    return active_hit

def handle_pedals(data):
    global pedal_note_state, hi_hat_pedal_held

    pedal_val = data[6] if len(data) > 6 else 0
    right_pressed = (pedal_val & 1) != 0
    left_pressed = (pedal_val & 2) != 0

    hi_hat_pedal_held = left_pressed

    if right_pressed and not pedal_note_state['right']:
        send_note_on(RIGHT_PEDAL_NOTE, velocity=100)
        pedal_note_state['right'] = True
    elif not right_pressed and pedal_note_state['right']:
        send_note_off(RIGHT_PEDAL_NOTE)
        pedal_note_state['right'] = False

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

    handle_pedals(data)
    handle_drums_and_cymbals(data)

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
