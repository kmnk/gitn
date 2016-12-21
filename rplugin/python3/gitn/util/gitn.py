# File: gitn.py
# Author: kmnk <kmnknmk at gmail.com>
# License: MIT license

from gitn.enum import Window

class Gitn:

    @staticmethod
    def system(vim, command, option={}):
        if len(command) <= 0: return ''
        return vim.call('gitn#system', command)

    @staticmethod
    def termopen(vim, command, option={}):
        Gitn.open_window(vim, option)

        vim.call('termopen', command)

        if 'startinsert' in option and option['startinsert']:
            vim.command('startinsert')

    @staticmethod
    def restart(vim, command, context):
        # TODO: 実行時の mode その他のオプションの維持。 source の維持はどうするか
        vim.call(
            'denite#helper#call_denite',
            'Denite', '-mode={0} gitn:{1}'.format(context['mode'], command),
            context['firstline'], context['lastline'])

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
