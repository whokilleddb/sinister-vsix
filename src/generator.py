"""
Contains the class responsible for building things
"""
import os
import shutil
from tempfile import TemporaryDirectory

from src.extensions.livepreview import LivePreview

class Generator:
    def __init__(self, ext, shellcode, enc):
        self.ext = None
        self.shellcode = shellcode
        # self.inflate = inflate 
        self.enc = enc
        self._tmp = TemporaryDirectory(delete=False)
        self.tmp = self._tmp.name
        print("[+] Temporary build directory:\t\t"+self.tmp)

        _ext = ext.lower()
        if _ext == "livepreview":
            self.ext = LivePreview()
        
    def template_files(self):
        """template files for compilation"""

        # Copy shellcode file
        temp_shellcode = os.path.join(self.tmp, "payload.bin")
        shutil.copyfile(self.shellcode, temp_shellcode)
        print("[+] Shellcode copied to:\t\t"+temp_shellcode) 

        # First copy files into temp directory 



        # Copy rust files 
    