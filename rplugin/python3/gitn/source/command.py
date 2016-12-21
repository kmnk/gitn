# File: command.py
# Author: kmnk <kmnknmk at gmail.com>
# License: MIT license

from denite.source.base import Base

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.kind = 'command'

    def on_init(self, context):
        return
