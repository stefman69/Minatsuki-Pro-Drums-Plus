import time
import vgamepad as vg
from enum import IntFlag

gamepad = vg.VX360Gamepad()

class XUSB_BUTTON(IntFlag):
    XUSB_GAMEPAD_DPAD_UP = 0x0001
    XUSB_GAMEPAD_DPAD_DOWN = 0x0002
    XUSB_GAMEPAD_DPAD_LEFT = 0x0004
    XUSB_GAMEPAD_DPAD_RIGHT = 0x0008
    XUSB_GAMEPAD_START = 0x0010
    XUSB_GAMEPAD_BACK = 0x0020
    XUSB_GAMEPAD_LEFT_THUMB = 0x0040
    XUSB_GAMEPAD_RIGHT_THUMB = 0x0080
    XUSB_GAMEPAD_LEFT_SHOULDER = 0x0100
    XUSB_GAMEPAD_RIGHT_SHOULDER = 0x0200
    XUSB_GAMEPAD_GUIDE = 0x0400
    XUSB_GAMEPAD_A = 0x1000
    XUSB_GAMEPAD_B = 0x2000
    XUSB_GAMEPAD_X = 0x4000
    XUSB_GAMEPAD_Y = 0x8000

def PressButton(button):
    if isinstance(button, (list, tuple)):
        for b in button:
            gamepad.press_button(button=b)
    else:
        gamepad.press_button(button=button)
    gamepad.update()

def ReleaseButton(button):
    if isinstance(button, (list, tuple)):
        for b in button:
            gamepad.release_button(button=b)
    else:
        gamepad.release_button(button=button)
    gamepad.update()

def PressButtonOnce(button, duration=0.05):
    PressButton(button)
    time.sleep(duration)
    ReleaseButton(button)

def Update():
    gamepad.update()

if __name__ == "__main__":
    PressButtonOnce(XUSB_BUTTON.XUSB_GAMEPAD_A)
    time.sleep(0.5)
    PressButton(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
    PressButton(XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    Update()
    time.sleep(0.5)
    ReleaseButton(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
    ReleaseButton(XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    Update()
    gamepad.reset()
    Update()
