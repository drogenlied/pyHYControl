#!/usr/bin/env python3

import setuptools

version_string = '0.0.1a'

setuptools.setup(
    name = 'pyHYControl',
    license = 'GPLv3',
    version = version_string,
    author = 'Jan M. Binder',
    author_email = 'jan-git@nlogn.org',
    url = 'https://github.com/drogenlied/pyHYControl',
    download_url = 'https://github.com/drogenlied/pyHYControl/archive/v{0}.tar.gz'.format(version_string),
    description = 'A python package and programme to control the Huanyang Variable Frequency Drive'
                  ' for three-phase motors.'
                  'The datashet for this device claims that it can communicate via Modbus, but '
                  'in reality, the only similarities are the RTU/ASCII encoding and the '
                  'address byte. The rest of the protocol works differently.',
    keywords = 'Huanyang VFD RS485 Modbus',

    packages = setuptools.find_packages(),
    install_requires= ['crcmod>=1.7', 'pyyaml>=3.11', 'pyserial>=3.0'],

    zip_safe = False,
    package_data = {
        'hycontrol': ['registers.yml'],
        },

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',

        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Communications',
    ],
)

