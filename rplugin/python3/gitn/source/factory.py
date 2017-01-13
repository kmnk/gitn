# File: factory.py
# Author: kmnk <kmnknmk at gmail.com>
# License: MIT license

from gitn.source.status import Source as Status
from gitn.source.log import Source as Log
from gitn.source.command import Source as Command
from gitn.source.changed_files import Source as ChangedFiles

class Factory:

    @staticmethod
    def create(gitn_source, context):
        command = context['args'][0] if len(context['args']) > 0 else ''

        source = Factory.__create(command, gitn_source, context)

        source.name = gitn_source.name
        source.path = gitn_source.path
        if not source.syntax_name:
            source.syntax_name = gitn_source.syntax_name

        return source

    @staticmethod
    def __create(command, gitn_source, context):
        if command == 'status':
            return Status(gitn_source.vim)
        elif command == 'log':
            return Log(gitn_source.vim)
        elif command == 'changed_files':
            return ChangedFiles(gitn_source.vim)
        else:
            return Command(gitn_source.vim)
