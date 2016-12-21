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
