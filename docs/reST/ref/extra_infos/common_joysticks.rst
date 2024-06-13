Common joysticks
================

This is a non exhaustive list of common joystick frequently used by pygame users.

Nintendo Switch Left Joy-Con (pygame 2.x)
*****************************************

The Nintendo Switch Left Joy-Con has 4 axes, 11 buttons, and 0 hats. The values for the 4 axes never change.
The controller is recognized as "Wireless Gamepad".
After SDL 2.24.0, The controller is recognized as "Nintendo Switch Joy-Con (L)".


* **Buttons**::

                    After SDL 2.24.0         Before SDL 2.24.0
    D-pad Up            Button 2                  Button 3
    D-pad Down          Button 1                  Button 0
    D-pad Left          Button 3                  Button 2
    D-pad Right         Button 0                  Button 1
    SL                  Button 9                  Button 4
    SR                  Button 10                 Button 5
    -                   Button 6                  Button 8
    Stick In            Button 7                  Button 10
    Capture             Button 5                  Button 13
    L                   Button 17                 Button 14
    ZL                  Button 19                 Button 15

Reference : D-pad Up points toward SL and SR buttons. 

* **Hat/JoyStick**::

    Down -> Up      -    Axis 1                    Axis Y
    Left -> Right   -    Axis 0                    Axis X


Nintendo Switch Right Joy-Con (pygame 2.x)
******************************************

The Nintendo Switch Right Joy-Con has 4 axes, 11 buttons, and 0 hats. The values for the 4 axes never change.
The controller is recognized as "Wireless Gamepad".
After SDL 2.24.0, The controller is recognized as "Nintendo Switch Joy-Con (R)".

* **Buttons**::

                  After SDL 2.24.0         Before SDL 2.24.0
    A Button          Button 1                 Button 0
    B Button          Button 3                 Button 2
    X Button          Button 0                 Button 1
    Y Button          Button 2                 Button 3
    SL                Button 9                 Button 4
    SR                Button 10                Button 5
    +                 Button 6                 Button 9
    Stick In          Button 7                 Button 11
    Home              Button 5                 Button 12
    R                 Button 16                Button 14
    ZR                Button 18                Button 15

* **Hat/JoyStick**::

    Down -> Up      -  Axis 1                   Axis Y
    Left -> Right   -  Axis 0                   Axis X

Nintendo Switch Left/Right Joy-Con (after SDL **2.24.0**)
*********************************************************
This device is created, if Nintendo Switch Joy-con Left and Nintendo Switch Joy-con Right are connected (these two devices are removed).
The Nintendo Switch Left/Right Joy-Con has 6 axes, 20 buttons, and 0 hats. The values for the 6 axes never change.
The controller is recognized as "Nintendo Switch Joy-Con (L/R)".

* **Left Stick**::

    Left -> Right   - Axis 0
    Up -> Down      - Axis 1

* **Right Stick**::

    Left -> Right   - Axis 2
    Up -> Down      - Axis 3

* **Buttons**::

    A Button        - Button 0
    B Button        - Button 1
    X Button        - Button 2
    Y Button        - Button 3
    - Button        - Button 4
    Home Button     - Button 5
    + Button        - Button 6
    ZL              - Button ? Missing
    ZR              - Button ? Missing
    L. Stick In     - Button 9
    R. Stick In     - Button 10
    D-pad Up        - Button 11
    D-pad Down      - Button 12
    D-pad Left      - Button 13
    D-pad Right     - Button 14
    Capture Button  - Button 15
    Right SR        - Button 16
    Left SL         - Button 17
    Right SL        - Button 18
    Left SR         - Button 19

Nintendo Switch Pro Controller (pygame 2.x)
*******************************************

The Nintendo Switch Pro Controller has 6 axes, 16 buttons, and 0 hats.
The controller is recognized as "Nintendo Switch Pro Controller".


* **Left Stick**::

    Left -> Right   - Axis 0
    Up -> Down      - Axis 1

* **Right Stick**::

    Left -> Right   - Axis 2
    Up -> Down      - Axis 3

* **Left Trigger**::

    Out -> In       - Axis 4

* **Right Trigger**::

    Out -> In       - Axis 5

