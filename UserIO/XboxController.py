from inputs import get_gamepad
import time
import math
import multiprocessing as mp


class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        self.LeftJoystickY = mp.Value('d', 0)
        self.LeftJoystickX = mp.Value('d', 0)
        self.RightJoystickY = mp.Value('d', 0)
        self.RightJoystickX = mp.Value('d', 0)
        self.LeftTrigger = mp.Value('d', 0)
        self.RightTrigger = mp.Value('d', 0)
        self.LeftBumper = mp.Value('i', 0)
        self.RightBumper = mp.Value('i', 0)
        self.A = mp.Value('i', 0)
        self.X = mp.Value('i', 0)
        self.Y = mp.Value('i', 0)
        self.B = mp.Value('i', 0)
        self.LeftThumb = mp.Value('i', 0)
        self.RightThumb = mp.Value('i', 0)
        self.Back = mp.Value('i', 0)
        self.Start = mp.Value('i', 0)
        self.LeftDPad = mp.Value('i', 0)
        self.RightDPad = mp.Value('i', 0)
        self.UpDPad = mp.Value('i', 0)
        self.DownDPad = mp.Value('i', 0)

        self._monitor_process = mp.Process(target=self._monitor_controller, args=())
        self._monitor_process.start()

    def __del__(self):
        self._monitor_process.terminate()

    # return the buttons/triggers that you care about in this methode
    def read(self):
        return self.LeftJoystickY.value, self.LeftJoystickX.value, self.RightJoystickX.value,\
            self.LeftBumper.value, self.RightBumper.value, self.Y.value, self.A.value, self.X.value,\
            self.B.value, self.Start.value

    def _monitor_controller(self):
        process = True
        while process:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    # normalize between -1 and 1
                    self.LeftJoystickY.value = round(event.state / XboxController.MAX_JOY_VAL, 2)
                elif event.code == 'ABS_X':
                    # normalize between -1 and 1
                    self.LeftJoystickX.value = round(event.state / XboxController.MAX_JOY_VAL, 2)
                elif event.code == 'ABS_RY':
                    # normalize between -1 and 1
                    self.RightJoystickY.value = round(event.state / XboxController.MAX_JOY_VAL, 2)
                elif event.code == 'ABS_RX':
                    # normalize between -1 and 1
                    self.RightJoystickX.value = round(event.state / XboxController.MAX_JOY_VAL, 2)
                elif event.code == 'ABS_Z':
                    # normalize between 0 and 1
                    self.LeftTrigger.value = round(event.state / XboxController.MAX_TRIG_VAL, 2)
                elif event.code == 'ABS_RZ':
                    # normalize between 0 and 1
                    self.RightTrigger.value = round(event.state / XboxController.MAX_TRIG_VAL, 2)
                elif event.code == 'BTN_TL':
                    self.LeftBumper.value = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper.value = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A.value = event.state
                elif event.code == 'BTN_NORTH':
                    # previously switched with X
                    self.Y.value = event.state
                elif event.code == 'BTN_WEST':
                    # previously switched with Y
                    self.X.value = event.state
                elif event.code == 'BTN_EAST':
                    self.B.value = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb.value = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb.value = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back.value = event.state
                elif event.code == 'BTN_START':
                    self.Start.value = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad.value = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad.value = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad.value = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad.value = event.state


if __name__ == '__main__':
    joy = XboxController()
    while True:
        print(joy.read())
        time.sleep(1)
