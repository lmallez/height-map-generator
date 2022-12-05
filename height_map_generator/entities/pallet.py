#!/bin/python3
from dataclasses import dataclass

from entities.tint import Color, Tint


@dataclass
class Pallet:
    def get_color(self, val):
        # isSet = False
        color_val = Color(0, 0, 0)
        for tints in self.tints:
            if tints.isInside(val):
                return tints.get_color(val)
                # if isSet:
                #     color_val.add(tints.get_color(val))
                # else:
                #     color_val = tints.get_color(val)
                #     isSet = True
        return color_val

    tints: [Tint]
