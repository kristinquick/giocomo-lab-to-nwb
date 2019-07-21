from setuptools import setup

setup(
    name='giocomo',
    version='0.1dev',
    description='tool to convert giocomo matlab data into NWB:N format',
    author='Kristin Quick',
    author_email='kristin@scenda.io',
    packages=['giocomo'],
    install_requires=['pynwb','numpy','scipy','hdf5storage','datetime','pytz','uuid']
)