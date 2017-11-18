# Playstation 3 mappings

These are the mappings for my ps3 controller on the raspberry pi.

Use the following command to access the values.

     jstest  /dev/input/js1

## Left Stem
    Axes 0: left/Right
    Axes 1: Up/down
    Button: 1

## Right Stem

    Axes 2: left/Right
    Axes 3:  up/down
    Button: 2

## Left Pad controls

    Button| BTN  | AXIS
    U       4      8
    R       5      9
    D       6      10
    L       7      -

## Right  controls

   Symbol   | Button| BTN  | AXIS
   Triangle     U      12     16
   Circle       R      13     17
   Cross        D      14     18
   Square       L      15     19

## Top buttons

    Button| BTN  | AXIS
    L1       10     14
    L2       8      12
    R1       11     15
    R2       9      13

## Main Buttons
    Start  3
    PS     16
    Select 0 

## Other

These are the other axis that seem to have values in the output  Acc only works when the controller is moved quickly.

            Axis
    Pitch   23
    Roll    24
    Acc     26
    Other   25




    



