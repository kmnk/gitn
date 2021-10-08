" File: gitn.py
" Author: kmnk <kmnknmk at gmail.com>
" License: MIT license

function! gitn#system(command)
  return system(a:command)
endfunction

function! gitn#put(string, ...)
  if a:0 > 0 && a:1
    put!=a:string
  else
    put=a:string
  endif
endfunction

function! gitn#current_branch()
  return system('git branch --show-current')
endfunction

" only for github repository
function! gitn#repository_name()
  let url = trim(system('git config --get remote.origin.url'))
  if match(url, 'https://github.com/') >= 0
    return url[19:-5]
  elseif match(url, 'git@github.com:') >= 0
    return url[15:-5]
  else
    return url
  endif
endfunction

function! gitn#get_head_hash()
  return trim(system('git rev-parse HEAD'))
endfunction
