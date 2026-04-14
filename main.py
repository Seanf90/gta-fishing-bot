import time
import pyautogui
import win32api
import win32con
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController, Button

# Initialize controllers
keyboard = KeyboardController()
mouse = MouseController()


def press_mouse():
    mouse.press(Button.left)
    pyautogui.mouseDown()
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)


def release_mouse():
    mouse.release(Button.left)
    pyautogui.mouseUp()
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def press_key_4():
    """Press the '4' key to equip and cast the fishing rod."""
    time.sleep(0.5)
    keyboard.press('4')
    time.sleep(0.1)
    keyboard.release('4')
    print("Pressed 4 to cast fishing rod")


def detect_fish_popup():
    """
    Wait for the fish event popup to appear on screen.
    Times out after 20 seconds and presses Escape to reset if nothing is detected.
    """
    start_time = time.time()
    timeout_duration = 20

    while True:
        try:
            fish_popup_1 = pyautogui.locateOnScreen('test1.png', confidence=0.75)
            fish_popup_2 = pyautogui.locateOnScreen('test2.png', confidence=0.75)

            if fish_popup_1:
                print("Fish detected with test1.png!")
                return
            if fish_popup_2:
                print("Fish detected with test2.png!")
                return

        except pyautogui.ImageNotFoundException:
            print("Fish popup not found, retrying...")

        if time.time() - start_time > timeout_duration:
            print("Timeout reached. Pressing Escape to restart.")
            pyautogui.press('esc')
            time.sleep(1)
            pyautogui.press('esc')
            print("Escape pressed twice, restarting fishing process.")
            return

        time.sleep(0.5)


def detect_bobber_state():
    """
    Check the current colour state of the fishing bobber.
    Returns: 'green', 'yellow', 'red', or 'none'.
    """
    bobber_states = {
        'green':  ['greencolour.png'],
        'yellow': ['yellowcolour2.png'],
        'red':    ['redcolour.png', 'redtest.png', 'redtest3.png'],
        'none':   ['nocolour.png', 'nocolour2.png', 'nocolour3.png']
    }

    for state, images in bobber_states.items():
        for image in images:
            try:
                if pyautogui.locateOnScreen(image, confidence=0.75):
                    print(f"{state.capitalize()} bobber detected.")
                    return state
            except pyautogui.ImageNotFoundException:
                continue

    print("No bobber state detected.")
    return 'none'


def detect_fish_caught():
    """
    Check whether a fish has been successfully caught or the minigame has ended.
    Returns True if a catch/stop condition is detected.
    """
    stop_images = ['stoptest1.png', 'stoptest2.png', 'caught_mack.png', 'caught_bass.png', 'turtlestop.png']

    for image in stop_images:
        try:
            if pyautogui.locateOnScreen(image, confidence=0.75):
                print(f"Fish caught / stop condition detected ({image}).")
                return True
        except pyautogui.ImageNotFoundException:
            continue

    return False


def detect_fish_away():
    """
    Check whether the fish has escaped.
    Returns True if the 'fish away' screen is detected.
    """
    try:
        if pyautogui.locateOnScreen('fishaway2.png', confidence=0.9):
            print("Fish got away! Restarting process...")
            return True
    except pyautogui.ImageNotFoundException:
        pass

    return False


def reel_in_fish():
    """
    Main reeling loop. Holds or releases the mouse based on bobber colour state:
      - Green / Yellow: hold mouse to reel in
      - Red: release mouse briefly
    Exits when the fish is caught, escapes, or the bobber is lost.
    """
    is_mouse_pressed = False
    max_failed_attempts = 3
    failed_attempts = 0

    print("Started reeling in fish...")
    press_mouse()
    is_mouse_pressed = True

    try:
        while True:
            if detect_fish_caught():
                print("Fish caught — ending reel.")
                time.sleep(0.5)
                return

            if detect_fish_away():
                return

            bobber_state = detect_bobber_state()
            print(f"Bobber state: {bobber_state}")

            if bobber_state == 'none':
                failed_attempts += 1
                if failed_attempts >= max_failed_attempts:
                    print("Lost bobber — exiting reeling process.")
                    return
                time.sleep(0.1)
                continue

            failed_attempts = 0  # Reset counter on a valid detection

            if bobber_state == 'red':
                if is_mouse_pressed:
                    release_mouse()
                    is_mouse_pressed = False
                    print("Red bobber — releasing mouse.")
                time.sleep(0.015)

            else:  # green or yellow: reel in
                if not is_mouse_pressed:
                    for _ in range(7):
                        press_mouse()
                    is_mouse_pressed = True
                    print(f"{bobber_state.capitalize()} bobber — reeling in.")
                time.sleep(0.1)

    finally:
        # Always release the mouse when exiting, regardless of how we leave
        if is_mouse_pressed:
            release_mouse()
            print("Mouse released on exit.")


def fish_automation():
    """Main loop — casts, waits for a bite, reels in, and repeats indefinitely."""
    while True:
        press_key_4()
        detect_fish_popup()
        reel_in_fish()
        print("Restarting fishing process...")
        time.sleep(0.64)


if __name__ == "__main__":
    fish_automation()
