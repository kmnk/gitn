# File: gitn.py
# Author: kmnk <kmnknmk at gmail.com>
# License: MIT license

import os
import re
import sys

print(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from denite.source.base import Base

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'gitn'
        self.kind = 'gitn'

    def gather_candidates(self, context):
        # TODO
        return []
