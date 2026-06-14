## Samsung Fingerprint Position Calculator

> [!CAUTION]
> Result can be inaccurate. I tested this only on a53x and a54x.

# Get values with:
- position : adb shell cat /sys/devices/virtual/fingerprint/fingerprint/position
- size     : adb shell wm size"
- xdpi     : adb shell dumpsys display | grep 'density '
- cutout   : adb shell dumpsys display | grep DisplayCutout
