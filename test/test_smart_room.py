import unittest
import mock.GPIO as GPIO
from unittest.mock import patch, PropertyMock
from unittest.mock import Mock

from mock.adafruit_bmp280 import Adafruit_BMP280_I2C
from src.smart_room import SmartRoom
from mock.senseair_s8 import SenseairS8


class TestSmartRoom(unittest.TestCase):

    @patch.object(GPIO, "input")
    def test_check_room_occupancy(self, infrared: Mock):
        smart_room = SmartRoom()
        infrared.return_value = True
        result = smart_room.check_room_occupancy()
        self.assertEqual(result, True)

    @patch.object(GPIO, "input")
    def test_check_enough_light(self, light: Mock):
        smart_room = SmartRoom()
        light.return_value = False
        result = smart_room.check_enough_light()
        self.assertEqual(result, False)

    @patch.object(GPIO, "input")
    @patch.object(GPIO, "input")
    @patch.object(GPIO, "output")
    def test_manage_light_level(self, lightbulb: Mock, light: Mock, infrared: Mock ):
        smart_room = SmartRoom()
        infrared.return_value = True
        light.return_value = True

        smart_room.manage_light_level()

        self.assertTrue(smart_room.light_on)