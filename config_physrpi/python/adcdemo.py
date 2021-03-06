#!/usr/bin/env python3
#
# adcdemo.py - ADC demo with ADS1015
#
# 30Jan19  Updated comments
# 30Jan18  Increased resolution of print command,
#          changed full-scale range to 4096
# 18May16  Adapted from Adafruit code by Everett Lipman
#

import sys
import time

#
# Adafruit libraries modified by Ben Laroque for Python 3 and ADS1015
#
from Adafruit import ADS1x15
###############################################################################

#
# Default ADC IC is ADS1015
# Default address is 0x48 on the default I2C bus
#
adc = ADS1x15()

# Single ended:
#
# First argument is channel
# Second argument is the full-scale range in mV (default +/- 6144).
#    options: 256, 512, 1024, 2048, 4096, 6144.
#    Note: input must not exceed VDD + 0.3
# Third argument is samples per second (default 250).
#    options: 128, 250, 490, 920, 1600, 2400, 3300.
# Return value is in millivolts.
#
# v2 = adc.readADCSingleEnded(2, 4096, 250)*0.001
# v3 = adc.readADCSingleEnded(3, 4096, 250)*0.001

# Differential:
#
# First argument is the full-scale range in mV (default +/- 6144).
#    options: 256, 512, 1024, 2048, 4096, 6144.
#    Note: input must not exceed VDD + 0.3
# Second argument is samples per second (default 250).
#    options: 128, 250, 490, 920, 1600, 2400, 3300.
# Return value is in millivolts.
#
# v01 = adc.readADCDifferential01(4096, 128)*0.001  # returns float
# v23 = adc.readADCDifferential23(4096, 128)*0.001  # returns float

#
# Read channels 2 and 3 in differential mode.  See above for defaults.
#
# Slower sampling -> lower noise.
#
while True:
   v23 = adc.readADCDifferential23(4096, 128)*0.001  # returns float
   print('%.4f V' % v23)
   time.sleep(0.5)
