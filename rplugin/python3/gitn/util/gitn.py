# File: gitn.py
# Author: kmnk <kmnknmk at gmail.com>
# License: MIT license

from gitn.enum import Window

class Gitn:

    @staticmethod
    def highlight(vim, param):
        if not 'container' in param: return
        if not 'containees' in param: return

        container = param['container']
        if not 'name' in container: return
        if not 'pattern' in container: return

        vim.command('syntax match {0} /{1}/ contained keepend'
            .format(container['name'], container['pattern']))

        for containee in param['containees']:
            if not 'name' in containee: continue
            if not 'pattern' in containee: continue
            if not 'color' in containee: continue
            vim.command('syntax match {0} /{1}/ contained containedin={2} {3}'
                .format(
                    containee['name'],
                    containee['pattern'],
                    container['name'],
                    'nextgroup={0}'.format(containee['next']) if 'next' in containee else ''))
            vim.command('highlight default link {0} {1}'
                .format(containee['name'], containee['color']))

    @staticmethod
    def system(vim, command, option={}):
        if len(command) <= 0: return ''

        if 'confirm' in option and option['confirm'] and not Gitn.confirm(vim, command): return ''

        return vim.call('gitn#system', command)

    @staticmethod
    def termopen(vim, command, option={}):
        Gitn.open_window(vim, option)

        if 'confirm' in option and option['confirm'] and not Gitn.confirm(vim, command): return ''

        vim.call('termopen', command)

        if 'startinsert' in option and option['startinsert']:
            vim.command('startinsert')

    @staticmethod
    def open_window(vim, option={}):
        window = option['window'] if 'window' in option else Window.tab
        vim.command(Window.to_open_blank_command(window))

        if 'text' in option:
            vim.call('gitn#put', option['text'])
            vim.command('keepjumps normal gg')
            vim.command('delete')
        if 'filetype' in option: vim.command('setlocal filetype={0}'.format(option['filetype']))
        if 'buftype' in option: vim.command('setlocal buftype={0}'.format(option['buftype']))

    @staticmethod
    def confirm(vim, text):
        return vim.call('input', 'run it ?: {0} [y/n]'.format(text)) == 'y'

    # copy from denite.kind.base
    @staticmethod
    def yank(vim, text):
        vim.call('setreg', '"', text, 'v')
        if vim.call('has', 'clipboard'):
            vim.call('setreg', vim.eval('v:register'), text, 'v')
