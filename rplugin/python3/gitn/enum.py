# File: enum.py
# Author: kmnk <kmnknmk at gmail.com>
# License: MIT license

from enum import Enum, unique

class Window(Enum):
    current = 0
    tab     = 1
    split   = 2
    vsplit  = 3

    @classmethod
    def to_open_blank_command(cls, window):
        if window == cls.current: return 'enew'
        if window == cls.tab: return 'tabnew'
        if window == cls.split: return 'new'
        if window == cls.vsplit: return 'vnew'
        return 'enew'


@unique
class Status(Enum):
    unmodified = ' '
    modified   = 'M'
    added      = 'A'
    deleted    = 'D'
    renamed    = 'R'
    copied     = 'C'
    unmerged   = 'U'
    untracked  = '?'

    @classmethod
    def has_short(cls, short):
        if cls.unmodified.value == short: return True
        if cls.modified.value == short: return True
        if cls.added.value == short: return True
        if cls.deleted.value == short: return True
        if cls.renamed.value == short: return True
        if cls.copied.value == short: return True
        if cls.unmerged.value == short: return True
        if cls.untracked.value == short: return True
        return False

    @classmethod
    def by_short(cls, short):
        if cls.unmodified.value == short: return cls.unmodified
        if cls.modified.value == short: return cls.modified
        if cls.added.value == short: return cls.added
        if cls.deleted.value == short: return cls.deleted
        if cls.renamed.value == short: return cls.renamed
        if cls.copied.value == short: return cls.copied
        if cls.unmerged.value == short: return cls.unmerged
        if cls.untracked.value == short: return cls.untracked
