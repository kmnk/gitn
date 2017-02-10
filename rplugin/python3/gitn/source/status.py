# File: status.py
# Author: kmnk <kmnknmk at gmail.com>
# License: MIT license

from gitn.enum import Status
from gitn.util.gitn import Gitn
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

HIGHLIGHT = {
    'container': {
        'name': 'gitn_status_line',
        'pattern': '\\v([^ ]+)? +!?([^ ]+)? *:',
    },
    'containees': [
        {
            'name': 'gitn_status_unmodified',
            'pattern': '\-',
            'color': 'Comment',
        },
        {
            'name': 'gitn_status_modified',
            'pattern': 'Modified',
            'color': 'DiffChange',
        },
        {
            'name': 'gitn_status_added',
            'pattern': 'Added',
            'color': 'DiffAdd',
        },
        {
            'name': 'gitn_status_deleted',
            'pattern': 'Deleted',
            'color': 'DiffDelete',
        },
        {
            'name': 'gitn_status_renamed',
            'pattern': 'Renamed',
            'color': 'DiffText',
        },
        {
            'name': 'gitn_status_copied',
            'pattern': 'Copied',
            'color': 'DiffText',
        },
        {
            'name': 'gitn_status_unmerged',
            'pattern': 'Unmerged',
            'color': 'ErrorMsg',
        },
        {
            'name': 'gitn_status_untracked',
            'pattern': 'Untracked',
            'color': 'Comment',
        },
        {
            'name': 'gitn_status_work',
            'pattern': ' !',
            'color': 'Todo',
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

        self.name = 'gitn'
        self.kind = 'gitn_status'
        self.vars = {
            'command': ['git'],
            'action': ['status'],
            'default_opts': ['-s'],
            'separator': ['--'],
        }

    def on_init(self, context):
        self.__proc = None
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
            'contains=gitn_status_line,deniteMatched contained')

    def gather_candidates(self, context):
        if self.__proc:
            return self.__async_gather_candidates(context, 0.5)

        commands = []
        commands += self.vars['command']
        commands += self.vars['action']
        commands += self.vars['default_opts']
        commands += self.vars['separator']

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
                [paths, word, index, work] = result
                candidates.append({
                    'word': '{1:<9} {3:1}{2:<9}:{0}'.format(
                        os.path.relpath(word, start=context['__directory']),
                        TO_DISPLAY[index],
                        TO_DISPLAY[work],
                        '!' if work != Status.unmodified else ' '),
                    'action__path': paths[0],
                    'action__paths': paths,
                    'action__line': 0,
                    'action__col': 0,
                })

        return candidates

    def __parse_short_status(self, line, context):
        m = re.search(r'^(.)(.)\s*(.+)$', line)
        if not m or not m.group(3):
            return []

        [index, work, path] = m.groups()

        index_status = Status.by_short(index)
        work_status = Status.by_short(work)

        # TODO: refactor to more simple logic
        if index_status == Status.renamed:
            m = re.search(r'^(.+)\s+->\s+(.+)$', path)
            [path_from, path_to] = m.groups()
            paths = [p if not os.path.isabs(p) else context['__directory'] + '/' + p for p in [path_from, path_to]]
        else:
            paths = [p if not os.path.isabs(p) else context['__directory'] + '/' + p for p in [path]]

        return [paths, path, index_status, work_status]
