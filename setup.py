# -*- coding: utf-8 -*-

import setuptools

from hexserial.version import INVENTREE_HEX_PLUGIN_VERSION


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setuptools.setup(
    name="inventree-hex-serials",

    version=INVENTREE_HEX_PLUGIN_VERSION,

    author="Oliver Walters",

    author_email="oliver.henry.walters@gmail.com",

    description="Hexadecimal serial number generation plugin for InvenTree",

    long_description=long_description,

    long_description_content_type='text/markdown',

    keywords="inventree inventory serial numbers",

    url="https://github.com/SchrodingersGat/inventree-hex-serials/",

    license="MIT",

    packages=setuptools.find_packages(),

    install_requires=[
    ],

    setup_requires=[
        "wheel",
        "twine",
    ],

    python_requires=">=3.8",

    entry_points={
        "inventree_plugins": [
            "HexSerialNumbers = hexserial.hex_serial:HexSerialNumberPlugin",
        ]
    },
)
