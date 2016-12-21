# File: status.py
# Author: kmnk <kmnknmk at gmail.com>
# License: MIT license

from gitn.enum import Status
from denite.source.base import Base
from denite.process import Process
import os
import re

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

STATUS_SYNTAX = '''
syntax match gitn_status_line /\\v([^ ]+)? +!?([^ ]+)? *:/ contained keepend
'''.strip()

STATUS_UNMODIFIED_SYNTAX = (
    'syntax match gitn_status_unmodified '
    '/\-/ contained '
    'containedin=gitn_status_line')
STATUS_UNMODIFIED_HIGHLIGHT = 'highlight default link gitn_status_unmodified Comment'

STATUS_MODIFIED_SYNTAX = (
    'syntax match gitn_status_modified '
    '/Modified/ contained '
    'containedin=gitn_status_line')
STATUS_MODIFIED_HIGHLIGHT = 'highlight default link gitn_status_modified DiffChange'

STATUS_ADDED_SYNTAX = (
    'syntax match gitn_status_added '
    '/Added/ contained '
    'containedin=gitn_status_line')
STATUS_ADDED_HIGHLIGHT = 'highlight default link gitn_status_added DiffAdd'

STATUS_DELETED_SYNTAX = (
    'syntax match gitn_status_deleted '
    '/Deleted/ contained '
    'containedin=gitn_status_line')
STATUS_DELETED_HIGHLIGHT = 'highlight default link gitn_status_deleted DiffDelete'

STATUS_RENAMED_SYNTAX = (
    'syntax match gitn_status_renamed '
    '/Renamed/ contained '
    'containedin=gitn_status_line')
STATUS_RENAMED_HIGHLIGHT = 'highlight default link gitn_status_renamed DiffText'

STATUS_COPIED_SYNTAX = (
    'syntax match gitn_status_copied '
    '/Copied/ contained '
    'containedin=gitn_status_line')
STATUS_COPIED_HIGHLIGHT = 'highlight default link gitn_status_copied DiffText'

STATUS_UNMERGED_SYNTAX = (
    'syntax match gitn_status_unmerged '
    '/Unmerged/ contained '
    'containedin=gitn_status_line')
STATUS_UNMERGED_HIGHLIGHT = 'highlight default link gitn_status_unmerged ErrorMsg'

STATUS_UNTRACKED_SYNTAX = (
    'syntax match gitn_status_untracked '
    '/Untracked/ contained '
    'containedin=gitn_status_line')
STATUS_UNTRACKED_HIGHLIGHT = 'highlight default link gitn_status_untracked Comment'

STATUS_WORK_SYNTAX = (
    'syntax match gitn_status_work '
    '/ !/ contained '
    'containedin=gitn_status_line')
STATUS_WORK_HIGHLIGHT = 'highlight default link gitn_status_work Todo'

STATUS_SEPARATOR_SYNTAX = (
    'syntax match gitn_status_separator '
    '/:/ contained '
    'containedin=gitn_status_line')
STATUS_SEPARATOR_HIGHLIGHT = 'highlight default link gitn_status_separator Comment'

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'gitn'
        self.kind = 'gitn_status'
        self.vars = {
            'command': ['git'],
            'action': ['status'],
            'default_opts': ['-s'],
            'separator': ['--'],
            'final_opts': ['.'],
        }

    def on_init(self, context):
        self.__proc = None
        context['__directory'] = self.vim.call('expand', context['path'])

    def on_close(self, context):
        if self.__proc:
            self.__proc.kill()
            self.__proc = None

    def highlight(self):
        self.vim.command(STATUS_SYNTAX)
        self.vim.command(STATUS_UNMODIFIED_SYNTAX)
        self.vim.command(STATUS_UNMODIFIED_HIGHLIGHT)
        self.vim.command(STATUS_MODIFIED_SYNTAX)
        self.vim.command(STATUS_MODIFIED_HIGHLIGHT)
        self.vim.command(STATUS_ADDED_SYNTAX)
        self.vim.command(STATUS_ADDED_HIGHLIGHT)
        self.vim.command(STATUS_DELETED_SYNTAX)
        self.vim.command(STATUS_DELETED_HIGHLIGHT)
        self.vim.command(STATUS_RENAMED_SYNTAX)
        self.vim.command(STATUS_RENAMED_HIGHLIGHT)
        self.vim.command(STATUS_COPIED_SYNTAX)
        self.vim.command(STATUS_COPIED_HIGHLIGHT)
        self.vim.command(STATUS_UNMERGED_SYNTAX)
        self.vim.command(STATUS_UNMERGED_HIGHLIGHT)
        self.vim.command(STATUS_UNTRACKED_SYNTAX)
        self.vim.command(STATUS_UNTRACKED_HIGHLIGHT)
        self.vim.command(STATUS_WORK_SYNTAX)
        self.vim.command(STATUS_WORK_HIGHLIGHT)
        self.vim.command(STATUS_SEPARATOR_SYNTAX)
        self.vim.command(STATUS_SEPARATOR_HIGHLIGHT)
        self.vim.command('highlight default link deniteGrepInput Function')

    def define_syntax(self):
        self.vim.command(
            'syntax region ' + self.syntax_name + ' start=// end=/$/ '
            'contains=gitn_status_line contained')

    def gather_candidates(self, context):
        if self.__proc:
            return self.__async_gather_candidates(context, 0.5)

        commands = []
        commands += self.vars['command']
        commands += self.vars['action']
        commands += self.vars['default_opts']
        commands += self.vars['separator']
        commands += self.vars['final_opts']

        self.__proc = Process(commands, context, context['__directory'])
        return self.__async_gather_candidates(context, 2.0)

    def __async_gather_candidates(self, context, timeout):
        outs, errs = self.__proc.communicate(timeout=timeout)
        context['is_async'] = not self.__proc.eof()
        if self.__proc.eof():
            self.__proc = None

        candidates = []

        for line in outs:
            result = self.__parse_short_status(line, context)
            if result:
                [path, index, work] = result
                candidates.append({
                    'word': '{1:<9} {3:1}{2:<9}:{0}'.format(
                        os.path.relpath(path, start=context['__directory']),
                        TO_DISPLAY[index],
                        TO_DISPLAY[work],
                        '!' if work != Status.unmodified else ' '),
                    'action__path': path,
                    'action__line': 0,
                    'action__col': 0,
                })

        return candidates

    def __parse_short_status(self, line, context):
        m = re.search(r'^(.)(.)\s*(.+)$', line)
        if not m or not m.group(3):
            return []

        [index, work, path] = m.groups()

        if not os.path.isabs(path):
            path = context['__directory'] + '/' + path

        return [path, Status.by_short(index), Status.by_short(work)]
