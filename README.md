## DalekBot code
### files you will need:

see requirements.txt for pip packages needed

version 0.1


this readme is out of date due to name changes and refactoring of the code.

joystick.py runs on it's own at the moment this should work on your bot.
basic.py is just for trying out things
test.py is end to end tests this MUST work on all bots.

DalekPrint() takes one or two parameters the first one gets printed to stout and the other
gets sent to the onboard device in your case, the scrollphat I intend to use one of my lcd screens.

All the challenge_xxx files are the files that need to be changed so that DalekV2main works, and will be
added back once updated.

scrollphat.py and cwild.py are just so my code works. You can just delete them and use the proper one.


The joystick.py should work all on its own, and is the main file for driving the bot. it uses Tank mode with the two paddles. the D pad uses the left and right to call the DalekTurn() on the autoDrive module. All the button numbers are printed to debug when they are pressed.

The DalekSpi.py is the file for getting all the data from the Arduino and can be imported into any module. Uses the default pins on both the Raspberry pi and the Arduino. Remember that connecting up a 5v Arduino to the RPI will probably damage the RPI! use a 3.3v one or a level shifter.


autoDrive.py is  the file that uses the mag to turn to a given heading, and can be run directly. uncomment the lines at the end of the file to  see what it can do. At the top of the file there are a list of settings that can be edited depending on the surface you are driving on.
  
  

things to look at:

https://pypi.python.org/pypi/inputs used to capture keyboard events.




 