"""
Base extension class
"""

class BaseExtension:
    def __init__(self, name):
        self.name = name
        self.template_path = None
        self.vsix = None

    
