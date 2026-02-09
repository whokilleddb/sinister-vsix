"""
Generator for LivePreview
"""
import os
from .baseext import BaseExtension

class LivePreview(BaseExtension):
    def __init__(self):
        super().__init__("livepreview")
        self.template_path = os.path.join(
            os.getcwd(), "templates", "livepreview"
        )
        self.vsix = "live-server-0.4.15.vsix"
        