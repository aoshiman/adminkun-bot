#!/bin/bash
export LANG=ja_JP.utf-8
export ENV_NAME=adminkun-bot
export VIRTUALENV_PATH=$HOME/.virtualenvs/$ENV_NAME
source $VIRTUALENV_PATH/bin/activate
cd $HOME/dev/adminkun-bot
python ./adminkun.py tweet
exit
