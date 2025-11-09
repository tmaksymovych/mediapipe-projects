from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def Volume_scale(current_length:int):
    # Get default audio endpoint (speakers)
    devices = AudioUtilities.GetSpeakers()
    
    # 'volume' is now our object to control volume
    volume = devices.EndpointVolume

    # --- Get Current Volume ---
    # GetMasterVolumeLevelScalar() returns a float between 0.0 and 1.0
    current_volume_scalar = volume.GetMasterVolumeLevelScalar()
    print(f"Current volume (scalar): {current_volume_scalar}")
    print(f"Current volume (%): {current_volume_scalar * 100:.0f}%")

    # --- Set Volume ---
    # We want to set it to 50% (0.5 scalar)
    print(f"Setting volume to {current_length * 100:.0f}%")
    volume.SetMasterVolumeLevelScalar(current_length, None)

    # --- Other useful things ---
    # Mute
    # volume.SetMute(True, None)
    # Unmute
    # volume.SetMute(False, None)
    # Get mute status
    # is_muted = volume.GetMute()
    # print(f"Is muted: {is_muted}")
