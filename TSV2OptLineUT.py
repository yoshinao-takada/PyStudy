"""
File: TSV2OptLineUT.py
Unit test for TSV2OptLine.py
"""
import TSV2OptLine as opt

def main():
    o = opt.TSV2OptLine()
    print(o.DicFormat[opt.Format.RI])
    print(o.DicFreqUnit[opt.FreqUnit.MHz])
    print(o.DicParameter[opt.Parameter.Y])
    print(o.formatOptionLine())
    src:str = "# kHz S RI R 75"
    o.parse(src)
    print(o.formatOptionLine())
    pass

if __name__ == "__main__":
    main()