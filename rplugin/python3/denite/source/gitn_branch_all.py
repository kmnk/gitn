# File: gitn_branch_all.py
# Author: kmnk <kmnknmk at gmail.com>
# License: MIT license

from gitn.util.gitn import Gitn
from denite.process import Process
import copy
import os
import re

from .gitn import Source as Base

HIGHLIGHT = {
    'container': {
        'name': 'gitn_branch_line',
        'pattern': '\\v([* ]) (.+)',
    },
    'containees': [
        {
            'name': 'gitn_branch_current',
            'pattern': '*',
            'color': 'Todo',
        },
        {
            'name': 'gitn_branch_default',
            'pattern': ' [^ ]\+',
            'color': 'Statement',
        },
        {
            'name': 'gitn_branch_remotes',
            'pattern': ' remotes\/origin\/[^ ]\+',
            'color': 'Special',
        },
        {
            'name': 'gitn_branch_origin',
            'pattern': ' origin\/[^ ]\+',
            'color': 'Statement',
        },
        {
            'name': 'gitn_branch_link',
            'pattern': ' \->',
            'color': 'Comment',
        },
    ]
}

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'gitn_branch_all'
        self.kind = 'gitn_branch'
        self.vars = {
            'command': ['git'],
            'action': ['branch'],
            'default_opts': ['--list', '--all'],
            'separator': ['--'],
        }

    def on_init(self, context):
        self.__proc = None

    def on_close(self, context):
        if self.__proc:
            self.__proc.kill()
            self.__proc = None

    def highlight(self):
        Gitn.highlight(self.vim, HIGHLIGHT)

    def define_syntax(self):
        self.vim.command(
            'syntax region ' + self.syntax_name + ' start=// end=/$/ '
            'contains=gitn_branch_line,deniteMatched contained')

    def gather_candidates(self, context):
        if self.__proc:
            return self.__async_gather_candidates(context, 0.5)

        opts = copy.copy(self.vars['default_opts'])
        if len(context['args']) > 0:
            args = context['args']
            if 'all' in args:
                opts += ['--all']

        commands = []
        commands += self.vars['command']
        commands += self.vars['action']
        commands += opts
        commands += self.vars['separator']

        self.__proc = Process(commands, context, self.vim.call('expand', context['path']))
        return self.__async_gather_candidates(context, 2.0)

    def __async_gather_candidates(self, context, timeout):
        outs, errs = self.__proc.communicate(timeout=timeout)
        context['is_async'] = not self.__proc.eof()
        if self.__proc.eof():
            self.__proc = None

        candidates = []

        for line in outs:
            result = self.__parse_branch(line, context)
            if result:
                [name, ref_name, is_current, is_remote, is_tracked] = result
                candidates.append({
                    'word': '{0} {1}{2}'.format(
                        '*' if is_current else ' ',
                        ref_name + ' -> ' if ref_name != '' else '',
                        name),
                    'action__name': name,
                })

        return candidates

    def __parse_branch(self, line, context):
        name = ''
        ref_name = ''
        current = ''
        is_current = False
        is_remote = False
        is_tracked = True

        m = False

        if not m:
            m = re.search(r'^([* ]) ([^ ]+)$', line)
            if m: [current, name] = m.groups()

        if not m:
            m = re.search(r'^([* ]) ([^ ]+) -> ([^ ]+)$', line)
            if m: [current, ref_name, name] = m.groups()

        if not m:
            m = re.search(r'^([* ]) ([(][^)]+[)])$', line)
            if m:
                [current, name] = m.groups()
                is_tracked = False

        is_current = current == '*'
        #is_remote = 

        return [name, ref_name, is_current, is_remote, is_tracked]
