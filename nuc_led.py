
DRIVER_LOCATION = '/proc/acpi/nuc_led'

class LED:
    """
    "Abstract" base class from which to derive RingLED and PowerLED
    """

    _led_id = None
    _colours = None
    _styles = {'Always On': 'none','1Hz Blink':'blink_fast', '0.5Hz Blink': 'blink_medium' , "0.25Hz Blink":'blink_slow'
              ,'1Hz Fade':'fade_fast', '0.5Hz Fade': 'fade_medium' , "0.25Hz Fade":'fade_slow'}

    def styles(self):
        return(list(LED._styles.values()))

    def _read_led_state(self):
        print("Error")
        return({})

    def get_led_state(self):
        """
        Reads led state from DRIVER_LOCATION
        Returns a dict of led state
        """
        self._led_state.update(self._read_led_state())
        return(self._led_state)

    def turn_off_led(self):
        payload = self._led_state.copy()
        payload.update({'brightness': 0, 'style': 'none', 'colour': 'off'})
        self.set_led_state(payload)

    def set_led_state(self, data):
        """
        Writes content of data to DRIVER_LOCATION
        """
        brightness = data['brightness']
        style = data['style']
        colour = data['colour']
        f = open(DRIVER_LOCATION, 'w')
        payload = self.get_led_id() + ',' + str(brightness) + ',' + style + ',' + colour
        print(payload)
        print(payload, file=f)
        f.close()

        #update stored state
        self.get_led_state()

    def _get_state_from_text(self, text):
        brightness = (text[0]).split(': ')[1].split('%')[0]
        style = ((text[1]).split(': ')[1].split(' (')[0])
        colour = ((text[2]).split(': ')[1].split(' (')[0]).lower()

        data = {'brightness': int(brightness), 'style': LED._styles[style], 'colour': colour}
        return(data)

    def valid_colours(self):
        pass

    def set_brightness(self, brightness):
        brightness = max(0, min(100, brightness))
        payload = self._led_state.copy()
        payload.update({'brightness': brightness})
        print(payload)
        self.set_led_state(payload)

    def set_colour(self, colour):
        if (colour in self.valid_colours()):
            payload = self._led_state.copy()
            payload.update({'colour': colour})
            print(payload)
            self.set_led_state(payload)
        else:
            print("Attempted to pass invalid colour value")

    def set_style(self, style):
        if (style in LED._styles.values()    ):
            payload = self._led_state.copy()
            payload.update({'style': style})
            print(payload)
            self.set_led_state(payload)
        else:
            print("Attempted to pass invalid style value")

class RingLED(LED):
    """
    Derived class holding data specific to the ring led
    """

    _led_id = 'ring'
    _colours = ["off", "cyan", "pink", "yellow", "blue", "red", "green", "white"]


    def __init__(self):
        self._led_state = {'id': RingLED._led_id}
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
        self._led_state = {'id': PowerLED.led_id}
        self.get_led_state()

    def get_led_id(self):
        return(PowerLED._led_id)

    def valid_colours(self):
        return(PowerLED._colours)

    #def update_led_state(self):
    def _read_led_state(self):
        f = open(DRIVER_LOCATION, 'r')
        state = f.read()
        state = state.split('\n')
        power_state = state[:3]
        f.close()
        return(self._get_state_from_text(power_state))
