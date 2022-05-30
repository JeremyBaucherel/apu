# -*- coding: iso-8859-1 -*-

import os.path

def join (path1, *args):
    sep = u"\\"
    path = str(path1)
           
    for subpath in args:
        path += sep + str(subpath)
    
    return path


class Path:

    def __init__ (self, init_path=None):
        self._path = u""
        if init_path != None:
            self._path = os.path.normpath(str(init_path))
    
    def append (self, path):
        self._path = os.path.join(self._path, str(path))
        
    def __add__ (self, path):
        self.append(path)
        return self
    
    def __iadd (self, path):
        self.append(path)
        return self

    def __str__ (self):
        return self._path
