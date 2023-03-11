import sys
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def change_volume(step_size):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = current_volume

    if step_size[0] == '+':
        new_volume = min(current_volume + float(step_size[1:])/100, 1.0)
    elif step_size[0] == '-':
        new_volume = max(current_volume - float(step_size[1:])/100, 0.0)
    elif step_size[0] == '=':
        new_volume = float(step_size[1:])/100

    volume.SetMasterVolumeLevelScalar(new_volume, None)
    current_modified_volume = round(new_volume * 100)
    print(f"{current_modified_volume}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please enter a step size using +, -, or = followed by a number.")
        sys.exit()

    step_size = sys.argv[1]
    change_volume(step_size)
