# File: gitn_changed_files.py
# Author: kmnk <kmnknmk at gmail.com>
# License: MIT license

from gitn.enum import Status
from gitn.util.gitn import Gitn
from denite.process import Process
import os
import re

from .gitn import Source as Base

TO_DISPLAY = {
    Status.unmodified : '-', # Unmodified
    Status.modified   : 'Modified',
    Status.added      : 'Added',
    Status.deleted    : 'Deleted',
    Status.renamed    : 'Renamed',
    Status.copied     : 'Copied',
    Status.unmerged   : 'Unmerged',
    Status.untracked  : 'Untracked',
}

HIGHLIGHT = {
    'container': {
        'name': 'gitn_change_files_line',
        'pattern': '\\v([^ ]+)? +!?([^ ]+)? *:',
    },
    'containees': [
        {
            'name': 'gitn_change_files_unmodified',
            'pattern': '\-',
            'color': 'Comment',
        },
        {
            'name': 'gitn_change_files_modified',
            'pattern': 'Modified',
            'color': 'DiffChange',
        },
        {
            'name': 'gitn_change_files_added',
            'pattern': 'Added',
            'color': 'DiffAdd',
        },
        {
            'name': 'gitn_change_files_deleted',
            'pattern': 'Deleted',
            'color': 'DiffDelete',
        },
        {
            'name': 'gitn_change_files_renamed',
            'pattern': 'Ranamed',
            'color': 'DiffText',
        },
        {
            'name': 'gitn_change_files_copied',
            'pattern': 'Copied',
            'color': 'DiffText',
        },
        {
            'name': 'gitn_change_files_unmerged',
            'pattern': 'Unmerged',
            'color': 'ErrorMsg',
        },
        {
            'name': 'gitn_change_files_untracked',
            'pattern': 'Untracked',
            'color': 'Comment',
        },
        {
            'name': 'gitn_status_separator',
            'pattern': ':',
            'color': 'Comment',
        },
    ]
}

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'gitn_changed_files'
        self.kind = 'file'
        self.vars = {
            'command': ['git'],
            'action': ['diff-tree'],
            'default_opts': ['-r', '--no-commit-id'],
            'ish': [],
        }

    def on_init(self, context):
        self.__proc = None

        if len(context['args']) < 2: return

        self.vars['ish'] = ['{0}^..{1}'.format(context['args'][0], context['args'][1])]

        context['__directory'] = self.vim.call('expand', context['path'])

    def on_close(self, context):
        if self.__proc:
            self.__proc.kill()
            self.__proc = None

    def highlight(self):
        Gitn.highlight(self.vim, HIGHLIGHT)

    def define_syntax(self):
        self.vim.command(
            'syntax region ' + self.syntax_name + ' start=// end=/$/ '
            'contains=gitn_change_files_line,deniteMatched contained')

    def gather_candidates(self, context):
        if self.__proc:
            return self.__async_gather_candidates(context, 0.5)

        commands = []
        commands += self.vars['command']
        commands += self.vars['action']
        commands += self.vars['default_opts']
        commands += self.vars['ish']

        self.__proc = Process(commands, context, context['__directory'])

        return self.__async_gather_candidates(context, 2.0)

    def __async_gather_candidates(self, context, timeout):
        outs, errs = self.__proc.communicate(timeout=timeout)
        context['is_async'] = not self.__proc.eof()
        if self.__proc.eof():
            self.__proc = None

        candidates = []

        for line in outs:
            result = self.__parse(line, context)
            if result:
                [path, status] = result
                candidates.append({
                    'word': '{1:<9}:{0}'.format(
                        os.path.relpath(path, start=context['__directory']),
                        TO_DISPLAY[status]),
                    'action__path': path,
                    'action__line': 0,
                    'action__col': 0,
                })

        return candidates

    def __parse(self, line, context):
        m = re.search(r':([^ ]+) ([^ ]+) ([^ ]+) ([^ ]+) (.)\t([^	]+)\t?(.+)?$', line)
        if not m or not m.group(6): return []

        [src_mode, dst_mode, src_commit, dst_commit, status, src_path, dst_path] = m.groups()

        if not os.path.isabs(src_path):
            path = context['__directory'] + '/' + src_path

        return [path, Status.by_short(status)]
