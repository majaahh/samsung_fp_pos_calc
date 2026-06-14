#!/usr/bin/env python3
#
# Copyright (c) 2026 Majaahh
# SPDX-License-Identifier: Apache-2.0
#

import argparse


def calc_sensor_location(position, width, height, ydpi):
    vals = [float(x) for x in position.split(",")]

    if len(vals) < 6:
        raise ValueError("Expected at least 6 comma-separated values")

    bottom_mm = vals[0]
    active_mm = vals[5]

    mm_to_px = ydpi / 25.4

    bottom_px = bottom_mm * mm_to_px
    active_px = active_mm * mm_to_px

    center_x = int(width / 2)
    center_y = int(height - bottom_px - (active_px / 2))

    radius = int(active_px / 2)

    return (
        round(center_x),
        round(center_y),
        round(radius),
        {
            "bottom_mm": bottom_mm,
            "active_mm": active_mm,
            "bottom_px": round(bottom_px),
            "active_px": round(active_px),
        },
    )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Samsung UDFPS sensor_location calculator\n\n"
            "Get values with:\n"
            "  position : adb shell cat /sys/class/fingerprint/fingerprint/position\n"
            "  size     : adb shell wm size\n"
            "  ydpi     : adb shell dumpsys display | sed -n 's/.*density \\([0-9][0-9]*, [0-9.][0-9.]* x [0-9.][0-9.]* dpi\\).*/\\1/p'\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("position")
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--height", type=int, required=True)
    parser.add_argument("--ydpi", type=float, required=True)

    args = parser.parse_args()

    x, y, r, debug = calc_sensor_location(
        args.position,
        args.width,
        args.height,
        args.ydpi,
    )

    print(f"{x}|{y}|{r} (<x>|<y>|<radius>)")
    print()
    print("Debug:")
    for k, v in debug.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
