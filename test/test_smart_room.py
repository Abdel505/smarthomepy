import unittest
import mock.GPIO as GPIO
from unittest.mock import patch, Mock

from src.smart_room import SmartRoom


class TestSmartRoom(unittest.TestCase):

    @patch.object(GPIO, "input")
    def test_check_room_occupancy(self, infrared: Mock):
        smart_room = SmartRoom()
        infrared.return_value = True
        result = smart_room.check_room_occupancy()
        self.assertTrue(result)

    @patch.object(GPIO, "input")
    def test_check_enough_light(self, light: Mock):
        smart_room = SmartRoom()
        light.return_value = False
        result = smart_room.check_enough_light()
        self.assertFalse(result)

    @patch.object(GPIO, "output")
    @patch.object(SmartRoom, "check_enough_light")
    @patch.object(SmartRoom, "check_room_occupancy")
    def test_manage_light_level(self, infrared: Mock, photo: Mock, led: Mock):
        smart_room = SmartRoom()
        infrared.return_value = True
        photo.return_value = True
        smart_room.manage_light_level()
        led.assert_called_with(smart_room.LED_PIN, True)
        self.assertTrue(smart_room.light_on)
