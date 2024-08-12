"""
File: NwData.py
Data transfer object between numpy linear circuit matrix analysis
and Touchstone Ver.2.x file read/write.
"""
import numpy as np
from CFmt import CFmt as cfmt
from CFmt import FmtConf as fmtconf
from CFmt import MatrixFormat as matform
from _pyio import TextIOWrapper as file


class NwData(object):
    """
    Validate array sizes.
    w: angular frequency array
    ma: linear circuit matrix array;
        linear circuit matrices must always be square.
    """
    @staticmethod
    def areSizesValid(w:np.ndarray, ma:np.ndarray):
        wsh = w.shape
        mash = ma.shape
        if len(wsh) != 1 or len(mash) != 3:
            return False
        if wsh[0] != mash[0] or mash[1] != mash[2]:
            return False
        return True

    """
    Constructor accepts
    w: angular frequency array
    ma: linear circuit matrix array
    """
    def __init__(self, w:np.ndarray, ma:np.ndarray):
        if NwData.areSizesValid(w, ma) == False:
            raise("Invalid array size.")
        self.w = w
        self.ma = ma
        self.maRows = ma.shape[1]
        self.maRowRange = range(self.maRows)
        self.maEleCount = self.maRows * self.maRows # square matrix element count
        self.maTriCount = 0 # Upper or Lower triangle element count
        for i in range(self.maRows + 1):
            self.maTriCount += i

    """
    Write the network data into a Touchstone Ver.2.x file.
    """
    def write(self, conf:fmtconf, tsstream:file):
        for i in range(len(self.w)):
            self.writeWRecord(conf, file, self.w[i], self.ma[i])
    """
    Write a single frequency record in a network data 
    into a Touchstone ver.2.x file.
    """
    def writeWRecord(self, conf:fmtconf, tsstream: file, w:float, m:np.ndarray):
        words = [conf.formatW(w)]
        words.extend(conf.mat2Text(m))
        if self.maRows <= 2:
            file.write(" ".join(words) + "\n")
            return
        index = 0
        for row in self.maRowRange:
            wordsForRow = [ conf.formatW(w) if row == 0 else "  "]
            nextIndex:int = index
            if conf.mf == matform.Full:
                nextIndex += 2 * self.maRows
            elif conf.mf == matform.Upper:
                nextIndex += 2 * (self.maRows - row)
            elif conf.mf == matform.Lower:
                nextIndex += 2 * (row + 1)
            wordsForRow.extend(words[index:nextIndex])
            index = nextIndex
            file.write(" ".join(wordsForRow) + "\n")

    "Read the network data from a Touchstone Ver.2.x file."
    def read(self, conf:fmtconf, tsstream:file):
        for i in range(len(self.w)):
            self.readWRecord(conf, tsstream, i)
    
    """
    Read a single frequency record in a networkdata formatted
    in Touchstone ver.2.x format.
    """
    def readWRecord(self, conf:fmtconf, tsstream:file, i:int):
        wordsCount = self.maEleCount if conf.mf == matform.Full else self.maTriCount
        # read the 1st line of the record.
        textLine:str = tsstream.readline()
        if len(str) == 0:
            raise("Unexpected EOF")
        words = fmtconf.splitEx(textLine)
        if len(words) == 0:
            raise("Unexpected blank line")
        # parse the angular frequency and remove it from words.
        self.w[i] = conf.parseW(words[0])
        words.remove(words[0])
        eleCount:int = self.maEleCount if conf.mf == matform.Full else self.maTriCount
        numCount:int = 2 * eleCount
        while len(words) < numCount:
            textLine = tsstream.readline()
            if len(str) == 0:
                raise("Unexpected EOF")
            additionalWords = fmtconf.splitEx(textLine)
            if len(additionalWords) == 0:
                raise("Unexpected blank line")
            words.extend(additionalWords)
        if len(words) != numCount:
            raise("Inconsistent number count in the record")
        self.ma[i] = conf.text2Mat(words, self.maRows)
        
        
