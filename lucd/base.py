from pathlib import Path
from .utils import Util


class Base(Util):
    def __init__(self):
        self._profile: Path = None
        self._headless: bool = False
        self._mute: bool = False

    @property
    def profile(self):
        return self._profile

    @profile.setter
    def profile(self, path: Path):
        self._profile = path

    @property
    def headless(self):
        return self._headless

    @headless.setter
    def headless(self, value: bool):
        self._headless = value

    @property
    def mute(self):
        return self._mute

    @mute.setter
    def mute(self, value: bool):
        self._mute = value
