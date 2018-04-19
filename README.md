Extract P-codes from iTOS
=========================

(Started 2018-04 by David Megginson)

Python3 script to extract humanitarian P-code data from the iTOS JSON API into a simple CSV spreadsheet with HXL hashtags.

# Installation

    pip install -r requirements.txt

# Usage

    python extract-itos-pcodes.py {country} {level}

* {country} an ISO3 country code, like "SEN" for Senegal
* {level} the administrative level to display, where 1 is country, 2 is admin level 1, etc.

# License

This code is released into the Public Domain, and comes with NO WARRANTY.