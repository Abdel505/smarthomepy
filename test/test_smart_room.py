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

    """@patch('src.smart_room.adafruit_bmp280.Adafruit_BMP280_I2C')
    def test_manage_window_opens_when_colder(self, mockBmp280Class: Mock):
        # Create two mocks, one for indoor, one for outdoor
        mock_indoor_sensor = Mock()
        mock_outdoor_sensor = Mock()

        # Set the side_effect to return our mocks when the class is instantiated
        MockBmp280Class.side_effect = [mock_indoor_sensor, mock_outdoor_sensor]

        # Configure the temperature for each sensor mock
        type(mock_indoor_sensor).temperature = PropertyMock(return_value=20)  # Indoor is 20
        type(mock_outdoor_sensor).temperature = PropertyMock(return_value=23)  # Outdoor is 23

        # Run the code
        smart_room = SmartRoom()
        smart_room.manage_window()

        # Assert that the window was opened
        self.assertTrue(smart_room.window_open)"""


