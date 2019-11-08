#!/bin/python3

from HeightMapGenerator.entities.Tint import Color


class Pallet:
    def __init__(self, tints):
        self.tints = tints

    def getColor(self, val):
        # isSet = False
        color_val = Color(0, 0, 0)
        for tints in self.tints:
            if tints.isInside(val):
                return tints.getColor(val)
                # if isSet:
                #     color_val.add(tints.getColor(val))
                # else:
                #     color_val = tints.getColor(val)
                #     isSet = True
        return color_val

    tints = None
