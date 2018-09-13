#!/bin/python3

from entity.Teinte import Color


class Pallette:
    def __init__(self, teintes):
        self.teintes = teintes

    def getColor(self, val):
        # isSet = False
        colorval = Color(0, 0, 0)
        for teinte in self.teintes:
            if teinte.isInside(val):
                return teinte.getColor(val)
                # if isSet:
                #     colorval.add(teinte.getColor(val))
                # else:
                #     colorval = teinte.getColor(val)
                #     isSet = True
        return colorval

    teintes = None