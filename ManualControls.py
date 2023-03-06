from inputs import get_gamepad
from UserIO.KeyBoardInput import *
from UserIO.XboxController import *
from VideoCamera.DroneCamera import *
from djitellopy import Tello
import sys,cv2
import multiprocessing as mp
# Tello Wrapper https://djitellopy.readthedocs.io/en/latest/tello/


# Connect to the Drone( don't have it currently)
def check_gamepad():
    try:
        get_gamepad()
        return True
    except:
        return False


# MAIN PROGRAM STARTS HERE
if __name__ == "__main__":
    deBug = False

    if not deBug:
        loopSpeedSeconds = 1
        quadDrone = Tello()
        try:
            print("Attempting to connect to drone!")
            quadDrone.connect()
        except:
            print("Couldn't Connect to the Drone!")
            sys.exit()

        print("Connected, Testing Connection!")
        try:
            print(quadDrone.query_battery())
        except:
            print("Test Failed")
            sys.exit()

        print("Connection SUCCESSFUL...Moving to Get User Input")
    else:
        loopSpeedSeconds = .5
        print("In Debug Mode")

    process = True
    Hovering = False
    Streaming = False
    Landed = True
    IoDevice = 'KeyBoard'
    UserKeyboard = KeyBoard()
    userGamePad = None
    SteamProcess = None     # For Controlling the Stream
    MAX_SPEED = 100      # For the Controller
    DEFAULT_SPEED = 50  # For the Keyboard

    while process:
        if Streaming:
            img = quadDrone.get_frame_read().frame
            img = cv2.resize(img, (360, 240))
            cv2.imshow("Image", img)
            cv2.waitKey(loopSpeedSeconds)

        if IoDevice == 'KeyBoard':
            # Get KeyBoard Response
            Key_W, Key_A, Key_S, Key_D, Key_Up, Key_Down, Key_Left,\
                Key_Right, Key_Escape, Key_Enter, Key_Backspace,\
                Key_Space, Key_Tab, Key_C = UserKeyboard.read()

            # Check for Program Termination
            if Key_Escape == 1:
                process = False
                if Streaming:
                    quadDrone.streamoff()
                if not Landed:
                    if not deBug:
                        quadDrone.land()
                    print("Landing Drone")
                del UserKeyboard
            if Key_C == 1:
                if Streaming:
                    # Stop Streaming
                    Streaming = False
                    quadDrone.streamoff()
                    cv2.destroyAllWindows()
                else:
                    # Start Steaming
                    Streaming = True
                    quadDrone.streamon()
            # If we are not Terminating then we are good to continue
            else:
                # If we are landed then we only want to take off or check for input change
                if Landed:
                    # Check for Input Switch (to xbox controller)
                    if Key_Tab == 1:
                        # Check to see if there is a gamepad to connect to
                        if check_gamepad():
                            # Move over to the Controller
                            del UserKeyboard
                            userGamePad = XboxController()
                            print("Changed to Xbox Controller")
                            IoDevice = 'Controller'
                        else:
                            # No Gamepad Detected so we go back to Keyboard
                            print("NO GAMEPAD-RETURNED TO KEYBOARD")
                            Key_Tab = 0
                    # Check for takeoff
                    if Key_Enter == 1 and (Key_Enter != Key_Backspace):
                        print("Takeoff)")
                        if not deBug:
                            quadDrone.takeoff()
                        Landed = False
                        Hovering = False
                # If not landed:
                else:
                    # Check to see if we are landing
                    if Key_Backspace == 1 and (Key_Enter != Key_Backspace):
                        print("LAND")
                        if not deBug:
                            quadDrone.land()
                        Landed = True
                        Hovering = False
                    else:
                        left_right = 0
                        forward_backward = 0
                        up_down = 0
                        yaw = 0

                        # Check for Hover
                        if Key_Space == 1:
                            if Hovering:
                                Hovering = False
                            else:
                                Hovering = True
                        # If we are not hovering then we can get the rest of the commands
                        if not Hovering:
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
                            if deBug:
                                print(f'KEYBOAR INPUT {left_right},{forward_backward},{up_down},{yaw}')
                            else:
                                # Send Movement
                                quadDrone.send_rc_control(left_right, forward_backward, up_down, yaw)
                        else:
                            if deBug:
                                print(f'HOVER - {left_right},{forward_backward},{up_down},{yaw}')
                            else:
                                quadDrone.send_rc_control(left_right, forward_backward, up_down, yaw)
        elif IoDevice == 'Controller':
            LeftJoystickY, LeftJoystickX, RightJoystickX, \
                LeftBumper, RightBumper, Y_Button, A_Button, \
                X_Button, B_Button, Start_Button, Select_Button = userGamePad.read()
            # Check for Program Termination
            if X_Button == 1:
                process = False
                if Streaming:
                    quadDrone.streamoff()
                if not Landed:
                    if not deBug:
                        quadDrone.land()
                    print("Landing Drone")
                del userGamePad
            if Select_Button == 1:
                if Streaming:
                    # Stop Streaming
                    Streaming = False
                    SteamProcess.terminate()
                else:
                    # Start Steaming
                    Streaming = True
                    SteamProcess = mp.Process(target=stream_tello, args=(quadDrone))
                    SteamProcess.start()

            # If we are not Terminating then we are good to continue
            else:
                # If we are landed then we only want to take off or check for input change
                if Landed:
                    # Check for Input Switch (to keyboard)
                    if B_Button == 1:
                        del userGamePad
                        # Move Over to the Keyboard
                        UserKeyboard = KeyBoard()
                        print("Change to KeyBoard")
                        IoDevice = 'KeyBoard'
                    # Check for takeoff
                    if A_Button == 1 and (A_Button != Y_Button):
                        print("Take off")
                        if not deBug:
                            quadDrone.takeoff()
                        Landed = False
                        Hovering = False
                # If not landed:
                else:
                    # Check to see if we are landing
                    if Y_Button == 1 and (Y_Button != A_Button):
                        print("LAND")
                        if not deBug:
                            quadDrone.land()
                        Landed = True
                        Hovering = False
                    else:
                        left_right = 0
                        forward_backward = 0
                        up_down = 0
                        yaw = 0

                        # Check for Hover
                        if Start_Button == 1:
                            if Hovering:
                                Hovering = False
                            else:
                                Hovering = True
                        # If we are not hovering then we can get the rest of the commands
                        if not Hovering:
                            # Get Left Right Velocity
                            left_right = int(LeftJoystickX * MAX_SPEED)
                            # Get Forward Backward Velocity
                            forward_backward = int(LeftJoystickY * MAX_SPEED)
                            # Get Up Down Velocity
                            if LeftBumper != RightBumper:
                                if LeftBumper == 1:
                                    up_down = -DEFAULT_SPEED
                                else:
                                    up_down = DEFAULT_SPEED
                            # Get Yaw
                            yaw = int(RightJoystickX * MAX_SPEED)
                            if deBug:
                                print(f'KEYBOARD INPUT {left_right},{forward_backward},{up_down},{yaw}')
                            else:
                                # Send Movement
                                quadDrone.send_rc_control(left_right, forward_backward, up_down, yaw)
                        else:
                            if deBug:
                                print(f'HOVER - {left_right},{forward_backward},{up_down},{yaw}')
                            else:
                                quadDrone.send_rc_control(left_right, forward_backward, up_down, yaw)
    if not deBug:
        quadDrone.end()
    print("Program Closed")
    sys.exit()
