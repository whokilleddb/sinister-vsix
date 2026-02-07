"""
Contains the class responsible for building things
"""
import os
from tempfile import TemporaryDirectory

from src.extensions.livepreview import LivePreview

class Generator:
    def __init__(self, ext, shellcode, inflate, enc):
        self.ext = None
        self.shellcode = shellcode
        self.inflate = inflate 
        self.enc = enc
        self._tmp = TemporaryDirectory(delete=False)
        self.tmp = self._tmp.name

        _ext = ext.lower()
        print(_ext)
        if _ext == "livepreview":
            self.ext = LivePreview()
        
    def template_files(self):
        """template files for compilation"""

        # First copy files into temp directory 

        # Copy shellcode file 

        # Copy rust files 
    