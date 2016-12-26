# File: gitn_status.py
# Author: kmnk <kmnknmk at gmail.com>
# License: MIT license

from gitn.enum import Window
from gitn.util.gitn import Gitn

from .file import Kind as OpenableFile

class Kind(OpenableFile):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'gitn_status'
        self.default_action = 'open'

    def action_add(self, context):
        Gitn.system(self.vim, 'git add ' + self.__join(self.__to_paths(context['targets'])))
        Gitn.restart(self.vim, 'status', context)

    def action_reset_head(self, context):
        Gitn.system(self.vim, 'git reset HEAD ' + self.__join(self.__to_paths(context['targets'])))
        Gitn.restart(self.vim, 'status', context)

    def action_commit(self, context):
        Gitn.termopen(self.vim,
            'git commit ' + self.__join(self.__to_paths(context['targets'])),
            { 'startinsert': True })

    def action_commit_amend(self, context):
        Gitn.termopen(self.vim,
            'git commit --amend ' + self.__join(self.__to_paths(context['targets'])),
            { 'startinsert': True })

    def action_checkout(self, context):
        Gitn.system(self.vim, 'git checkout ' + self.__join(self.__to_paths(context['targets'])))
        Gitn.restart(self.vim, 'status', context)

    def action_diff(self, context):
        diff = Gitn.system(self.vim, 'git diff ' + self.__join(self.__to_paths(context['targets'])))
        if len(diff) > 0:
            Gitn.open_window(self.vim, {
                'window': Window.tab,
                'text': diff,
                'filetype': 'diff',
                'buftype': 'nofile',
            })

    def action_yank(self, context):
        Gitn.yank(self.vim, "\n".join([
            t['action__path'] for t in context['targets']
        ]))

    def action_diff_cached(self, context):
        diff = Gitn.system(self.vim, 'git diff --cached ' + self.__join(self.__to_paths(context['targets'])))
        if len(diff) > 0:
            Gitn.open_window(self.vim, {
                'window': Window.tab,
                'text': diff,
                'filetype': 'diff',
                'buftype': 'nofile',
            })

    def action_unstage(self, context): self.action_reset_head(context)
    def action_checkin(self, context): self.action_commit(context)
    def action_ci(self, context): self.action_commit(context)
    def action_ciam(self, context): self.action_commit_amend(context)
    def action_co(self, context): self.action_checkout(context)
    def action_di(self, context): self.action_diff(context)
    def action_dic(self, context): self.action_diff_cached(context)

    def __join(self, paths): return ' '.join(paths)

    def __to_paths(self, targets):
        return [t['action__path'] for t in targets]
