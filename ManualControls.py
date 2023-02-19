from inputs import get_gamepad
from UserIO.KeyBoardInput import *
from  UserIO.XboxController import *
import sys

# Connect to the Drone( don't have it currently)
def checkGamepad():
    try:
        get_gamepad()
        return True
    except:
        return False


process = True
Hold = False
IoDevice = 'KeyBoard'
UserKeyboard = KeyBoard()
userGamePad = None
MAX_SPEED = 50      # For the Controller
DEFAULT_SPEED = 50  # For the Keyboard

while process:
    print("MAIN LOOP-",process)
    time.sleep(1)
    if IoDevice == 'KeyBoard':
        Key_W,Key_A,Key_S,Key_D,Key_Up,Key_Down,Key_Left,Key_Right,Key_Escape,Key_Enter,Key_Backspace,Key_Space,Key_Tab = UserKeyboard.read()

        # Check for Program Termination
        if Key_Escape == 1:
            process = False
            del UserKeyboard
        # Check for Input Switch
        if Key_Tab == 1:
            del UserKeyboard
            if checkGamepad():
                # Move over to the Controller
                userGamePad = XboxController()
                print("Changed to Xbox Controller")
                IoDevice = 'Controller'
            else:
                UserKeyboard = KeyBoard()
                print("NO GAMEPAD-RETURNED TO KEYBOARD")
                Key_Tab = 0
        # Check for Hover (lock other inputs until hover is disabled)
        

    elif IoDevice == 'Controller':
        LeftJoystickY, LeftJoystickX, RightJoystickX, LeftBumper, RightBumper, Y_Button, A_Button, X_Button, B_Button, Start_Button = userGamePad.read()

        if X_Button == 1:
            process = False
            del userGamePad
        if B_Button == 1:
            del userGamePad
            # Move Over to the Keyboard
            UserKeyboard = KeyBoard()
            print("Change to KeyBoard")
            IoDevice = 'KeyBoard'
print("Program Closed")
quit()