#!/usr/bin/env python3

#
# pwmset.py - Set hardware PWM duty cycle
#
# 02Mar19  Updated to decrease frequency and increase resolution
# 12Mar18  Everett Lipman
#

DEFDUTY = 0.0

USAGE="""
usage: pwmset.py [duty]

       duty is the PWM duty cycle as a percentage.
       Default is %.1f.
""" % DEFDUTY

import os
import sys
from wpdir import wiringpi

#
# constants
#
PWM_OUTPUT = 2  # pin mode
PWM_MODE_MS = 0 # standard mark-space PWM

PWMPIN = 18  # Broadcom pin numbering

#
# The PWM clock base frequency is 19.2 MHz.  The counter
# is incremented at the base frequency divided by PWM_DIVISOR.
# When it reaches PWM_RANGE counts, it begins a new cycle.
# The output in mark-space mode is held high until the
# counter reaches the value set by pwmWrite().
#
# RANGE:  300; DIVISOR: 2 -> 32 kHz PWM with a resolution of 300 steps
# RANGE: 4000; DIVISOR: 2 -> 2.4 kHz PWM with a resolution of 4000 steps
#
PWM_RANGE = 4000  # must be less than 4096
PWM_DIVISOR = 2   # must be between 2 and 4095
###############################################################################

#
# Check user ID - must be running with root privileges
#
euid = os.geteuid()
if euid != 0:
   print('\nThis program must be run as root.  Try using sudo.',
          file=sys.stderr)
   print('Exiting.\n', file=sys.stderr)
   exit(1)

retval = wiringpi.wiringPiSetupGpio()  # use Broadcom pin numbering
if retval != 0:
   print('wiringpi setup error.  Exiting.', file=sys.stderr)
   exit(1)

wiringpi.pinMode(PWMPIN, PWM_OUTPUT)
wiringpi.pwmSetMode(PWM_MODE_MS)
wiringpi.pwmSetClock(PWM_DIVISOR)
wiringpi.pwmSetRange(PWM_RANGE)
###############################################################################

if len(sys.argv) == 1:
   duty = DEFDUTY
else:
   try:
      duty = float(sys.argv[1])/100.0
   except:
      print(file=sys.stderr)
      print(USAGE, file=sys.stderr)
      print(file=sys.stderr)
      exit(1)

if duty > 1.0 or duty < 0.0:
   print(file=sys.stderr)
   print(USAGE, file=sys.stderr)
   print(file=sys.stderr)
   exit(1)

duty_counts = int(duty*PWM_RANGE)
duty_pct = 100.0*float(duty_counts)/PWM_RANGE

print()
print('Setting PWM duty cycle to %.3f %%  (%d/%d)' % (duty_pct, duty_counts,
                                                      PWM_RANGE))

wiringpi.pwmWrite(PWMPIN, duty_counts)  # Allowable values: 0 to PWM_RANGE

print('done.\n')
