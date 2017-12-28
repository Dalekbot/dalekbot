## DalekBot code

First open the  DalekV2Drive and comment/uncomment/change the  pin numbers for your setup, there are a few changes to Cosma's code mainly tank mode for the joystick paddles and  comment out of the print statements.

The joystick.py should work all on its own, and is the main file for driving the bot. it uses Tank mode with the two paddles. the D pad uses the left and right to call the DalekTurn() on the autoDrive module. All the button numbers are printed to debug when they are pressed.

The DalekSpi.py is the file for getting all the data from the Arduino and can be imported into any module. Uses the default pins on both the Raspberry pi and the Arduino. Remember that connecting up a 5v Arduino to the RPI will probably damage the RPI! use a 3.3v one or a level shifter.

autoDrive.py is  the file that uses the mag to turn to a given heading, and can be run directly. uncomment the lines at the end of the file to  see what it can do. At the top of the file there are a list of settings that can be edited depending on the surface you are driving on.









