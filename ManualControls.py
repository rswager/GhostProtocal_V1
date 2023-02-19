from inputs import get_gamepad
from UserIO.KeyBoardInput import *
from  UserIO.XboxController import *

#Connect to the Drone( don't have it currently)
def checkGamepad():
    try:
        print("GAME PAD ACCESSED: ", get_gamepad())
        return True
    except:
        print("NO GAMEPAD!")
        return False


process = True
Hold = False
IoDevice = 'KeyBoard'
UserKeyboard = KeyBoard()
userGamePad = None
MAX_SPEED = 50 #For the Controller
DEFAULT_SPEED = 50 #For the Keyboard

while process:
    if IoDevice == 'KeyBoard':
        Key_W,Key_A,Key_S,Key_D,Key_Up,Key_Down,Key_Left,Key_Right,Key_Escape,Key_Enter,Key_Backspace,Key_Space,Key_Tab = UserKeyboard.read()

        if Key_Escape == 1:
            process = False
            del UserKeyboard
            break
        if Key_Tab == 1 and checkGamepad():
            #Move over to the Controller
            del UserKeyboard
            userGamePad = XboxController()
            print("Changed to Xbox Controller")
            IoDevice = 'Controller'
        else:
            Key_Tab = 0
    elif IoDevice == 'Controller':
        LeftJoystickY, LeftJoystickX, RightJoystickX, LeftBumper, RightBumper, Y_Button, A_Button, X_Button, B_Button, Start_Button = userGamePad.read()

        if X_Button == 1:
            process = False
            del userGamePad
            break
        if B_Button == 1:
            del userGamePad
            #Move Over to the Keybaord
            UserKeyboard = KeyBoard()
            print("Change to KeyBoard")
            IoDevice = 'KeyBoard'
print("Program Closed")
quit()