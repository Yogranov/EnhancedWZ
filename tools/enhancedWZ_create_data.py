from PIL import ImageGrab
import time
import json
from pynput import mouse
import winsound


def pick_coordinate_sound():
    frequency = 1500
    duration = 100
    winsound.Beep(frequency, duration)
    time.sleep(0.05)
    winsound.Beep(frequency, duration)

def error_pick_coordinate_sound():
    frequency = 400
    duration = 100
    winsound.Beep(frequency, duration)
    time.sleep(0.1)
    winsound.Beep(round(frequency/2), duration)

def pick_color_sound():
    frequency = 1500
    duration = 100
    winsound.Beep(frequency, duration)
    time.sleep(0.05)
    winsound.Beep(frequency*2, duration)

def next_stage_sound():
    frequency = 1000
    duration = 100
    winsound.Beep(frequency, duration)
    time.sleep(0.05)
    winsound.Beep(frequency*2, duration)
    time.sleep(0.05)
    winsound.Beep(frequency*2, duration)
    time.sleep(0.05)
    winsound.Beep(frequency*2, duration)


def prolog():
    print("")
    print("Welcome to the data creation tool for the enhancedWZ project.")
    print("This tool will help you create the data.json file for the enhancedWZ project.")
    print("This file contain all the events and positions that the program will be looking for.")
    print("The program will ask you to pick the expected and unexpected colors and positions.")
    print("")

    print("Please follow the instructions below.")
    print("0. Before we start, please open the game and wait for the event to happen.")
    print("   * You can take a screenshot and save it for later, but remember to use full screen mode on the next steps.")
    print("")
    
    print("1. On the first step, you will need to enter a name for this event.")
    print("2. In the second step you will pick the expected colors and positions.")
    print("3. In the third step you will pick the unexpected colors and positions.")
    print(" * You can skip on any step by pressing the middle mouse button with no action before")
    print("4. After you are done with the unexpected colors and positions, the program will save the data to the 'new_data.json' file.")
    print("   You should open the 'new_data.json' file and add the new event to the 'data.json' file.")
    print("")

    print("Controls:")
    print("The way we will pick the colors and positions is by clicking on the screen.")
    print("The left click will pick the position and the right click will pick the color.")
    print("The middle click will move to the next step.")
    print("")

    print("Recap:")
    print("On the first step ('aka expected')' you just need to click on the positions that you expect to have the colors as they are right now.")
    print("On the second step ('aka unexpected') you need to RIGHT click FIRST on the color that you want to make sure the NEXT positions (with left key) you will click on is NOT (for example, right click on red and then left click on the sky).")
    print("")

    print("To help you while you are in the game, you will hear a sound effect for each mouse click.")
    input("Press enter to hear left click sound effect.")
    pick_coordinate_sound()
    input("Press enter to hear right click sound effect.")
    pick_color_sound()
    input("Press enter to hear middle click sound effect.")
    next_stage_sound()
    input("Press enter to hear error sound effect, the one you will hear if you click on the wrong mouse key (for example, trying to pick position on the second stage without picking color first).")
    error_pick_coordinate_sound()
    print("")

    input("Thats it, press enter to start and good luck!")


data = {}
expected_colors = []
unexpected_colors = []

position = None
stage = "expected"
last_mouse_position = [0, 0]
last_picked_color = [0,0,0]
last_pressed_key = None


def handle_left_click(x, y):
    global last_pressed_key
    global stage

    last_pressed_key = "left"

    last_mouse_position[0] = x
    last_mouse_position[1] = y

    if stage == "unexpected" and last_picked_color == [0,0,0]:
        return

    pick_coordinate_sound()
    
    time.sleep(0.1)

def handle_right_click(x, y):
    global last_pressed_key
    global stage

    last_pressed_key = "right"
    last_mouse_position[0] = x
    last_mouse_position[1] = y

    pick_color_sound()
    time.sleep(0.1)

def handle_middle_click():
    global last_pressed_key
    global stage
    last_pressed_key = "middle"

    if stage == "expected":
        stage = "unexpected"
    elif stage == "unexpected":
        print("Done recording.")
        stage = "done"

    next_stage_sound()
    time.sleep(0.1)

def on_click(x, y, button, pressed):
    if button == mouse.Button.right and pressed:
        handle_right_click(x, y)

    if button ==  mouse.Button.middle and pressed:
        handle_middle_click()
    
    if button == mouse.Button.left and pressed:
        handle_left_click(x, y)

    return False

    

if __name__ == "__main__":
    prolog()

    event_name = input("Enter event name: ")

    while True:
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()

        px = ImageGrab.grab().load()
        if stage != "expected":
            break


        p = last_mouse_position
        print("Expected coordinate: ", [p[0], p[1]])
        print("Expected color: ", px[p[0], p[1]])

        expected_colors.append({
            "coordinate": [p[0], p[1]],
            "color": px[p[0], p[1]]
        })


    while True:
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()

        px = ImageGrab.grab().load()
        if stage != "unexpected":
            break

        p = last_mouse_position
        if last_pressed_key == "right":
            last_picked_color = px[p[0], p[1]]
            print("Change last picked color to: ", last_picked_color)
            continue

        if last_pressed_key == "left" and last_picked_color == [0,0,0]:
            print("You must pick a color first.")
            error_pick_coordinate_sound()
            continue

        print("Unexpected coordinate: ", [p[0], p[1]])
        print("Unexpected color: ", last_picked_color)

        unexpected_colors.append({
            "coordinate": [p[0], p[1]],
            "color": last_picked_color
        })


        time.sleep(0.1)

    data[event_name] = {}
    data[event_name]["expected_colors"] = expected_colors
    data[event_name]["unexpected_colors"] = unexpected_colors

    with open("new_data.json", "w") as f:
        f.write(json.dumps(data, indent=4))

    print("Job done. New data saved to 'new_data.json' file.")