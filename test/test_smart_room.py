import unittest
import mock.GPIO as GPIO
from unittest.mock import patch, PropertyMock
from unittest.mock import Mock

from mock.adafruit_bmp280 import Adafruit_BMP280_I2C
from src.smart_room import SmartRoom
from mock.senseair_s8 import SenseairS8


class TestSmartRoom(unittest.TestCase):

    @patch.object(GPIO, "input")
    def test_check_room_occupancy(self, value: Mock):
        smart_room = SmartRoom()
        value.return_value = True
        result = smart_room.check_room_occupancy()
        self.assertEqual(result, True)

    @patch.object(GPIO, "input")
    def test_check_enough_light(self, light: Mock):
        smart_room = SmartRoom()
        light.return_value = False
        result = smart_room.check_enough_light()
        self.assertEqual(result, False)