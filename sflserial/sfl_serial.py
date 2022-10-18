"""Custom serial number generation plugin for InvenTree

Provides serial number generation and validation as specified by Toronto Space Flight Labs

This software is distributed under the MIT license (see LICENSE file)
"""

# Generic libraries
import string

# Django libraries
from django.core.exceptions import ValidationError

# InvenTree plugin libraries
from plugin import InvenTreePlugin
from plugin.mixins import SettingsMixin, ValidationMixin

from sflserial.version import SFL_PLUGIN_VERSION


class SFLSerialNumberPlugin(SettingsMixin, ValidationMixin, InvenTreePlugin):
    """Serial number generation and validation plugin.
    
    Serial numbers should be formatted like:

    - AAA
    - AAB
    - AAC
    - ...
    - ABA
    - ...
    - ZZZ
    - AAAA
    
    """

    # Plugin metadata
    NAME = "SFL Serial"
    TITLE = "SFL Serial Number Generator"
    DESCRIPTION = "Serial number generation plugin for Toronto Space Flight Labs"
    SLUG = "sflserial"
    VERSION = SFL_PLUGIN_VERSION

    # No custom settings currently, but can be expanded as required
    SETTINGS = {}

    def validate_serial_number(self, serial: str):
        """Serial number validation routine:
        
        - Must be at least three characters long
        - Must only consist of characters A-Z
        """
        
        if len(serial) < 3:
            raise ValidationError("Serial number must be at least three characters")

        for c in serial:
            if c not in string.ascii_uppercase:
                raise ValidationError("Serial number can only contain characters A-Z")
        
    def convert_serial_to_int(self, serial: str):
        """Convert a serial number (string) to an integer representation.
        
        Essentially this serial number scheme is a "base 26" number?
        
        Iterate through each character, and if we find a "weird" character, simply return None
        """

        num = 0

        # Reverse iterate through the serial number string
        for idx, c in enumerate(serial[::-1]):
            if c not in string.ascii_uppercase:
                # An invalid character, not sure how to continue
                # Also, should not ever get here due to validate_serial_number routine
                return None

            c_int = ord(c) - ord('A')
            c_int *= (26 ** idx)

            num += c_int
        
        return num

    def increment_serial_number(self, serial: str):
        """Find the next serial number in the required sequence

        e.g.
        AAA -> AAB
        AAZ -> ABA
        DQX -> DQY
        ZZZ -> AAAA
        """

        if serial in [None, '']:
            # Provide an initial condition
            return "AAA"

        output = ''
        rollover = False

        for c in serial[::-1]:
            # If any character is invalid, return immediately
            if c not in string.ascii_uppercase:
                return None
            
            if not rollover:
                if c == 'Z':
                    c = 'A'
                else:
                    rollover = True
                    c = chr(ord(c) + 1)
            
            output = c + output
        
        # If we get to the end of the sequence without incrementing, add a new character
        if not rollover:
            output = 'A' + output
        
        return output
