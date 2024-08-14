"""
File: CFmt.py
Complex number and matrix formatter/parser for Touchstone V2.x format
"""

import math
import cmath
from enum import Enum
import numpy as np
#region ENUM_DEFS
class TwoPortDataOrder(Enum):
    Classic = 0 # 21_12
    Modern = 1  # 12_21
    Undefined = 2

class MatrixFormat(Enum):
    Full = 0
    Lower = 1
    Upper = 2

class ComplexFormat(Enum):
    dB = 0
    MA = 1
    RI = 2

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
#endregion ENUM_DEFS
class TSOpt(object):
    DicFreqUnit = {
        FreqUnit.Hz : "Hz",
        FreqUnit.kHz : "kHz",
        FreqUnit.MHz : "MHz",
        FreqUnit.GHz : "GHz"
    }

    DicParameter = {
        Parameter.S : "S",
        Parameter.Y : "Y",
        Parameter.Z : "Z",
        Parameter.H : "H",
        Parameter.G : "G"
    }

    DicFormat = {
        ComplexFormat.dB : "DB",
        ComplexFormat.MA : "MA",
        ComplexFormat.RI : "RI",
    }

    """
    Constructor sets default values.
    """
    def __init__(self):
        self.fu: FreqUnit = FreqUnit.GHz
        self.pa: Parameter = Parameter.S
        self.cf: ComplexFormat = ComplexFormat.MA
        self.r: float = 50

    """
    Parse an option line.
    """
    def parse(self, str: str):
        if (str[0] != '#'):
            raise("Not an option line")
        options = FmtConf.splitEx(str)
        nextRVal:bool = False
        self.r = -1
        for opt in options:
            if opt == "Hz":
                self.fu = FreqUnit.Hz
                nextRVal = False
            elif opt == "kHz":
                self.fu = FreqUnit.kHz
                nextRVal = False
            elif opt == "MHz":
                self.fu = FreqUnit.MHz
                nextRVal = False
            elif opt == "GHz":
                self.fu = FreqUnit.GHz
                nextRVal = False
            elif opt == "S":
                self.pa = Parameter.S
                nextRVal = False
            elif opt == "Y":
                self.pa = Parameter.Y
                nextRVal = False
            elif opt == "Z":
                self.pa = Parameter.Z
                nextRVal = False
            elif opt == "H":
                self.pa = Parameter.H
                nextRVal = False
            elif opt == "G":
                self.pa = Parameter.G
                nextRVal = False
            elif opt == "DB":
                self.cf = ComplexFormat.dB
                nextRVal = False
            elif opt == "MA":
                self.cf = ComplexFormat.MA
                nextRVal = False
            elif opt == "RI":
                self.cf = ComplexFormat.RI
                nextRVal = False
            elif opt == "R":
                nextRVal = True
            elif nextRVal:
                self.r = float(opt)
            else:
                pass
    
    """
    Format an option line.
    """
    def format(self) -> str:
        elements = ["#"]
        elements.append(self.DicFreqUnit[self.fu])
        elements.append(self.DicParameter[self.pa])
        elements.append(self.DicFormat[self.cf])
        if self.r > 0:
            elements.append("R")
            elements.append(str(self.r))
        return " ".join(elements)

