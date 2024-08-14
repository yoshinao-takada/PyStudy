"""
Touchstone file reader/writer
"""
import numpy as np
import CFmt
from _pyio import FileIO as file

"""
Network data with angular frequencies
"""
class NwData(object):
    """
    Constructor
    """
    def __init__(self):
        self.w:np.ndarray
        self.m:np.ndarray
        self.stream:file
        self.lineTexts:list = []
        self.opt:CFmt.TSOpt = CFmt.TSOpt()
        self.nPorts = 0
        self.nFreqPoints = 0
        self.c2Text = CFmt.FmtConf.dicFormatNum[self.opt.cf]
        self.w2Text = CFmt.FmtConf.dictFormatFreq[self.opt.fu]
        self.text2c = CFmt.FmtConf.dicParseNum[self.opt.cf]
        self.text2w = CFmt.FmtConf.dicParseFreq[self.opt.fu]
    
    #region WRITER_METHODS
    def setVer1Opt(self, fu:CFmt.FreqUnit, pa:CFmt.Parameter, cf:CFmt.ComplexFormat, r:float):
        self.opt.fu = fu
        self.opt.pa = pa
        self.opt.cf = cf
        self.opt.r = r
        self.c2Text = CFmt.FmtConf.dicFormatNum[self.opt.cf]
        self.w2Text = CFmt.FmtConf.dictFormatFreq[self.opt.fu]

    def setNwData(self, w:np.ndarray, m:np.ndarray):
        self.w = w
        self.m = m
        if len(m.shape) != 3:
            raise(f"Invalid array dimension of m:{m.shape}")
        if len(w) != m.shape[0]:
            raise(f"Array size mismatch: len(w)={len(w)}, len(m)={m.shape[0]}")
        if m.shape[1] != m.shape[2]:
            raise(f"Data array not square: m.shape={m.shape}")
        self.nFreqPoints = len(w)
        self.nPorts = m.shape[1]

    def setHeaderComments(self, comments:list):
        self.lineTexts = []
        for comment in comments:
            self.lineTexts.append("! " + str(comment) + "\n")
    
    def fmtVer1wm(self, w:float, m:np.ndarray):
        rangePorts = range(self.nPorts)
        words = [self.w2Text(w)]
        if self.nPorts <= 2:
            for row in rangePorts:
                for column in rangePorts:
                    words.extend(self.c2Text(m[row,column]))
            self.lineTexts.append(" ".join(words) + "\n")
        else:
            for row in rangePorts:
                for column in rangePorts:
                    words.extend(self.c2Text(m[row,column]))
                self.lineTexts.append(" ".join(words) + "\n")
                words = " "
        return
    
    def fmtVer1(self):
        self.lineTexts.append(self.opt.format() + "\n")
        for i in range(len(self.w)):
            self.fmtVer1wm(self.w[i], self.m[i])

    def write(self, stream:file):
        for text in self.lineTexts:
            stream.write(text)

    #endregion WRITER_METHODS

    #region READER_METHODS
    def read(self, stream:file):
        self.lineTexts = []
        while True:
            text = stream.readline()
            if len(text) == 0: # EOF
                break
            if text[0] == '!': # comment line
                continue
            self.lineTexts.append(text)
        self.estimatePortNumVer1()
        self.estimateFreqPointsVer1()
        self.parseOptVer1()

    
    @staticmethod
    def isOdd(i:int):
        return i % 2 == 1
    
    def estimatePortNumVer1(self):
        words = []
        sampleLine:bool = False
        for text in self.lineTexts:
            if text[0] == '#':
                continue
            lineWords = CFmt.FmtConf.splitEx(text)
            if sampleLine and NwData.isOdd(len(lineWords)):
                break
            elif sampleLine == False and NwData.isOdd(len(lineWords)):
                sampleLine = True
                words.extend(lineWords)
            elif sampleLine and NwData.isOdd(len(lineWords)) == False:
                words.extend(lineWords)
            else:
                pass
        n:int = len(words) - 1
        self.nPorts = -1
        for i in range(n):
            if (2 * i * i) == n:
                self.nPorts = i
                break
        if self.nPorts < 0:
            raise("Invalid data layout")
        
    def estimateFreqPointsVer1(self):
        self.nFreqPoints = 0
        for text in self.lineTexts:
            if text[0] == '#' or text[0] == ' ':
                continue
            else:
                self.nFreqPoints += 1

    def parseOptVer1(self):
        for text in self.lineTexts:
            if text[0] == '#':
                self.opt.parse(text)
                break
        if self.opt.r < 0:
            self.opt.r = 50
        self.text2c = CFmt.FmtConf.dicParseNum[self.opt.cf]
        self.text2w = CFmt.FmtConf.dicParseFreq[self.opt.fu]


    def extractNNwDataVer1(self, w:np.ndarray, m:np.ndarray):
        words = []
        i:int = 0
        wcRecord = 1 + 2 * self.nPorts * self.nPorts
        for text in self.lineTexts:
            if text[0] == '#':
                continue
            words.extend(CFmt.FmtConf.splitEx(text))
            if len(words) == wcRecord:
                w[i] = self.text2w(words[0])
                del words[0]
                elementIndex:int = 0
                for row in range(self.nPorts):
                    for column in range(self.nPorts):
                        m[i, row, column] = self.text2c(words[elementIndex:elementIndex + 2])
                        elementIndex += 2
                if self.nPorts == 2:
                    c = m[i, 0, 1]
                    m[i, 0, 1] = m[i, 1, 0]
                    m[i, 1, 0] = c
                words = []
                i += 1

    #endregion READER_METHODS
