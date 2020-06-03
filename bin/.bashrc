source ~/.bashrc
current_path=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
base_path=$(dirname $current_path)

# echo $base_path
export PS1=" \[\033[01;33m\](minimum)\[\033[00m\] $PS1"

alias dpa="docker ps -a"
alias xminimum="$current_path/minimum"
alias xcli="python3 $current_path/cli.py"
alias xmake="python3 $current_path/makefile.py"

export PATH="$PATH:$base_path/scripts"

