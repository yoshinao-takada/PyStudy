"""
File: NwData.py
Data transfer object between numpy linear circuit matrix analysis
and Touchstone Ver.2.x file read/write.
"""
import numpy as np
from CFmt import CFmt as cfmt
from CFmt import FmtConf as fmtconf
from CFmt import TSOpt as tsopt
from CFmt import TwoPortDataOrder as tpdo
from CFmt import MatrixFormat as matfmt
from CFmt import ComplexFormat as cmpfmt
from CFmt import FreqUnit as fu
from CFmt import Parameter as nwpar
from _pyio import TextIOWrapper as file


"""
A series of angular frequencies and a series of linear
circuit matrices.
"""
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
            self.writeWRecord(conf, tsstream, self.w[i], self.ma[i])
    """
    Write a single frequency record in a network data 
    into a Touchstone ver.2.x file.
    """
    def writeWRecord(self, conf:fmtconf, tsstream:file, w:float, m:np.ndarray):
        words = [conf.formatW(w)]
        words.extend(conf.mat2Text(m))
        if self.maRows <= 2:
            lineText = " ".join(words) + "\n"
            tsstream.write(lineText)
            return
        index = 0
        for row in self.maRowRange:
            wordsForRow = [ conf.formatW(w) if row == 0 else "  "]
            nextIndex:int = index
            if conf.mf == matfmt.Full:
                nextIndex += 2 * self.maRows
            elif conf.mf == matfmt.Upper:
                nextIndex += 2 * (self.maRows - row)
            elif conf.mf == matfmt.Lower:
                nextIndex += 2 * (row + 1)
            wordsForRow.extend(words[index:nextIndex])
            index = nextIndex
            tsstream.write(" ".join(wordsForRow) + "\n")

    "Read the network data from a Touchstone Ver.2.x file."
    def read(self, conf:fmtconf, tsstream:file):
        for i in range(len(self.w)):
            self.readWRecord(conf, tsstream, i)
    
    """
    Read a single frequency record in a networkdata formatted
    in Touchstone ver.2.x format.
    """
    def readWRecord(self, conf:fmtconf, tsstream:file, i:int):
        wordsCount = self.maEleCount if conf.mf == matfmt.Full else self.maTriCount
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
        eleCount:int = self.maEleCount if conf.mf == matfmt.Full else self.maTriCount
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
        
