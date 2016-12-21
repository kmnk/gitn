# File: gitn.py
# Author: kmnk <kmnknmk at gmail.com>
# License: MIT license

import os
import re
import sys

print(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from gitn.source.factory import Factory
from .base import Base

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'gitn'

    def on_init(self, context):
        if not hasattr(self, '__source'):
            self.__source = Factory.create(self, context)

        if hasattr(self.__source, 'on_init'):
            self.__source.on_init(context)

        self.kind = self.__source.kind

    def on_close(self, context):
        if hasattr(self.__source, 'on_close'):
            self.__source.on_close(context)

    def highlight(self):
        self.__source.highlight()

    def define_syntax(self):
        self.__source.define_syntax()

    def gather_candidates(self, context):
        if hasattr(self.__source, 'gather_candidates'):
            return self.__source.gather_candidates(context)
