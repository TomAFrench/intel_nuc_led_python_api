# Intel NUC7i[x]BN and NUC6CAY LED Control

This is a simple python library for ease of integration and use of the kernel module [here](https://github.com/TomAFrench/intel_nuc_led) (forked from original work by [milesp20](https://github.com/milesp20/intel_nuc_led)) designed for Intel NUC7i[x]BN and NUC6CAY kits.

## Usage

This library exposes two classes RingLED and PowerLED to represent the two leds on the NUC which have methods to control their brightness, color and style.

### Brightness:

LED brightness may be set using the `set_brightness(level)` method where level may take any integer value between `0` and `100`

### Colour:

LED color may be set using the `set_color(new_color)` where `new_color` may take the values in the following table

|LED Color|power|ring|
|---------|:---:|:--:|
|amber    |X    |    |
|cyan     |     |X   |
|blue     |X    |X   |
|green    |     |X   |
|off      |X    |X   |
|pink     |     |X   |
|red      |     |X   |
|white    |     |X   |
|yellow   |     |X   |
    

### Style:

LED style may be set using the `set_style(option)` where `option` may take the values in the following table


|Blink/Fade Option|Description    |
|-----------------|---------------|
|blink\_fast      |1Hz blink      |
|blink\_medium    |0.5Hz blink    |
|blink\_slow      |0.25Hz blink   |
|fade\_fast       |1Hz blink      |
|fade\_medium     |0.5Hz blink    |
|fade\_slow       |0.25Hz blink   |
|none             |solid/always on|
