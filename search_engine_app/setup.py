from setuptools import setup
from search_engine_app import __version__


setup(
    name='SearchEngineApp',
    version=__version__,
    packages=['search_engine_app'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
