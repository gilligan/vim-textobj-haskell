if !has('python')
    echomsg "Warning: textobj-haskell requires python"
    finish
endif

function! textobj#haskell#select_i()
    if g:haskell_textobj_include_types == 0
        python selectIHaskellBinding(vim.current.buffer, vim.current.window.cursor[0], False)
    else
        python selectIHaskellBinding(vim.current.buffer, vim.current.window.cursor[0], True)
    endif

    let start_position = g:haskell_textobj_ret[0]
    let end_position = g:haskell_textobj_ret[1]
    return ['v', start_position, end_position]
endfunction

function! textobj#haskell#select_a()
    if g:haskell_textobj_include_types == 0
        python selectAHaskellBinding(vim.current.buffer, vim.current.window.cursor[0], False)
    else
        python selectAHaskellBinding(vim.current.buffer, vim.current.window.cursor[0], True)
    endif

    let start_position = g:haskell_textobj_ret[0]
    let end_position = g:haskell_textobj_ret[1]
    return ['v', start_position, end_position]
endfunction


