from abc import ABC, abstractmethod

DRIVER_LOCATION = "/proc/acpi/nuc_led"

LED_ID = "id"
BRIGHTNESS = "brightness"
STYLE = "style"
COLOR = "color"


class LEDError(Exception):
    pass


class ColorIsNotValidException(LEDError):
    def __init__(self, color):
        super().__init__("Color {0} is not valid color".format(color))


class StyleIsNotValidException(LEDError):
    def __init__(self, style):
        super().__init__("Style {0} is not valid style".format(style))


class LED(ABC):
    """
    The abstract base class for all LED types. Contains common methods.
    """

    _led_id = None
    _colors = None
    _styles = {
        "Always On": "none",
        "1Hz Blink": "blink_fast",
        "0.5Hz Blink": "blink_medium",
        "0.25Hz Blink": "blink_slow",
        "1Hz Fade": "fade_fast",
        "0.5Hz Fade": "fade_medium",
        "0.25Hz Fade": "fade_slow",
    }

    @abstractmethod
    def get_led_id(self):
        pass

    def styles(self):
        return list(LED._styles.values())

    @abstractmethod
    def valid_colors(self):
        pass

    @abstractmethod
    def _read_led_state(self):
        pass

    def get_led_state(self):
        """
        Returns LED state

        :rtype: Dictionary of LED state
        """
        self._led_state.update(self._read_led_state())
        return self._led_state

    def set_led_state(self, data):
        """
        Writes content of data to DRIVER_LOCATION

        :param data: Dictionary of desired LED state
        """
        current_state = self.get_led_state()
        brightness = data.get(BRIGHTNESS, current_state[BRIGHTNESS])
        style = data.get(STYLE, current_state[STYLE])
        color = data.get(COLOR, current_state[COLOR])

        payload = ",".join([self.get_led_id(), str(brightness), style, color])
        with open(DRIVER_LOCATION, "w") as file:
            print(payload, file=file)

        # update stored state
        self.get_led_state()

    def _get_state_from_text(self, text):
        """
        Constructs a dictionary representation of the LED state

        :param text: Relevant LED state text as returned from kernel module
        """
        brightness = (text[0]).split(": ")[1].split("%")[0]
        style = (text[1]).split(": ")[1].split(" (")[0]
        color = ((text[2]).split(": ")[1].split(" (")[0]).lower()

        data = {BRIGHTNESS: int(brightness), STYLE: LED._styles[style], COLOR: color}
        return data

    def set_brightness(self, brightness):
        brightness = max(0, min(100, brightness))
        self.set_led_state({BRIGHTNESS: brightness})

    def set_color(self, color):
        if color in self.valid_colors():
            self.set_led_state({COLOR: color})
        else:
            raise ColorIsNotValidException(color)

    def set_style(self, style):
        if style in LED._styles.values():
            self.set_led_state({STYLE: style})
        else:
            raise StyleIsNotValidException(style)

    def turn_off_led(self):
        self.set_led_state({BRIGHTNESS: 0, STYLE: "none", COLOR: "off"})


class RingLED(LED):
    """
    Ring LED
    """

    _led_id = "ring"
    _colors = ["off", "cyan", "pink", "yellow", "blue", "red", "green", "white"]

    def __init__(self):
        self._led_state = {LED_ID: RingLED._led_id}
        self.get_led_state()

    def get_led_id(self):
        return RingLED._led_id

    def valid_colors(self):
        return RingLED._colors

    def _read_led_state(self):
        with open(DRIVER_LOCATION, "r") as file:
            state = file.read()

        state = state.split("\n")
        ring_state = state[4:-2]
        return self._get_state_from_text(ring_state)


class PowerLED(LED):
    """
    Power button LED.
    """

    _led_id = "power"
    _colors = ["off", "blue", "amber"]

    def __init__(self):
        self._led_state = {LED_ID: PowerLED._led_id}
        self.get_led_state()

    def get_led_id(self):
        return PowerLED._led_id

    def valid_colors(self):
        return PowerLED._colors

    def _read_led_state(self):
        with open(DRIVER_LOCATION, "r") as file:
            state = file.read()

        state = state.split("\n")
        power_state = state[:3]
        return self._get_state_from_text(power_state)
