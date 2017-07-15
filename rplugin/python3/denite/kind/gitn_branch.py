# File: gitn_branch.py
# Author: kmnk <kmnknmk at gmail.com>
# License: MIT license

from gitn.enum import Window
from gitn.util.gitn import Gitn

from .file import Kind as OpenableFile

class Kind(OpenableFile):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'gitn_branch'
        self.default_action = 'switch'

    def action_switch(self, context):
        Gitn.system(self.vim, 'git checkout ' + context['targets'][0]['action__name'])