"""
Attributes and their read/write functions of
NwData compatible to Touchstone ver.2.x.
"""
class NwDataAttributes(object):
    #region STATIC_CONSTANTS
    VERSION_KEY:str = "[Version]"
    OPTION_KEY:str = "#"
    NUMPORTS_KEY:str = "[Number of Ports]"
    TPDO_KEY:str = "[Two-Port Data Order]"
    NUMFRQS_KEY:str = "[Number of Frequencies]"
    NUMNOISEFRQS_KEY:str = "[Number of Noise Frequencies]"
    REF_KEY:str = "[Reference]"
    MATFMT_KEY:str = "[Matrix Format]"
    MIXEDMODEORDER_KEY:str = "[Mixed-Mode Order]"
    BEGININFO_KEY:str = "[Begin Information]"
    ENDINFO_KEY:str = "[End Information]"
    NWDATA_KEY:str = "[Network Data]"
    NOISEDATA_KEY:str = "[Noise Data]"
    END_KEY:str = "[End]"
    DIC_MATFMT = {
        matfmt.Full : "Full",
        matfmt.Upper : "Upper",
        matfmt.Lower : "Lower"
    }
    #endregion STATIC_CONSTANTS
    """
    Constructor
    """
    def __init__(self):
        self.ver:str = ""
        self.opt:tsopt = tsopt()
        self.numPorts:int = 0
        self.tpdo:tpdo = tpdo.Modern
        self.numfrqs:int = 0
        self.numnoisefrqs:int = 0
        self.refs:list = []
        self.matfmt:matfmt = matfmt.Full

    def formatConf(self) -> fmtconf:
        return fmtconf(self.opt.fu, self.opt.cf, self.matfmt, self.tpdo)

    """
    Read attributes preceding to [Network Data] block.
    """
    def readPreamble(self, tsstream:file):
        nwdataFound:bool = False
        self.opt.r = -1
        self.tpdo = tpdo.Undefined
        while nwdataFound == False:
            lineText:str = tsstream.readline()
            if len(lineText) == 0:
                raise("Unexpected EOF")
            keyEnd = lineText.find("]")
            if lineText.find(NwDataAttributes.VERSION_KEY) >= 0:
                # [Version]
                words = fmtconf.splitEx(lineText)
                if len(words) < 2:
                    raise(f"Invalid version line\"{lineText}\"")
                self.ver = words[1]
            elif lineText.find(NwDataAttributes.OPTION_KEY) >= 0:
                # option line
                self.opt.parse(lineText)
            elif lineText.find(NwDataAttributes.NUMPORTS_KEY) >= 0:
                # [Numbre of Ports]
                words = fmtconf.splitEx(lineText[keyEnd+1:])
                if len(words) != 1:
                    raise(f"Invalid number of ports line\"{lineText}\"")
                self.numPorts = int(words[0])
            elif lineText.find(NwDataAttributes.TPDO_KEY) >= 0:
                # [Two-Port Data Order]
                words = fmtconf.splitEx(lineText[keyEnd + 1:])
                if len(words) != 1:
                    raise(f"Invalid Two-Port Data Order line\"{lineText}\"")
                self.tpdo = tpdo.Modern if words[0] == "12_21" else tpdo.Classic
            elif lineText.find(NwDataAttributes.NUMFRQS_KEY) >= 0:
                # [Number of Frequencies]
                words = fmtconf.splitEx(lineText[keyEnd + 1:])
                if len(words) != 1:
                    raise(f"Invalid Number of Frequencies line\"{lineText}\"")
                self.numfrqs = int(words[0])
            elif lineText.find(NwDataAttributes.NUMNOISEFRQS_KEY) >= 0:
                # [Number of Noise Frequencies]
                words = fmtconf.splitEx(lineText[keyEnd + 1:])
                if len(words) != 1:
                    raise(f"Invalid Number of Noise Frequencies line\"{lineText}\"")
                self.numnoisefrqs = int(words[0])
            elif lineText.find(NwDataAttributes.REF_KEY) >= 0:
                # [Reference]
                words = fmtconf.splitEx(lineText[keyEnd + 1:])
                if len(words) != self.numPorts:
                    raise(f"Invalid Reference line\"{lineText}\"")
                self.refs = []
                for word in words:
                    self.refs.append(int(word))
            elif lineText.find(NwDataAttributes.MATFMT_KEY) >= 0:
                # [Matrix Format]
                words = fmtconf.splitEx(lineText[keyEnd + 1:])
                if len(words) != 1:
                    raise(f"Invalid Matrix Format line\"{lineText}\"")
                if words[0] == "Full":
                    self.matfmt = matfmt.Full
                elif words[0] == "Upper":
                    self.matfmt = matfmt.Upper
                elif words[0] == "Lower":
                    self.matfmt = matfmt.Lower
                else:
                    raise(f"Invalid Matrix Format line\"{lineText}\"")
            elif lineText.find(NwDataAttributes.NWDATA_KEY) >= 0:
                nwdataFound = True
            elif lineText.find(NwDataAttributes.MIXEDMODEORDER_KEY) >= 0 \
                or lineText.find(NwDataAttributes.BEGININFO_KEY) >= 0 \
                or lineText.find(NwDataAttributes.ENDINFO_KEY) >= 0 :
                pass # ignore these options as not supported.
            else:
                pass # ignore other conditions
    
    def expectEndKey(self, tsstream:file):
        endFound:bool = False
        while endFound == False:
            lineText:str = tsstream.readline()
            if len(lineText) == 0:
                endFound = True
            if lineText.find(NwDataAttributes.END_KEY) >= 0:
                endFound = True
            else:
                pass

    def writePreamble(self, tsstream:file):
        tsstream.write(NwDataAttributes.VERSION_KEY + " " + self.ver + "\n")
        tsstream.write(self.opt.format() + "\n")
        tsstream.write(NwDataAttributes.NUMPORTS_KEY + " " + str(self.numPorts) + "\n")
        if self.tpdo != tpdo.Undefined:
            tpdoValue = " 12_21\n" if self.tpdo == tpdo.Modern else " 21_12\n"
            tsstream.write(NwDataAttributes.TPDO_KEY + tpdoValue)
        tsstream.write(NwDataAttributes.NUMFRQS_KEY + " " + str(self.numfrqs) + "\n")
        tsstream.write(NwDataAttributes.NUMNOISEFRQS_KEY + " " + str(self.numnoisefrqs) + "\n")
        if len(self.refs) == self.numPorts:
            referenceValue = ""
            for x in self.refs:
                referenceValue += " " + str(x)
            referenceValue += "\n"
            tsstream.write(NwDataAttributes.REF_KEY + referenceValue)
        tsstream.write(NwDataAttributes.MATFMT_KEY + " " + NwDataAttributes.DIC_MATFMT[self.matfmt] + "\n")
        tsstream.write(NwDataAttributes.NWDATA_KEY + "\n")
