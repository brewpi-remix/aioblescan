#!/usr/bin/python3

from setuptools import setup

version="0.2.5"

setup(name='aioblescan',
    packages=['aioblescan', 'aioblescan.plugins'],
    version=version,
    author='Lee Bussy',
    author_email='lee@bussy.org',
    description='Scanning B:Eacons for Tilt supporting BrewPi.',
    url='https://github.com/brewpi-remix/aioblescan',
    download_url='https://github.com/brewpi-remix/aioblescan.git',
    keywords = ['bluetooth', 'advertising', 'hci', 'ble'],
    license='MIT',
    install_requires=[],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7'
    ])
