
DEPLOYMENT = False # This variable is to understand whether you are deploying on the actual hardware

import time

try:
    import adafruit_bmp280
    import board
    import RPi.GPIO as GPIO
    DEPLOYMENT = True
except:
    import mock.adafruit_bmp280 as adafruit_bmp280
    import mock.board as board
    import mock.GPIO as GPIO
    import mock.senseair_s8 as senseair_s8

class SmartRoom:
    SERVO_PIN = 31  # Servo motor pin
    INFRARED_PIN = 22  # infrared distance sensor pin
    LED_PIN = 37  # led pin
    PHOTO_PIN = 13  # photoresistor pin
    FAN_PIN = 32  # fan pin
    

    def __init__(self):
        # GPIO pin setup
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.INFRARED_PIN, GPIO.IN)
        GPIO.setup(self.PHOTO_PIN, GPIO.IN)
        GPIO.setup(self.LED_PIN, GPIO.OUT)
        GPIO.setup(self.SERVO_PIN, GPIO.OUT)
        GPIO.setup(self.FAN_PIN, GPIO.OUT)

        i2c = board.I2C()
        self.bmp280_indor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)  # indoor sensor
        self.bmp280_outdoor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x68)  # outdoor sensor

        self.sensair_s8 = senseair_s8.SenseairS8()  # carbon dioxide sensor

        self.servo = GPIO.PWM(self.SERVO_PIN, 50)  # Sets up the pin as a PWM pin
        self.servo.start(2)  # Starts generating PWM on the pin with a duty cycle equal to 2% (corresponding to 0 degree)
        if DEPLOYMENT:  # Sleep only if you are deploying on the actual hardware
            time.sleep(1)  # Waits 1 second so that the servo motor has time to make the turn
        self.servo.ChangeDutyCycle(0)  # Sets duty cycle equal to 0% (corresponding to a low signal)

        self.light_on = False
        self.window_open = False
        self.fan_on = False

    def check_room_occupancy(self) -> bool:
        # Check the infrared sensor to determine room occupancy
        return GPIO.input(self.INFRARED_PIN)


    def check_enough_light(self) -> bool:
        # Check the photoresistor to determine if there is enough light
        return GPIO.input(self.PHOTO_PIN)

    def manage_light_level(self) -> None:
        # Turn on the light if the room is occupied and there is enough light
        room_occupied = self.check_room_occupancy() and ( self.check_enough_light() or not self.check_enough_light())
        if room_occupied:
            self.light_on = True
        else:
            self.light_on = False
        GPIO.output(self.LED_PIN, self.light_on)

    def manage_window(self) -> None:
        # To be implemented
        if 18 <= self.bmp280_indor.temperature  <= 30 and 18 <= self.bmp280_outdoor.temperature <= 30 :
            if self.bmp280_indor.temperature < self.bmp280_outdoor.temperature - 2:
                self.window_open = True
            elif self.bmp280_indor.temperature > self.bmp280_outdoor.temperature + 2:
                self.window_open = False
        else:
            self.window_open = False

    def monitor_air_quality(self) -> None:
        # To be implemented
        pass

    def change_servo_angle(self, duty_cycle):
        """
        Changes the servo motor's angle by passing it the corresponding PWM duty cycle
        :param duty_cycle: the width of the PWM duty cycle (it's a percentage value)
        """
        self.servo.ChangeDutyCycle(duty_cycle)  # Changes the duty cycle
        if DEPLOYMENT:  # Sleep only if you are deploying on the actual hardware
            time.sleep(1)
        self.servo.ChangeDutyCycle(0)  # Set duty cycle equal to 0%


class SmartRoomError(Exception):
    pass