from charlieplexer import Charlieplexer
from utils import signal_is_digit_0_to_5
from datetime import datetime, timedelta
import time

class LED_board:
    """ Simulated LED board. Acts though Charlieplexer """
    def __init__(self, GPIO):
        self.GPIO = GPIO
        self.charlieplexer = Charlieplexer(self.GPIO)

    def light_led(self, led_nr):
        fire_led = {
            '0': self.charlieplexer.fire_led_0,
            '1': self.charlieplexer.fire_led_1,
            '2': self.charlieplexer.fire_led_2,
            '3': self.charlieplexer.fire_led_3,
            '4': self.charlieplexer.fire_led_4,
            '5': self.charlieplexer.fire_led_5
        }
        if signal_is_digit_0_to_5(str(led_nr)):
            fire_led[str(led_nr)]()
            self.GPIO.show_leds_states()

    def light_led_for_time(self, led_nr, sec):
        self.light_led(led_nr)
        time.sleep(sec)
        self.disable_all_leds()

    def flash_all_leds_once(self):
        self.fire_leds_for_seconds((0, 1, 2, 3, 4, 5), 1)
        self.disable_all_leds_for_seconds(0.2)

    def flash_all_leds_multiple_times(self, times):
        for i in range(times):
            self.fire_leds_for_seconds((0, 1, 2, 3, 4, 5), 0.3)
            if i != times-1:
                self.disable_all_leds_for_seconds(0.3)
            else:
                # This minimizes the time the user cannot interact with the Keypad
                # Yet it makes sure all leds are disabled by the end of the flashing
                self.disable_all_leds()

    def twinkle_all_leds(self):
        for i in range(6):
            self.light_led(i)
            time.sleep(0.5)
        self.disable_all_leds()

    def fire_leds_for_seconds(self, leds, sec):
        end_time = datetime.now() + timedelta(seconds=sec)
        while datetime.now() < end_time:
            for led in leds:
                self.light_led(led)

    def disable_all_leds(self):
        self.charlieplexer.disable()
        self.GPIO.show_leds_states()

    def disable_all_leds_for_seconds(self, sec):
        end_time = datetime.now() + timedelta(seconds=sec)
        while datetime.now() < end_time:
            self.charlieplexer.disable()
            self.GPIO.show_leds_states()

    def twinkle_leds_from_centre(self):
        self.twinkle_led_combinations(((2, 3), (1, 4), (0, 5)))

    def twinkle_leds_from_edges(self):
        self.twinkle_led_combinations(((0, 5), (1, 4), (2, 3)))

    def twinkle_led_combinations(self, combinations):
        for combination in combinations:
            self.fire_leds_for_seconds(combination, 0.5)
        self.disable_all_leds()
