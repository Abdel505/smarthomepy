# smarthomepy
_smarthomepy_ is system to manage a smart room in a house. An infrared distance sensor is placed on the ceiling of the room and is used to determine whether someone is inside the room or not. Based on both the occupancy of the room and the light measurement obtained by a photoresistor, _smarthomepy_ turns on/off a smart lightbulb. Furthermore, the room has a window on one side, equipped with a servo motor to open/close it based on the delta between the temperatures measured by two temperature sensors, one indoor and one outdoor (i.e., inside and outside the room). Finally, _smarthomepy_ checks the CO2 level inside the room through a carbon dioxide sensor and then turns on/off the switch of an exhaust fan.

To recap, the system includes the following sensors and actuators:
* An infrared distance sensor located on the ceiling of the room.
* A smart lightbulb.
* A photoresistor sensor to measure the light level inside the room.
* A servo motor to open/close the window.
* Two temperature sensors, one indoor and one outdoor, used in combination with the servo motor to open/close the window.
* A carbon dioxide sensor to check the CO2 level inside the room.
* An exhaust fan to control the CO2 level inside the room.
  
The communication between the main board and the other components happens through GPIO pins. The communication is already configured in the BOARD mode (i.e., GPIO pins are referred to by their physical number on the board).

## Instructions for You
* FORK this project and make sure your forked repository is PUBLIC. Then, IMPORT the forked project into PyCharm.
* If you BELONG to the GAI4-TDD group, you are asked to develop _smarthomepy_ by following TDD WITH the support of GAI4-TDD. If you do NOT BELONG to the GAI4-TDD group, you are asked to develop _smarthomepy_ by following TDD WITHOUT the support of GAI4-TDD.
* You DO NOT need to develop a GUI.
* You CANNOT change the signature of the provided methods, move the provided methods to other classes, or change the name of the provided classes. However, you CAN add fields, methods (e.g., methods used by tests to set up the fixture or methods used by the provided methods), or even classes (including other test classes), as long as you comply with the provided API.
* You CAN use the internet to consult Python APIs or QA sites (e.g., StackOverflow).
* You CANNOT use AI tools (e.g., ChatGPT).
* You CANNOT interact with your colleagues. Work alone and do your best!
* The _smarthomepy_ requirements are divided into a set of USER STORIES, which serve as a to-do list (see the _Issues_ session).
* You should be able to incrementally develop _smarthomepy_ without an upfront comprehension of all its requirements. DO NOT read ahead, and handle the requirements (i.e., specified in the user stories) one at a time in the provided order. Develop _smarthomepy_ by starting from the first story’s requirement. When a story is IMPLEMENTED, move on to the NEXT one. A story is implemented when you are confident that your program correctly implements the functionality stipulated by the story's requirement. This implies that all your test cases for that story and all the test cases for the previous stories pass. You may need to review your program as you progress toward more advanced requirements.
* Each time you end a TDD phase, COMMIT.
* If you need to handle error situations (including situations unspecified by the user stories), throw a ```SmartHomeError```.
* At the end of the task, PUSH your forked project and fill in the following post-questionnaire: [https://forms.gle/EH1wkV3uVT8V9aEr5 ](https://docs.google.com/forms/d/e/1FAIpQLSfbO9SHJBmx0hsagQXTqbOOEjafVKd7VALzSwpcjixVblaA5A/viewform?usp=sharing&ouid=104797422950444435975).

## API Usage
Take some minutes to understand, in broad terms, how the API works (i.e., see the provided classes). If you do not fully understand the API, do not worry because further details will be given in the user stories (see the _Issues_ session).
