# gitn
gitn is thin wrapper for using git on [Denite.nvim][denite] .

# Requirements
## Plugins
- [Denite.nvim][denite]
- [vim-fugitive][fugitive]

# Install
## by dein.vim
```vim
call dein#add('kmnk/gitn')
```

# Features
## `gitn_status`
Show `git status` results

## `gitn_log`
Show `git log` results

# TODO
- add `git branch` source and kind
- add `git remote` source and kind
- add `git config` source and kind

[denite]:https://github.com/Shougo/denite.nvim
[dein]:https://github.com/Shougo/dein.vim
[fugitive]:https://github.com/tpope/vim-fugitive
