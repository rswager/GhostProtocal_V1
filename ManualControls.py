from inputs import get_gamepad
from UserIO.KeyBoardInput import *
from  UserIO.XboxController import *
import sys
#Tello Wrapper https://djitellopy.readthedocs.io/en/latest/tello/

# Connect to the Drone( don't have it currently)
def checkGamepad():
    try:
        get_gamepad()
        return True
    except:
        return False


process = True
Hover = False
Landed = True
IoDevice = 'KeyBoard'
UserKeyboard = KeyBoard()
userGamePad = None
MAX_SPEED = 50      # For the Controller
DEFAULT_SPEED = 50  # For the Keyboard

while process:
    time.sleep(.1)
    if IoDevice == 'KeyBoard':
        # Get KeyBoard Response
        Key_W,Key_A,Key_S,Key_D,Key_Up,Key_Down,Key_Left,Key_Right,Key_Escape,Key_Enter,Key_Backspace,Key_Space,Key_Tab = UserKeyboard.read()

        # Check for Program Termination
        if Key_Escape == 1:
            process = False
            del UserKeyboard

        # Check for Input Switch (to xbox controller)
        if Key_Tab == 1:
            del UserKeyboard
            # Check to see if there is a gamepad to connect to
            if checkGamepad():
                # Move over to the Controller
                userGamePad = XboxController()
                print("Changed to Xbox Controller")
                IoDevice = 'Controller'
            else:
                # No Gamepad Detected so we go back to Keyboard
                UserKeyboard = KeyBoard()
                print("NO GAMEPAD-RETURNED TO KEYBOARD")
                Key_Tab = 0
        # Check for Hover
        if Key_Space == 1:
            if Hover:
                Hover = False
            else:
                Hover = True

        # If we are not hovering then we can get the rest of the commands
        left_right = 0
        forward_backward =0
        up_down = 0
        yaw = 0
        if not Hover:
            if Key_Enter != Key_Backspace:
                # Get Takeoff
                if Key_Enter == 1 and Landed:
                    print("TELLO - TAKEOFF")
                    Landed = False
                    Hover = False
                # Get Land
                if Key_Backspace == 1 and not Landed:
                    print("TELLO - LAND")
                    Landed = True
                    Hover = False

                # Get RC Controlls (LeftRight_velocity,ForwardBackwards_Velocity,UpDown_Velocity,Yaw_velocity)
                # Get Remaining Inputs
                if not Landed:
                    # Get Left Right Velocity
                    if Key_A != Key_D:
                        if Key_A == 1:
                            left_right = -DEFAULT_SPEED
                        else:
                            left_right = DEFAULT_SPEED

                    # Get Forward Backward Velocity
                    if Key_W != Key_S:
                        if Key_W == 1:
                            forward_backward = DEFAULT_SPEED
                        else:
                            forward_backward = -DEFAULT_SPEED

                    # Get Up Down Velocity
                    if Key_Up != Key_Down:
                        if Key_Up == 1:
                            up_down = DEFAULT_SPEED
                        else:
                            up_down = -DEFAULT_SPEED

                    # Get Yaw
                    if Key_Left != Key_Right:
                        if Key_Left == 1:
                            yaw = -DEFAULT_SPEED
                        else:
                            yaw = DEFAULT_SPEED

                    print(f'KEYBOAR INPUT {left_right},{forward_backward},{up_down},{yaw}')
        else:
            print(f'HOVER - {left_right},{forward_backward},{up_down},{yaw}')

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