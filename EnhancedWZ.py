from time import sleep
from PIL import ImageGrab
import json

class EnhancedWZ:

    ###### public ######
    def Start(self):
        self.__loop()

    def Subscribe_to_red_alert(self, callback):
        self.__cb_dict['red_alert'] = callback

    def Subscribe_to_precision_airstrike(self, callback):
        self.__cb_dict['precision_airstrike'] = callback

    def Subscribe_to_test(self, callback):
        self.__cb_dict['test'] = callback

    ###### private ######
    __COOLDOWN_DURATION = 4

    __screenshot = None
    __cooldown = False
    __data = None
    __cb_dict = {
        'red_alert': None,
        'precision_airstrike': None,
        'test': None
    }

    def __init__(self):
        f = open('data.json')
        self.__data = json.load(f)


    def __loop(self):
        print("Start running EnhancedWZ...")
        while True:
            self.__screenshot = ImageGrab.grab().load()
            for item in self.__cb_dict.items():
                if item[1] is not None:
                    self.__search_for_event(item[0])

            if self.__cooldown:
                sleep(self.__COOLDOWN_DURATION)
                self.__cooldown = False

            sleep(0.01)

    def __fire_callback(self, callback : str):
        if callback is not None:
            print(f"{callback} found, calling callback")
            self.__cb_dict[callback]()
            self.__cooldown = True


    def __search_for_event(self, event_name: str):
        data = self.__data[event_name]
        should_fire = True
        expected_colors = data['expected_colors']
        for object in expected_colors:
            if not self.__is_color(object['coordinate'], object['color']):
                should_fire = False
                break

        unexpected_colors = data['unexpected_colors']
        for object in unexpected_colors:
            if self.__is_color(object['coordinate'], object['color']):
                should_fire = False
                break
    
        if should_fire:
            self.__fire_callback(event_name)

    
    def __is_color(self, coordinate: tuple, color: tuple, tolerance: int = 20):
        pixel = self.__screenshot[coordinate[0], coordinate[1]]

        return pixel[0] > color[0] - tolerance and pixel[0] < color[0] + tolerance and pixel[1] > color[1] - tolerance and pixel[1] < color[1] + tolerance and pixel[2] > color[2] - tolerance and pixel[2] < color[2] + tolerance
