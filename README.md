# gitn
gitn is thin wrapper for using git on [Denite.nvim][denite] .

# Requirements
## Plugins
- [denite.nvim][denite]
- [vim-fugitive][fugitive]

# Install
## by dein.vim
```vim
call dein#add('kmnk/gitn', {'depends': ['Shougo/denite.nvim', 'tpope/vim-fugitive']})
```

# Features
## `gitn_status`
Show `git status` results

## `gitn_log`
Show `git log` results

## `gitn_branch`
Show `git branch` result

# TODO
- add `git remote` source and kind
- add `git config` source and kind

[denite]:https://github.com/Shougo/denite.nvim
[dein]:https://github.com/Shougo/dein.vim
[fugitive]:https://github.com/tpope/vim-fugitive
