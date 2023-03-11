from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Get the default audio playback device
devices = AudioUtilities.GetSpeakers()

# Activate the endpoint volume interface
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Get the current system volume scalar
current_scalar = int(volume.GetMasterVolumeLevelScalar() * 100)

# Define the step size as 6 (which corresponds to 6% of the total volume range)
step_size = 6

# Calculate the new system volume scalar with a consistent increase of 6
new_scalar = min(current_scalar + step_size, 100)

# Set the new system volume scalar
volume.SetMasterVolumeLevelScalar(new_scalar / 100, None)

# Print the current and new system volume scalars
print(f"Current system volume: {current_scalar}")
print(f"New system volume: {new_scalar}")
