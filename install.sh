#!/bin/sh

# REQUIREMENTS
# all:
# - bash or zsh
# - Mozilla Firefox
# server:
# - Python 3 (tested in 3.9.10)
# - geckodriver (tested in 0.30.0)
# client:
# - Node (tested in v17.7.1)
# - Yarn (tested in 1.22.17)

if [ -z "$ZSH_VERSION" -a -z "$BASH_VERSION" ]; then
    echo "please run $(basename $0) with zsh or bash."
    exit 1
fi

if [ $# -gt 1 ]; then
    echo "usage: $(basename $0) [all | server | client]"
    echo "too many arguments" 1>&2
    exit 1
fi

ROOT_DIR=`dirname $(realpath $0)`
VENV_DIR=$ROOT_DIR/server/.venv

print_bold() {
    printf "\\033[1m$1\\033[0m\n"
}

print_bold "initializing git submodules"
git -C $ROOT_DIR submodule update --init --recursive

if [ $# -eq 0 ] || [ "$1" = "all" ] || [ "$1" = "client" ]; then

    print_bold "\\033[34m\nCLIENT SETUP"
    print_bold "installing packages"
    yarn --cwd $ROOT_DIR/client

fi

if [ $# -eq 0 ] || [ "$1" = "all" ] || [ "$1" = "server" ]; then

    PY='/usr/bin/env python3'

    print_bold "\\033[34m\nSERVER SETUP"

    print_bold "compiling btm"
    make -C $ROOT_DIR/server/btm

    print_bold "initializing python environment"
    test -f $ROOT_DIR/server/.env || cp $ROOT_DIR/server/.env.example $ROOT_DIR/server/.env
    $PY -m venv --prompt 'weBlock-server' $VENV_DIR
    source $VENV_DIR/bin/activate
    source $ROOT_DIR/server/activate

    print_bold "installing modules"
    $PY -m pip install -r $ROOT_DIR/server/requirements.txt
    $PY -m pip install -r $ROOT_DIR/server/btm/script/requirements.txt

    print_bold "downloading nltk resources"
    read -r -d '' NLTK_DOWNLOAD <<- EOM
        import nltk.downloader;
        nltk.download('wordnet',       download_dir='$VENV_DIR/nltk_data');
        nltk.download('vader_lexicon', download_dir='$VENV_DIR/nltk_data');
        nltk.download('punkt',         download_dir='$VENV_DIR/nltk_data');
        nltk.download('stopwords',     download_dir='$VENV_DIR/nltk_data');
        nltk.download('omw-1.4',       download_dir='$VENV_DIR/nltk_data');
EOM
    $PY -c "$(echo $NLTK_DOWNLOAD)"
    print_bold "downloading gensim resources"
    # make dir because gensim thinks it doesn't have permission to do it
    test -d $VENV_DIR/gensim-data || mkdir $VENV_DIR/gensim-data
    $PY -m gensim.downloader --download 'word2vec-google-news-300'

fi

