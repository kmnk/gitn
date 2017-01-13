# File: log.py
# Author: kmnk <kmnknmk at gmail.com>
# License: MIT license

from gitn.util.gitn import Gitn
from denite.source.base import Base
from denite.process import Process
import os
import re
import time

DATE_GRAPH_HIGHLIGHT = {
    'container': {
        'name': 'gitnLog_dateGraphHeader',
        'pattern': '\\v((\d{4}\/\d{2}\/\d{2} \d{2}:\d{2} )| {16} )[*|\/\-\ ]+',
    },
    'containees': [
        {
            'name': 'gitnLog_date',
            'pattern': '\\v\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}',
            'color': 'Comment',
            'next': 'gitnLog_graph',
        },
        {
            'name': 'gitnLog_graph',
            'pattern': '\\v[*|\/\-\\ ]+',
            'color': 'Statement',
        },
    ],
}

AUTHOR_NAME_HIGHLIGHT = {
    'container': {
        'name': 'gitnLog_authorNameHeader',
        'pattern': '\\v:[^:]+: ',
    },
    'containees': [
        {
            'name': 'gitnLog_separator',
            'pattern': '\\v:',
            'color': 'Comment',
        },
        {
            'name': 'gitnLog_authorName',
            'pattern': '\\v[^:]+',
            'color': 'Type',
        },
    ],
}

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'gitn'
        self.kind = 'gitn_log'
        self.vars = {
            'command': ['git'],
            'action': ['log'],
            'default_opts': [
                '--date=default',
                '--graph',
                '--pretty=format:"%H","%P","%an","%ae","%ad","%at","%cn","%ce","%cd","%ct","%s"',
            ],
            'separator': ['--'],
        }

    def on_init(self, context):
        self.__proc = None

    def on_close(self, context):
        if self.__proc:
            self.__proc.kill()
            self.__proc = None

    def highlight(self):
        Gitn.highlight(self.vim, DATE_GRAPH_HIGHLIGHT)
        Gitn.highlight(self.vim, AUTHOR_NAME_HIGHLIGHT)

    def define_syntax(self):
        self.vim.command(
            'syntax region ' + self.syntax_name + ' start=// end=/$/ '
            'contains=gitnLog_dateGraphHeader,gitnLog_authorNameHeader,deniteMathced contained')

    def gather_candidates(self, context):
        if self.__proc:
            return self.__async_gather_candidates(context, 0.5)

        commands = []
        commands += self.vars['command']
        commands += self.vars['action']
        commands += self.vars['default_opts']
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
            result = self.__parse(line)
            if result:
                if 'subject' in result:
                    candidates.append({
                        'word': '{0} {1}: {2} : {3}'.format(
                            time.strftime('%Y/%m/%d %H:%M', time.gmtime(result['author']['time'])),
                            result['graph'],
                            result['author']['name'],
                            result['subject'],
                        ),
                        'action__log': result
                    })
                elif 'graph' in result:
                    candidates.append({
                        'word': '                 {0}'.format(result['graph'].strip()),
                    })

        return candidates

    def __parse(self, line):
        m = re.search(r'^([^"]+)(?:"([^"]*)","([^"]*)","([^"]*)","([^"]*)","([^"]*)","([^"]*)","([^"]*)","([^"]*)","([^"]*)","([^"]*)","([^"]*)")?$', line)
        if not m or not m.group(1): return {}

        if not m.group(8): return { 'graph': m.group(1) }

        [graph, own_hash, parent_hash, author_name, author_email, author_date, author_time, committer_name, committer_email, committer_date, committer_time, subject] = m.groups()

        return {
            'graph': graph,
            'subject': subject,
            'hash': {
                'own': own_hash,
                'parent': parent_hash,
            },
            'author': {
                'name': author_name,
                'email': author_email,
                'date': author_date,
                'time': int(author_time, 10),
            },
            'committer': {
                'name': committer_name,
                'email': committer_email,
                'date': committer_date,
                'time': int(committer_time, 10),
            },
        }
