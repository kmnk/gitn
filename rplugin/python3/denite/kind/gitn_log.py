# File: gitn_log.py
# Author: kmnk <kmnknmk at gmail.com>
# License: MIT license

from itertools import filterfalse

from gitn.enum import Window
from gitn.util.gitn import Gitn

from .base import Base

class Kind(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'gitn_log'
        self.default_action = 'yank'
        self.persist_actions += ['preview']
        self._previewed_target = {}
        self._preview_window_id = None

    def action_revert(self, context):
        targets = self.__sort_by_committer_time([t for t in context['targets'] if 'action__log' in t])

        if len(targets) == 0:
            return

        Gitn.termopen(self.vim,
            'git revert ' + self.__join(self.__to_hashes(targets)),
            { 'startinsert': True })
        pass

    def action_reset(self, context):
        targets = self.__sort_by_committer_time([t for t in context['targets'] if 'action__log' in t])

        if len(targets) == 0:
            return

        commit = targets[0]['action__log']['hash']['own']

        Gitn.termopen(self.vim,
            'git reset {0}'.format(commit),
            { 'startinsert': True })

    def action_reset_hard(self, context):
        targets = self.__sort_by_committer_time([t for t in context['targets'] if 'action__log' in t])

        if len(targets) == 0:
            return

        commit = targets[0]['action__log']['hash']['own']

        Gitn.termopen(self.vim,
            'git reset --hard {0}'.format(commit),
            { 'startinsert': True, 'confirm': True })

    def action_files(self, context):
        targets = [t for t in context['targets'] if 'action__log' in t]
        if len(targets) == 0:
            return
        elif len(targets) == 1:
            f = targets[0]['action__log']['hash']['own']
            t = targets[0]['action__log']['hash']['own']
        else:
            sorted_targets = self.__sort_by_committer_time(targets)
            f = sorted_targets[0]['action__log']['hash']['own']
            t = sorted_targets[-1]['action__log']['hash']['own']

        self.vim.call(
            'denite#helper#call_denite',
            'Denite', 'gitn_changed_files:{0}:{1}'.format(f, t),
            context['firstline'], context['lastline'])

    def action_diff(self, context):
        targets = [t for t in context['targets'] if 'action__log' in t]

        f, t = self.__resolve_diff_range(context)

        if not f or not t: return

        diff = Gitn.system(self.vim, 'git diff {0}..{1} -- {2}'.format(
            f,
            t,
            self.__join(self.__to_paths(targets))
        ))

        window = targets[0]['action__window']
        if len(diff) > 0:
            Gitn.open_window(self.vim, {
                'window': Window.by(window) if Window.has(window) else Window.tab,
                'text': diff,
                'filetype': 'diff',
                'buftype': 'nofile',
            })

    def action_yank(self, context):
        Gitn.yank(self.vim, "\n".join([
            t['action__log']['hash']['own'] for t in context['targets'] if 'action__log' in t
        ]))

    def action_preview(self, context):
        targets = [t for t in context['targets'] if 'action__log' in t]

        target = context['targets'][0]

        if (not context['auto_preview']
                and self.__get_preview_window()
                and self._previewed_target == target):
            self.vim.command('pclose!')
            self._preview_window_id = None
            return

        prev_id = self.vim.call('win_getid')

        # TODO: implement more beautiful .. !
        if (self._preview_window_id
                and self.vim.call('win_gotoid', self._preview_window_id) == 1):
            pass
        else:
            self.vim.command('pedit! gitn_log_temporary_file_for_preview') # ugly..
            self.vim.command('wincmd P')
            self.vim.command('enew')
            self.vim.command('setlocal filetype=diff')
            self.vim.command('setlocal buftype=nofile')
            self._preview_window_id = self.vim.call('win_getid')

        f, t = self.__resolve_diff_range(context)

        if f and t:
            self.vim.command('silent read !git diff {0}..{1} -- {2}'.format(
                f,
                t,
                self.__join(self.__to_paths(targets))
            ))
            self.vim.command('keepjumps normal! G')
            self.vim.command('keepjumps normal! gg')
            self.vim.command('delete')

        self.vim.call('win_gotoid', prev_id)
        self._previewed_target = target

    def __get_preview_window(self):
        return next(filterfalse(lambda x:
                                not x.options['previewwindow'],
                                self.vim.windows), None)

    def __resolve_diff_range(self, context):
        targets = [t for t in context['targets'] if 'action__log' in t]
        if len(targets) == 0:
            return (None, None)
        elif len(targets) == 1:
            f = targets[0]['action__log']['hash']['own'] + '^'
            t = targets[0]['action__log']['hash']['own']
        else:
            sorted_targets = self.__sort_by_committer_time(targets)
            f = sorted_targets[0]['action__log']['hash']['own'] + '^'
            t = sorted_targets[-1]['action__log']['hash']['own']

        return (f, t)

    def __sort_by_committer_time(self, targets):
        return sorted([t for t in targets if 'action__log' in t], key=lambda t: t['action__log']['committer']['time'])

    def __join(self, paths): return ' '.join(paths)

    def __to_paths(self, targets):
        return [t['action__path'] for t in targets if 'action__path' in t]

    def __to_hashes(self, targets):
        return [t['action__log']['hash']['own'] for t in targets if 'action__log' in t]
