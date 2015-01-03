if !has('python')
    echomsg "Warning: textobj-haskell requires python"
    finish
endif

function! textobj#haskell#select_i()
    python selectHaskellBinding(vim.current.buffer, vim.current.window.cursor[0])
    let start_position = g:haskell_textobj_ret[0]
    let end_position = g:haskell_textobj_ret[1]
    return ['v', start_position, end_position]
endfunction

