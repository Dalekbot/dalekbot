
start the program with 

```bash
$ python3 main.py
```
args get passed to ___dalek_settings___ then we call the following 
```python
def maincontrol():                  # Main Control Loop
    controller.use(dalek_settings,dalek_sounds)
```

 We are now in the ___use___ function block of the controller code.

 We are in ps3_ControllerMode=1 by default.

 ```python
  # The Main Mode we are in
  # 1 Drive mode
  # 2 Challenge Select Mode
  # 3 Exterminate Mode this mode does nothing so is standby and disables the paddles on
  #   the controller
 ```
 The PS3 button, controls what mode we are in, each press iterates through the modes.

 If you select Mode 2 you get the ui on the stout/scrolphat to choose the challange to select.

 You will need to press the select button to select and start the challange.
 

 When you have finished the challenge you drop back to the ___use___ block on the controller code and go into ps3_ControllerMode=3 mode and wait for the PS3 button to be pressed