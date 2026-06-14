#!/usr/bin/env python3
#
# Copyright (c) 2026 Majaahh
# SPDX-License-Identifier: Apache-2.0
#

import argparse


def calc_sensor_location(position, width, height, xdpi, cutout=88):
    vals = [float(x) for x in position.split(",")]

    if len(vals) < 9:
        raise ValueError("Expected 9 comma-separated values")

    # FingerprintService$$ExternalSyntheticLambda1
    margin_bottom = vals[0]
    margin_left = vals[1]
    area_height = vals[3]
    active_area = vals[5]

    scale = xdpi / 25.4

    active_px = active_area * scale
    bottom_px = margin_bottom * scale
    left_px = margin_left * scale
    height_px = area_height * scale

    half_active = active_px / 2

    # SemUdfpsHelper.getFodSensorAreaRect()
    rect_left = (width / 2) - left_px - half_active
    rect_top = height - ((height_px / 2) + bottom_px + half_active)

    rect_right = rect_left + active_px
    rect_bottom = rect_top + active_px

    # Center of FOD rect
    center_x = round((rect_left + rect_right) / 2)
    center_y = round((rect_top + rect_bottom) / 2)

    # Empirical Samsung correction
    center_y -= round(cutout / 2)

    radius = int((active_px - 1) / 2)

    return (
        center_x,
        center_y,
        radius,
        {
            "rect_left": round(rect_left),
            "rect_top": round(rect_top),
            "rect_right": round(rect_right),
            "rect_bottom": round(rect_bottom),
            "active_px": active_px,
        },
    )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Samsung UDFPS sensor_location calculator\n\n"
            "Get values with:\n"
            "  position : adb shell cat /sys/devices/virtual/fingerprint/fingerprint/position\n"
            "  size     : adb shell wm size\n"
            "  xdpi     : adb shell dumpsys display | grep 'density '\n"
            "  cutout   : adb shell dumpsys display | grep DisplayCutout\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("position")
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--height", type=int, required=True)
    parser.add_argument("--xdpi", type=float, required=True)
    parser.add_argument("--cutout", type=int, default=88)

    args = parser.parse_args()

    x, y, r, debug = calc_sensor_location(
        args.position,
        args.width,
        args.height,
        args.xdpi,
        args.cutout,
    )

    print(f"{x}|{y}|{r} (<x>|<y>|<radius>)")
    print()
    print("Debug:")
    for k, v in debug.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
