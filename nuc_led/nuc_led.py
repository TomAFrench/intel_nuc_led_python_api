from abc import ABC, abstractmethod

DRIVER_LOCATION = '/proc/acpi/nuc_led'

LED_ID = 'id'
BRIGHTNESS = 'brightness'
STYLE = 'style'
COLOUR = 'colour'

class LED(ABC):
    """
    "Abstract" base class from which to derive RingLED and PowerLED
    """

    _led_id = None
    _colours = None
    _styles = {'Always On': 'none','1Hz Blink':'blink_fast',
               '0.5Hz Blink': 'blink_medium', '0.25Hz Blink':'blink_slow',
               '1Hz Fade':'fade_fast', '0.5Hz Fade': 'fade_medium',
               '0.25Hz Fade':'fade_slow'}
    @abstractmethod
    def get_led_id(self):
        pass

    def styles(self):
        return(list(LED._styles.values()))

    @abstractmethod
    def valid_colours(self):
        pass

    @abstractmethod
    def _read_led_state(self):
        pass

    def get_led_state(self):
        """
        Reads led state from DRIVER_LOCATION
        Returns a dict of led state
        """
        self._led_state.update(self._read_led_state())
        return(self._led_state)

    def turn_off_led(self):
        payload = self._led_state.copy()
        payload.update({BRIGHTNESS: 0, STYLE: 'none', COLOUR: 'off'})
        self.set_led_state(payload)

    def set_led_state(self, data):
        """
        Writes content of data to DRIVER_LOCATION
        """
        brightness = data[BRIGHTNESS]
        style = data[STYLE]
        colour = data[COLOUR]
        f = open(DRIVER_LOCATION, 'w')
        payload = ','.join([self.get_led_id(), str(brightness), style, colour])
        print(payload, file=f)
        f.close()

        #update stored state
        self.get_led_state()

    def _get_state_from_text(self, text):
        brightness = (text[0]).split(': ')[1].split('%')[0]
        style = ((text[1]).split(': ')[1].split(' (')[0])
        colour = ((text[2]).split(': ')[1].split(' (')[0]).lower()

        data = {BRIGHTNESS: int(brightness),
                STYLE: LED._styles[style],
                COLOUR: colour}
        return(data)

    def set_brightness(self, brightness):
        brightness = max(0, min(100, brightness))
        payload = self._led_state.copy()
        payload.update({BRIGHTNESS: brightness})
        self.set_led_state(payload)

    def set_colour(self, colour):
        if (colour in self.valid_colours()):
            payload = self._led_state.copy()
            payload.update({COLOUR: colour})
            self.set_led_state(payload)
        else:
            print("Attempted to pass invalid colour value")

    def set_style(self, style):
        if (style in LED._styles.values()    ):
            payload = self._led_state.copy()
            payload.update({STYLE: style})
            self.set_led_state(payload)
        else:
            print("Attempted to pass invalid style value")

class RingLED(LED):
    """
    Derived class holding data specific to the ring led
    """

    _led_id = 'ring'
    _colours = ["off", "cyan", "pink", "yellow",
                "blue", "red", "green", "white"]


    def __init__(self):
        self._led_state = {LED_ID: RingLED._led_id}
        self.get_led_state()

    def get_led_id(self):
        return(RingLED._led_id)

    def valid_colours(self):
        return(RingLED._colours)

    def _read_led_state(self):
        f = open(DRIVER_LOCATION, 'r')
        state = f.read()
        state = state.split('\n')
        ring_state = state[4:-2]
        f.close()
        return(self._get_state_from_text(ring_state))



class PowerLED(LED):
    """
    Derived class holding data specific to the power led
    """

    _led_id = 'power'
    _colours = ["off", "blue", "amber"]

    def __init__(self):
        self._led_state = {LED_ID: PowerLED.led_id}
        self.get_led_state()

    def get_led_id(self):
        return(PowerLED._led_id)

    def valid_colours(self):
        return(PowerLED._colours)

    def _read_led_state(self):
        f = open(DRIVER_LOCATION, 'r')
        state = f.read()
        state = state.split('\n')
        power_state = state[:3]
        f.close()
        return(self._get_state_from_text(power_state))
