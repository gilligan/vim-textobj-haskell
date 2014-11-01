if exists('g:loaded_textobj_haskell')
    finish
endif

if !exists('g:haskell_textobj_path')
    let plugins = split( globpath(&runtimepath, 'python/haskell-textobj.py'), '\n')
    if len( plugins ) > 0
        let g:haskell_textobj_path = plugins[0]
    else
        let g:haskell_textobj_path = 'haskell-textobj.py'
    endif
endif

if !exists('g:haskell_textobj_include_types')
    let g:haskell_textobj_include_types = 0
endif

python import vim
execute 'pyfile ' . g:haskell_textobj_path

call textobj#user#plugin('haskell', {
      \ '-': {
      \     'select-i': 'ih', '*select-i-function*': 'textobj#haskell#select_i',
      \     'select-a': 'ah', '*select-a-function*': 'textobj#haskell#select_a',
      \ },
    \})

let g:loaded_textobj_haskell = 1
