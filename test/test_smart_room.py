import unittest
from idlelib.autocomplete import TRY_A

import mock.GPIO as GPIO
from unittest.mock import patch, Mock, PropertyMock

from mock.adafruit_bmp280 import Adafruit_BMP280_I2C
from src.smart_room import SmartRoom


class TestSmartRoom(unittest.TestCase):

    @patch.object(GPIO, "input")
    def test_check_room_occupancy(self, mock_infrared: Mock):
        smart_room = SmartRoom()
        mock_infrared.return_value = True
        result = smart_room.check_room_occupancy()
        self.assertTrue(result)

    @patch.object(GPIO, "input")
    def test_check_enough_light(self, mock_photoresistor: Mock):
        smart_room = SmartRoom()
        mock_photoresistor.return_value = False
        result = smart_room.check_enough_light()
        mock_photoresistor.assert_called_with(smart_room.PHOTO_PIN)
        self.assertFalse(result)

    @patch.object(GPIO, "output")
    @patch.object(SmartRoom, "check_enough_light")
    @patch.object(SmartRoom, "check_room_occupancy")
    def test_manage_light_level_room_occupied_and_no_enough_light(self, mock_infrared: Mock, mock_photoresistor: Mock, led: Mock):
        smart_room = SmartRoom()
        mock_infrared.return_value = True
        mock_photoresistor.return_value = False
        smart_room.manage_light_level()
        led.assert_called_with(smart_room.LED_PIN, True)
        self.assertTrue(smart_room.light_on)

    @patch.object(GPIO, "output")
    @patch.object(SmartRoom, "check_enough_light")
    @patch.object(SmartRoom, "check_room_occupancy")
    def test_manage_light_level_room_occupied_with_enough_light(self, mock_infrared: Mock, mock_photoresistor: Mock, mock_led: Mock):
        smart_room = SmartRoom()
        mock_infrared.return_value = True
        mock_photoresistor.return_value = True
        smart_room.manage_light_level()
        mock_led.assert_called_with(smart_room.LED_PIN, False)
        self.assertFalse(smart_room.light_on)

    @patch.object(GPIO, "output")
    @patch.object(SmartRoom, "check_enough_light")
    @patch.object(SmartRoom, "check_room_occupancy")
    def test_manage_light_level_room_empty(self, mock_infrared: Mock, mock_photoresistor: Mock, mock_led: Mock):
        smart_room = SmartRoom()
        mock_infrared.return_value = False
        mock_photoresistor.side_effect = True
        smart_room.manage_light_level()
        mock_led.assert_called_with(smart_room.LED_PIN, False)
        self.assertFalse(smart_room.light_on)


    @patch.object(SmartRoom, "change_servo_angle")
    @patch.object(Adafruit_BMP280_I2C, "temperature", new_callable=PropertyMock)
    def test_window_management_Open_window(self, mock_temp: Mock, mock_servo: Mock):
        smart_room = SmartRoom()
        mock_temp.side_effect = [20, 26]
        mock_servo.return_value = 12
        smart_room.manage_window()
        self.assertTrue(smart_room.window_open)
        self.assertEqual(mock_temp.call_count, 2)
        mock_servo.assert_called_once_with(12)


    @patch.object(SmartRoom, "change_servo_angle")
    @patch.object(Adafruit_BMP280_I2C, "temperature", new_callable=PropertyMock)
    def test_window_management_Close_window(self, mock_temp: Mock, mock_servo: Mock):
        smart_room = SmartRoom()
        mock_temp.side_effect = [30, 26]
        mock_servo.return_value = 2
        smart_room.manage_window()
        self.assertFalse(smart_room.window_open)
        mock_servo.assert_called_with(2)
        self.assertEqual(mock_temp.call_count, 2)

    @patch.object(SmartRoom, "change_servo_angle")
    @patch.object(Adafruit_BMP280_I2C, "temperature", new_callable=PropertyMock)
    def test_window_management_Neutral_temperatures(self, mock_temp: Mock, mock_servo: Mock):
        smart_room = SmartRoom()
        smart_room.window_open = True
        mock_temp.side_effect = [20, 22]
        #mock_servo.return_value = 12
        smart_room.manage_window()
        self.assertTrue(smart_room.window_open)
        self.assertEqual(mock_temp.call_count, 2)
        mock_servo.assert_not_called()

