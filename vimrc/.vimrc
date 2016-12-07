set nocompatible
filetype off
" vim 主题
" 显示行数，设置软回车和缩进还有语法
set number
"set smarttab
"set filetype=python
au BufNewFile,BufRead *.py,*.pyw setf python
set autoindent " same level indent
set smartindent " next level indent
set expandtab
set tabstop=4
set shiftwidth=4
set softtabstop=4
" 不加这个在OS X下面delete键用不了
set backspace=2

" 开启语法高亮功能
syntax enable
" 允许用指定语法高亮配色方案替换默认方案
syntax on

" 编码设置
set encoding=utf-8
set fileencodings=ucs-bom,utf-8,cp936
set fileencoding=utf-8
set termencoding=utf-8

" 基于缩进或语法进行代码折叠
set foldmethod=indent
set foldmethod=syntax
" 启动 vim 时关闭折叠代码
set nofoldenable

" 总是显示状态栏
set laststatus=2

" 显示光标当前位置
set ruler
" 高亮显示当前行/列
set cursorline
set cursorcolumn

" 高亮显示搜索结果
set hlsearch
set tw=80
colorscheme molokai

" vundle 插件管理

set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
Plugin 'VundleVim/Vundle.vim'
Plugin 'scrooloose/nerdtree'
Plugin 'motemen/git-vim'
Bundle 'scrooloose/syntastic'
Bundle 'majutsushi/tagbar'
Bundle 'bling/vim-airline'
" Plugin "Valloric/YouCompleteMe"
Bundle 'Raimondi/delimitMate'
Bundle 'kien/ctrlp.vim'
Plugin 'klen/python-mode'
Plugin 'fisadev/vim-isort'
" Plugin 'nvie/vim-flake8'
Bundle 'mattn/emmet-vim'
Bundle 'powerline/powerline'
Bundle 'tomasr/molokai'
" Bundle 'milkypostman/powerline'
"Plugin "hail2u/vim-css3-syntax"
"Plugin "pangloss/vim-javascript"
" Plugin "ap/vim-css-color"
Bundle "mileszs/ack.vim"
Bundle 'davidhalter/jedi-vim'
call vundle#end()
" airline 特殊符号
let g:airline_powerline_fonts = 1
let mapleader = ','
let g:jedi#goto_assignments_command = "<leader>g"
let g:jedi#goto_definitions_command = "<leader>d"


" 使用 NERDTree 插件查看工程文件。设置快捷键，速记：file list
" nmap <Leader>fl :NERDTreeToggle<CR>
nmap <F2> :NERDTreeToggle<CR>
" open nerdtree with the current file selected
nmap ,t :NERDTreeFind<CR>
nmap tb :Tagbar<cr>
" 设置NERDTree子窗口宽度
let NERDTreeWinSize=30
" 设置NERDTree子窗口位置
let NERDTreeWinPos="left"
" 显示隐藏文件
let NERDTreeShowHidden=0
" NERDTree 子窗口中不显示冗余帮助信息
let NERDTreeMinimalUI=1
" 删除文件时自动删除文件对应 buffer
let NERDTreeAutoDeleteBuffer=1
let NERDTreeIgnore=['\.pyc', '\.swp']
" nerdtree 放右边
" let NERDTreeWinPos=1
let tagbar_width=25

" Override go-to.definition key shortcut to Ctrl-]
let g:pymode_rope_goto_definition_bind = "<C-]>"
"
" " Override run current python file key shortcut to Ctrl-Shift-e
let g:pymode_run_bind = "<C-S-e>"
"
" " Override view python doc key shortcut to Ctrl-Shift-d
let g:pymode_doc_bind = "<C-S-d>""

" YCM 补全菜单配色
" 菜单
" highlight Pmenu ctermfg=White ctermbg=Black
" 选中项
" highlight PmenuSel ctermfg=Blue ctermbg=White
" 补全功能在注释中同样有效
" let g:ycm_complete_in_comments=1
" " 允许 vim 加载 .ycm_extra_conf.py 文件，不再提示
" let g:ycm_confirm_extra_conf=0
" " 开启 YCM 标签补全引擎
" let g:ycm_collect_identifiers_from_tags_files=1
" let g:ycm_filepath_completion_use_working_dir=1
" " 引入 C++ 标准库tags
" set tags+=/data/misc/software/misc./vim/stdcpp.tags
" " YCM 集成 OmniCppComplete 补全引擎，设置其快捷键
" " inoremap <leader>; <C-x><C-o>
" " 补全内容不以分割子窗口形式出现，只显示补全列表
set completeopt-=preview
" " 从第一个键入字符就开始罗列匹配项
" let g:ycm_min_num_of_chars_for_completion=1
" " 禁止缓存匹配项，每次都重新生成匹配项
" let g:ycm_cache_omnifunc=0
" " 语法关键字补全         
" let g:ycm_seed_identifiers_with_syntax=1
" let g:ycm_error_symbol = '>>'
" let g:ycm_warning_symbol = '>*'

let g:indent_guides_guide_size=1

" powerline
set rtp+=/usr/local/lib/python2.7/site-packages/powerline/bindings/bash/powerline.sh

" set t_Co=256

let g:minBufExplForceSyntaxEnable = 1

set guifont=Source\ Code\ Pro\ for\ Powerline:h12 
set noshowmode

" syntastic配置
" show list of errors and warnings on the current file
" nmap <leader>e :Errors<CR>
" turn to next or previous errors, after open errors list
" nmap <leader>n :lnext<CR>
" nmap <leader>p :lprevious<CR>
" check also when just opened the file
" let g:syntastic_check_on_open = 1
" syntastic checker for javascript.
" eslint is the only tool support JSX.
" If you don't need write JSX, you can use jshint.
" And eslint is slow, but not a hindrance
" let g:syntastic_javascript_checkers = ['jshint']
" let g:syntastic_javascript_checkers = ['eslint']
" don't put icons on the sign column (it hides the vcs status icons of signify)
" let g:syntastic_enable_signs = 0
" custom icons (enable them if you use a patched font, and enable the previous 
" setting)
" let g:syntastic_error_symbol = '✗'
" let g:syntastic_warning_symbol = '⚠'
" let g:syntastic_style_error_symbol = '✗'
" let g:syntastic_style_warning_symbol = '⚠'"
" \e 列出语法错误
" \n 列出下一个错误
" \p 列出前一个错误

autocmd BufNewFile *.py,*.sh exec ":call SetTitle()"
""定义函数SetTitle，自动插入文件头
func SetTitle()
    if &filetype == 'python'
        call setline(1, "\#!/usr/bin/env python") 
        call setline(2, "\# -*- encoding:utf-8 -*-") 
    endif
    if &filetype == 'sh'
        call setline(1, "\#!/usr/bin/sh") 
    endif
endfunc