class CFmt(object):
    RAD2DEG_COEFF: float = 180.0 / math.pi
    DEG2RAD_COEFF: float = math.pi / 180.0
    @staticmethod
    def rad2deg(x: float):
        return CFmt.RAD2DEG_COEFF * x
    
    @staticmethod
    def deg2rad(x: float):
        return CFmt.DEG2RAD_COEFF * x

    @staticmethod
    def mag2dB(x:float):
        return 20.0 * math.log10(x)
        
    @staticmethod
    def dB2mag(x:float):
        return math.pow(10.0, x / 20.0)
    
    @staticmethod
    def c2RI(c: complex):
        return [c.real, c.imag]
    
    @staticmethod
    def c2MA(c: complex):
        return [abs(c), CFmt.rad2deg(math.atan2(c.imag, c.real))]
    
    @staticmethod
    def c2dB(c: complex):
        return [CFmt.mag2dB(abs(c)), CFmt.rad2deg(math.atan2(c.imag, c.real))]

    @staticmethod
    def RI2c(ri):
        return complex(ri[0], ri[1])
    
    @staticmethod
    def MA2c(ma):
        arg = CFmt.deg2rad(ma[1])
        return complex(ma[0] * math.cos(arg), ma[0] * math.sin(arg))
    
    @staticmethod
    def dB2c(db):
        mag = CFmt.dB2mag(db[0])
        return CFmt.MA2c([mag, db[1]])
    
    @staticmethod
    def fmtRI(c: complex):
        ri = CFmt.c2RI(c)
        return [str(ri[0]), str(ri[1])]
    
    @staticmethod
    def fmtMA(c: complex):
        ma = CFmt.c2MA(c)
        return [str(ma[0]), str(ma[1])]
    
    @staticmethod
    def fmtdB(c: complex):
        dB = CFmt.c2dB(c)
        return [str(dB[0]), str(dB[1])]
    
    @staticmethod
    def parseRI(ri: list) -> complex:
        return CFmt.RI2c([float(ri[0]), float(ri[1])])
    
    @staticmethod
    def parseMA(ma: list) -> complex:
        return CFmt.MA2c([float(ma[0]), float(ma[1])])
    
    @staticmethod
    def parsedB(dB: list) -> complex:
        return CFmt.dB2c([float(dB[0]), float(dB[1])])
    
