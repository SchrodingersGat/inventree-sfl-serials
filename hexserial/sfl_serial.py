"""Custom serial number generation plugin for InvenTree

Provides hexadecimal serial number generation and validation

This software is distributed under the MIT license (see LICENSE file)
"""

# Generic libraries
import string

# Django libraries
from django.core.exceptions import ValidationError

# InvenTree plugin libraries
from plugin import InvenTreePlugin
from plugin.mixins import SettingsMixin, ValidationMixin

from hexserial.version import INVENTREE_HEX_PLUGIN_VERSION


class HexSerialNumberPlugin(SettingsMixin, ValidationMixin, InvenTreePlugin):
    """Serial number generation and validation plugin.
    
    Serial numbers should be formatted like:

    - 12B
    - AZA
    - AA3
    - A7C
    - ...
    - ABA
    - ...
    - ZZZ
    - AAAA
    
    """

    # Plugin metadata
    NAME = "Hex Serials"
    AUTHOR = "Oliver Walters"
    TITLE = "Hex Serial Number Generator"
    DESCRIPTION = "Hexadecimal serial number generation plugin"
    SLUG = "hexserial"
    VERSION = INVENTREE_HEX_PLUGIN_VERSION

    # InvenTree version requirements
    MIN_VERSION = '0.9.0'

    # No custom settings currently, but can be expanded as required
    SETTINGS = {}

    def valid_chars(self):
        """Return a list of characters which can be used in this serial number schema:
        
        - Allow uppercase alphanumeric characters
        - Exclude '0' and 'O' characters

        This list of characters also specifies the 'increment' order
        """

        allowed = string.digits + string.ascii_uppercase

        # The following characters are explicitly disallowed in the schema
        disallowed = 'O0'

        for c in disallowed:
            idx = allowed.index(c)
            allowed = allowed[:idx] + allowed[idx+1:]
        
        return allowed

    def validate_serial_number(self, serial: str):
        """Serial number validation routine:
        
        - Must be at least three characters long
        - Must only consist of characters A-Z
        """
        
        if len(serial) < 3:
            raise ValidationError("Serial number must be at least three characters")

        valid = self.valid_chars()

        for c in serial:
            if c not in valid:
                raise ValidationError(f"Serial number contains prohibited character: {c}")
        
    def convert_serial_to_int(self, serial: str):
        """Convert a serial number (string) to an integer representation.    
        Iterate through each character, and if we find a "weird" character, simply return None
        """

        num = 0

        valid = self.valid_chars()
        N = len(valid)

        # Reverse iterate through the serial number string
        for idx, c in enumerate(serial[::-1]):
            if c not in valid:
                # An invalid character, not sure how to continue
                # Also, should not ever get here due to validate_serial_number routine
                return None

            c_int = valid.index(c) + 1
            c_int *= (N ** idx)

            num += c_int
        
        return num

    def increment_serial_number(self, serial: str):
        """Find the next serial number in the required sequence

        e.g.
        111 -> 112
        AAA -> AAB
        AAZ -> AB1
        AB9 -> ABA
        ABZ -> AC1
        DQX -> DQY
        ZZZ -> AAAA
        """

        valid = self.valid_chars()
        N = len(valid)

        if serial in [None, '']:
            # Provide an initial condition
            return valid[0] * 3

        output = ''
        rollover = False

        for c in serial[::-1]:
            # If any character is invalid, return immediately
            if c not in valid:
                return None
            
            idx = valid.index(c)

            if not rollover:
                if idx >= N - 1:
                    idx = 0
                else:
                    rollover = True
                    idx += 1
            
            output = valid[idx] + output
        
        # If we get to the end of the sequence without incrementing, add a new character
        if not rollover:
            output = valid[0] + output
        
        return output
