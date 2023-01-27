# -*- coding: utf-8 -*-

import setuptools

from hexserial.version import INVENTREE_HEX_PLUGIN_VERSION


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setuptools.setup(
    name="inventree-hex-serial",

    version=INVENTREE_HEX_PLUGIN_VERSION,

    author="Oliver Walters",

    author_email="oliver.henry.walters@gmail.com",

    description="Hexadecimal serial number generation plugin for InvenTree",

    long_description=long_description,

    long_description_content_type='text/markdown',

    keywords="inventree inventory serial numbers",

    url="https://github.com/inventree/inventree",

    license="MIT",

    packages=setuptools.find_packages(),

    install_requires=[
    ],

    setup_requires=[
        "wheel",
        "twine",
    ],

    python_requires=">=3.7",

    entry_points={
        "inventree_plugins": [
            "HexSerialNumber = hexserial.hex_serial:HexSerialNumberPlugin",
        ]
    },
)