class FmtConf(object):
    #region CONST_NUMBERS
    W2F:float = 0.5 / math.pi
    F2W:float = 2.0 * math.pi
    killo:float = 1000.0
    Mega:float = 1e6
    Giga:float = 1e9
    rcpKillo:float = 1e-3
    rcpMega:float = 1e-6
    rcpGiga:float = 1e-9
    #endregion CONST_NUMBERS

    #region SCALAR_FORMAT_PARSE_OPERATIONS
    #region FUNCTION_DEFS
    @staticmethod
    def fmtW2Hz(w: float):
        return str(FmtConf.W2F * w)
    
    @staticmethod
    def fmtW2kHz(w: float):
        return str(FmtConf.W2F * w * FmtConf.rcpKillo)
    
    @staticmethod
    def fmtW2MHz(w:float):
        return str(FmtConf.W2F * w * FmtConf.rcpMega)
    
    @staticmethod
    def fmtW2GHz(w:float):
        return str(FmtConf.W2F * w * FmtConf.rcpGiga)
    
    @staticmethod
    def parseHz2W(strHz:str):
        return FmtConf.F2W * float(strHz)
    
    @staticmethod
    def parsekHz2W(strkHz:str):
        return FmtConf.F2W * float(strkHz) * FmtConf.killo
    
    @staticmethod
    def parseMHz2W(strMHz:str):
        return FmtConf.F2W * float(strMHz) * FmtConf.Mega
    
    @staticmethod
    def parseGHz2W(strGHz:str):
        return FmtConf.F2W * float(strGHz) * FmtConf.Giga
    
    # 1 or more space delimitted number texts split int a text list.
    @staticmethod
    def splitEx(numStr:str):
        redundantTexts = numStr.split("\t")
        redundantTexts2 = []
        for t in redundantTexts:
            redundantTexts2.extend(t.split(" "))
        dense = []
        for t in redundantTexts2:
            if len(t) == 0:
                continue
            dense.append(t)
        return dense
    #endregion FUNCTION_DEFS
    
    # dictoinary key: FreqUnit, value: formatter function for angular frequency
    #region FUNCTION_DICTIONARIES
    dictFormatFreq = {
        FreqUnit.Hz: fmtW2Hz,
        FreqUnit.kHz: fmtW2kHz,
        FreqUnit.MHz: fmtW2MHz,
        FreqUnit.GHz: fmtW2GHz
    }
    
    #dictionary key: FreqUnit, value: parser function for angular freqeuncy
    dicParseFreq = {
        FreqUnit.Hz: parseHz2W,
        FreqUnit.kHz: parsekHz2W,
        FreqUnit.MHz: parseMHz2W,
        FreqUnit.GHz: parseGHz2W,
    }

    #dictionary key: complex format, value: formatter function for a complex number
    dicFormatNum = {
        ComplexFormat.dB: CFmt.fmtdB,
        ComplexFormat.MA: CFmt.fmtMA,
        ComplexFormat.RI: CFmt.fmtRI
    }

    #dictionary key: complex format, value: parser function for a complex number
    dicParseNum = {
        ComplexFormat.dB: CFmt.parsedB,
        ComplexFormat.MA: CFmt.parseMA,
        ComplexFormat.RI: CFmt.parseRI
    }
    #endregion FUNCTION_DICTIONARIES
    #endregion SCALAR_FORMAT_PARSE_OPERATIONS

    def __init__(self, fu:FreqUnit, cf:ComplexFormat, mf:MatrixFormat, tpdo:TwoPortDataOrder):
        self.fu = fu
        self.cf = cf
        self.mf = mf
        self.tpdo = tpdo
        # formatters and parsers for scalar values (angular freq and complex numbers)
        self.formatW = FmtConf.dictFormatFreq[fu] # formatter for angular freq to scaled text in Touchstone style.
        self.parseW = FmtConf.dicParseFreq[fu] # parser for angular freq from scaled text in Touchstone style.
        self.formatNum = FmtConf.dicFormatNum[cf] # formatter for a complex number to text in Touchstone style.
        self.parseNum = FmtConf.dicParseNum[cf] # parser for a complex number from text in Touchstone style.
        self.mat2Text = self.mat2TextFull
        self.text2Mat = self.text2MatFull
        if mf == MatrixFormat.Upper:
            self.mat2Text = self.mat2TextUpper
            self.text2Mat = self.text2MatUpper
        elif mf == MatrixFormat.Lower:
            self.mat2Text = self.mat2TextLower
            self.text2Mat = self.text2MatLower
        
    #region MATRIX_FORMAT_PARSE_OPERATIONS
    def mat2TextFull(self, m:np.ndarray):
        rows:int = m.shape[0]
        words = []
        for row in range(rows):
            for column in range(rows):
                words.extend(self.formatNum(m[row,column]))
        return words
    
    def mat2TextUpper(self, m:np.ndarray):
        rows:int = m.shape[0]
        words = []
        for row in range(rows):
            for column in range(row, rows):
                words.extend(self.formatNum(m[row,column]))
        return words
    
    def mat2TextLower(self, m:np.ndarray):
        rows:int = m.shape[0]
        words = []
        for row in range(rows):
            for column in range(row + 1):
                words.extend(self.formatNum(m[row,column]))
        return words
    
    def text2MatFull(self, text:list, rows:int):
        index:int = 0
        m = np.zeros([rows, rows], complex)
        for row in range(rows):
            for column in range(rows):
                floatfloat = [text[index], text[index + 1]]
                m[row,column] = self.parseNum(floatfloat)
                index += 2
        return m
    
    def text2MatUpper(self, words:list, rows:int):
        index:int = 0
        m = np.zeros([rows, rows], complex)
        for row in range(rows):
            for column in range(row, rows):
                floatfloat = [words[index], words[index + 1]]
                m[column, row] = m[row,column] = self.parseNum(floatfloat)
                index  += 2
        return m
    
    def text2MatLower(self, words:str, rows:int):
        index:int = 0
        m = np.zeros([rows, rows], complex)
        for row in range(rows):
            for column in range(row + 1):
                floatfloat = [words[index], words[index + 1]]
                m[column, row] = m[row, column] = self.parseNum(floatfloat)
                index  += 2
        return m
    #endregion MATRIX_FORMAT_PARSE_OPERATIONS
