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
        """switch branch to target
        """
        try:
            self.vim.command('Git checkout {0}'.format(context['targets'][0]['action__name']))
        except Exception as exc:
            # should handle fugitive error. but how ? X(
            pass

    def action_checkout(self, context): self.action_switch(context)

    def action_checkout_tracking(self, context):
        """switch tracking branch to target
        """
        try:
            self.vim.command('Git checkout -t {0}'.format(context['targets'][0]['action__name']))
        except Exception as exc:
            # should handle fugitive error. but how ? X(
            pass


    def action_rebase(self, context):
        """rebase on target branch
        """
        try:
            self.vim.command('Git rebase {0}'.format(context['targets'][0]['action__name']))
        except Exception as exc:
            # should handle fugitive error. but how ? X(
            pass

    def action_rebase_interactive(self, context):
        """rebase interactive on target branch
        """
        try:
            self.vim.command('Git rebase --interactive {0}'.format(context['targets'][0]['action__name']))
        except Exception as exc:
            # should handle fugitive error. but how ? X(
            pass

    def action_delete(self, context):
        """delete target branch
        """
        try:
            self.vim.command('Git branch -d {0}'.format(context['targets'][0]['action__name']))
        except Exception as exc:
            # should handle fugitive error. but how ? X(
            pass

    def action_delete_force(self, context):
        """delete force target branch
        """
        try:
            self.vim.command('Git branch -D {0}'.format(context['targets'][0]['action__name']))
        except Exception as exc:
            # should handle fugitive error. but how ? X(
            pass

    def action_create_from(self, context):
        """create new branch from target branch
        """
        from_branch_name = context['targets'][0]['action__name']
        new_branch_name = str(self.vim.call('denite#util#input',
                                            'Input new branch name:',
                                            '',
                                            ''))
        try:
            self.vim.command('Git checkout -b {0} {1}'.format(
                new_branch_name,
                from_branch_name
            ))
        except Exception as exc:
            # should handle fugitive error. but how ? X(
            pass

    def action_merge(self, context):
        """merge target branch to current branch
        """
        try:
            self.vim.command('Git merge {0}'.format(context['targets'][0]['action__name']))
        except Exception as exc:
            # should handle fugitive error. but how ? X(
            pass

    def action_merge_no_ff(self, context):
        """merge-no-fastforward target branch to current branch
        """
        try:
            self.vim.command('Git merge --no-ff {0}'.format(context['targets'][0]['action__name']))
        except Exception as exc:
            # should handle fugitive error. but how ? X(
            pass

    def action_merge_squash(self, context):
        """merge-squash target branch to current branch
        """
        try:
            self.vim.command('Git merge --squash {0}'.format(context['targets'][0]['action__name']))
        except Exception as exc:
            # should handle fugitive error. but how ? X(
            pass