* **Buttons**::

    A Button        - Button 0
    B Button        - Button 1
    X Button        - Button 2
    Y Button        - Button 3
    - Button        - Button 4
    Home Button     - Button 5
    + Button        - Button 6
    L. Stick In     - Button 7
    R. Stick In     - Button 8
    Left Bumper     - Button 9
    Right Bumper    - Button 10
    D-pad Up        - Button 11
    D-pad Down      - Button 12
    D-pad Left      - Button 13
    D-pad Right     - Button 14
    Capture Button  - Button 15


XBox 360 Controller (pygame 2.x)
********************************

The Xbox 360 controller mapping has 6 axes, 11 buttons and 1 hat.
The controller is recognized as "Xbox 360 Controller".

* **Left Stick**::

    Left -> Right   - Axis 0
    Up   -> Down    - Axis 1

* **Right Stick**::

    Left -> Right   - Axis 3
    Up   -> Down    - Axis 4

* **Left Trigger**::

    Out -> In       - Axis 2

* **Right Trigger**::

    Out -> In       - Axis 5

* **Buttons**::

    A Button        - Button 0
    B Button        - Button 1
    X Button        - Button 2
    Y Button        - Button 3
    Left Bumper     - Button 4
    Right Bumper    - Button 5
    Back Button     - Button 6
    Start Button    - Button 7
    L. Stick In     - Button 8
    R. Stick In     - Button 9
    Guide Button    - Button 10

* **Hat/D-pad**::

    Down -> Up      - Y Axis
    Left -> Right   - X Axis


Playstation 4 Controller (pygame 2.x)
*************************************

The PlayStation 4 controller mapping has 6 axes and 16 buttons.
The controller is recognized as "PS4 Controller".

* **Left Stick**::

    Left -> Right   - Axis 0
    Up   -> Down    - Axis 1

* **Right Stick**::

    Left -> Right   - Axis 2
    Up   -> Down    - Axis 3

* **Left Trigger**::

    Out -> In       - Axis 4

* **Right Trigger**::

    Out -> In       - Axis 5

* **Buttons**::

    Cross Button    - Button 0
    Circle Button   - Button 1
    Square Button   - Button 2
    Triangle Button - Button 3
    Share Button    - Button 4
    PS Button       - Button 5
    Options Button  - Button 6
    L. Stick In     - Button 7
    R. Stick In     - Button 8
    Left Bumper     - Button 9
    Right Bumper    - Button 10
    D-pad Up        - Button 11
    D-pad Down      - Button 12
    D-pad Left      - Button 13
    D-pad Right     - Button 14
    Touch Pad Click - Button 15


XBox 360 Controller (pygame 1.x)
********************************

The Xbox 360 controller mapping has 5 axes, 10 buttons, and 1 hat.
The controller is recognized as "Controller (XBOX 360 For Windows)".

* **Left Stick**::

    Left -> Right   - Axis 0
    Up   -> Down    - Axis 1

* **Right Stick**::

    Left -> Right   - Axis 4
    Up   -> Down    - Axis 3

* **Left Trigger & Right Trigger**::

    RT -> LT        - Axis 2

* **Buttons**::

    A Button        - Button 0
    B Button        - Button 1
    X Button        - Button 2
    Y Button        - Button 3
    Left Bumper     - Button 4
    Right Bumper    - Button 5
    Back Button     - Button 6
    Start Button    - Button 7
    L. Stick In     - Button 8
    R. Stick In     - Button 9

* **Hat/D-pad**::

    Down -> Up      - Y Axis
    Left -> Right   - X Axis


Playstation 4 Controller (pygame 1.x)
*************************************

The PlayStation 4 controller mapping has 6 axes, 14 buttons, and 1 hat.
The controller is recognized as "Wireless Controller".

* **Left Stick**::

    Left -> Right   - Axis 0
    Up   -> Down    - Axis 1

* **Right Stick**::

    Left -> Right   - Axis 2
    Up   -> Down    - Axis 3

* **Left Trigger**::

    Out -> In       - Axis 5

* **Right Trigger**::

    Out -> In       - Axis 4

* **Buttons**::

    Cross Button    - Button 0
    Circle Button   - Button 1
    Square Button   - Button 2
    Triangle Button - Button 3
    Left Bumper     - Button 4
    Right Bumper    - Button 5
    L. Trigger(Full)- Button 6
    R. Trigger(Full)- Button 7
    Share Button    - Button 8
    Options Button  - Button 9
    L. Stick In     - Button 10
    R. Stick In     - Button 11
    PS Button       - Button 12
    Touch Pad Click - Button 13

* **Hat/D-pad**::

    Down -> Up      - Y Axis
    Left -> Right   - X Axis