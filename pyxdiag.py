# -*- coding: utf-8 -*-
import os
import sys
import tempfile
import subprocess
import re

import argparse
import pathlib
import glob


def tgen(txt, ofmt="png"):

    fd, ifname = tempfile.mkstemp(dir=pathlib.Path.cwd())
    fd.write(txt)
    os.close(ifname)
    
    ofname = fgen(ifname, ofmt)

    os.remove(ifname)

    return ofname


def fgen(ifname="", ofmt="png"):
    ofpath = ""
    if pathlib.Path(ifname).is_file():
        ifpath = pathlib.Path(ifname).resolve()
        with open(ifpath,"r", encoding="utf-8") as f:
            txt = f.read()

        stderr, cmd = exec_xdiag(get_xdiag(txt), ifpath, ofmt)
        stderr = stderr if sys.stderr.encoding != "utf-8" else stderr.decode(sys.stderr.encoding)
        
        if stderr:
            if "WARNING" in stderr:
                # warning(s) might be found but the output file is to be generated.
                ofpath = _change_extension(ifpath, ofmt)
                print(f"[pyxiag][warning] {ofpath}\n{stderr}")
            else:
                # error(s) might occur. there is no output file.
                ofpath = f"no output for {ifpath}"
                print(f"[pyxiag][error] {ofpath}\n{stderr}")
        else:
            # no error. it should be ok.
            ofpath = _change_extension(ifpath, ofmt) # there is no way to get the absolute path of the output file from xdiag tools.
            print(f"[pyxiag][success] {ofpath}\n{stderr}")
    else:
        ofpath = f"no output for {ifname}" 
        print("[pyxiag][error] the input file might be invalid.")

    return ofpath

def get_xdiag(txt):
    xdiag = None
    expr = re.compile(r" *((block|seq|nw|packet|rack|act)diag) .*{")
    for s in txt.splitlines():
        m = expr.search(s)
        if m:
            xdiag = m.group(1)
            break
    return xdiag

def exec_xdiag(xdiag, ifpath, ofmt):
    cmd = [f"{xdiag}", f"{ifpath}", f"-T{ofmt}" ]
    if ofmt == "png":
        cmd.append("--no-transparency")
        stderr = subprocess.run(cmd, stderr=subprocess.PIPE).stderr
    return (stderr, cmd)
        

def _change_extension(ifpath, ext):
    p = pathlib.Path(ifpath)
    return str(p.parent.joinpath(p.stem + "." + ext))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--antialias", action="store_true", help="Pass diagram image to anti-alias filter")
    parser.add_argument("-f", "--font", help="FONT  use FONT to draw diagram")
    parser.add_argument("--fontmap", dest="font" , help="use FONTMAP file to draw diagram")
    parser.add_argument("--no-transparency", action="store_true", dest="FONT" , help="do not make transparent background of diagram (PNG only)")
    parser.add_argument("--size=SIZE" , help="Size of diagram (ex. 320x240)")
    parser.add_argument("-T", dest="size" , choices=["PNG", "SVG"], help="Output diagram as TYPE format")
    parser.add_argument("files", type=str, nargs="*")

    args = parser.parse_args()
    print(args)

    # fset=set()
    # for f in args.files:
    #     for f in pathlib.Path().glob(f):
    #         fset.add(str(pathlib.Path(f).resolve()))
    
    # for f in sorted(fset):
    #     fgen(f)