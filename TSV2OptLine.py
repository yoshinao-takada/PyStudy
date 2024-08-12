"""
File: TSV2OptLine.py
TouchStone v2.x Option line
"""
from enum import Enum
import math

class FreqUnit(Enum):
    Hz = 0
    kHz = 1
    MHz = 2
    GHz = 3

class Parameter(Enum):
    S = 0
    Y = 1
    Z = 2
    H = 3
    G = 4

class Format(Enum):
    DB = 0
    MA = 1
    RI = 2


class TSV2OptLine(object):
    DicFreqUnit = {
        FreqUnit.Hz : "Hz",
        FreqUnit.kHz : "kHz",
        FreqUnit.MHz : "MHz",
        FreqUnit.GHz : "GHz"
    }

    FreqUnitCoeff = {
        FreqUnit.Hz : 1.0,
        FreqUnit.kHz : 1000.0,
        FreqUnit.MHz : 1.0e6,
        FreqUnit.GHz : 1.0e9,
    }

    DicParameter = {
        Parameter.S : "S",
        Parameter.Y : "Y",
        Parameter.Z : "Z",
        Parameter.H : "H",
        Parameter.G : "G"
    }

    DicFormat = {
        Format.DB : "DB",
        Format.MA : "MA",
        Format.RI : "RI"
    }

    ln10 = math.log(10)
    ln10_20 = ln10 / 20.0

    @staticmethod
    def rad2deg(x: float):
        return 180.0 * x / math.pi
    
    @staticmethod
    def deg2rad(x: float):
        return math.pi * x / 180.0
    
    @staticmethod
    def complex2dB(x: complex):
        return [20.0 * math.log10(abs(x)), TSV2OptLine.rad2deg(math.atan2(x.imag, x.real))]
    
    @staticmethod
    def complex2MA(x: complex):
        return [abs(x), TSV2OptLine.rad2deg(math.atan2(x.imag, x.real))]
    
    @staticmethod
    def complex2RI(x: complex):
        return [x.real, x.imag]
    
    @staticmethod
    def dB2complex(xy):
        amp = math.exp(xy[0] * TSV2OptLine.ln10_20)
        arg = TSV2OptLine.deg2rad(xy[1])
        re = amp * math.cos(arg)
        im = amp * math.sin(arg)
        return complex(re, im)
    
    @staticmethod
    def MA2complex(xy):
        amp = xy[0]
        arg = TSV2OptLine.deg2rad(xy[1])
        re = amp * math.cos(arg)
        im = amp * math.sin(arg)
        return complex(re, im)
    
    @staticmethod
    def RI2complex(xy):
        return complex(xy[0], xy[1])
    
    """
    Constructor sets default values.
    """
    def __init__(self):
        self.FreqUnit: FreqUnit = FreqUnit.GHz
        self.Parameter: Parameter = Parameter.S
        self.Format: Format = Format.MA
        self.R: float = 50

    """
    Parse an option line.
    """
    def parse(self, str: str):
        if (str[0] != '#'):
            raise("Not an option line.")
        redundantOptions = str.split(' ')
        options = []
        # remove redundant items.
        for opt in redundantOptions:
            if len(opt) > 0:
                options.append(opt)
        nextRVal:bool = False
        for opt in options:
            if opt == "Hz":
                self.FreqUnit = FreqUnit.Hz
                nextRVal = False
            elif opt == "kHz":
                self.FreqUnit = FreqUnit.kHz
                nextRVal = False
            elif opt == "MHz":
                self.FreqUnit = FreqUnit.MHz
                nextRVal = False
            elif opt == "GHz":
                self.FreqUnit = FreqUnit.GHz
                nextRVal = False
            elif opt == "S":
                self.Parameter = Parameter.S
                nextRVal = False
            elif opt == "Y":
                self.Parameter = Parameter.Y
                nextRVal = False
            elif opt == "Z":
                self.Parameter = Parameter.Z
                nextRVal = False
            elif opt == "H":
                self.Parameter = Parameter.H
                nextRVal = False
            elif opt == "G":
                self.Parameter = Parameter.G
                nextRVal = False
            elif opt == "DB":
                self.Format = Format.DB
                nextRVal = False
            elif opt == "MA":
                self.Format = Format.MA
                nextRVal = False
            elif opt == "RI":
                self.Format = Format.RI
                nextRVal = False
            elif opt == "R":
                nextRVal = True
            elif nextRVal:
                self.R = float(opt)
            else:
                pass

    
    """
    Format an option line
    """
    def formatOptionLine(self):
        elements = ["#"]
        elements.append(self.DicFreqUnit[self.FreqUnit])
        elements.append(self.DicParameter[self.Parameter])
        elements.append(self.DicFormat[self.Format])
        elements.append("R")
        elements.append(str(self.R))
        return " ".join(elements)
        

