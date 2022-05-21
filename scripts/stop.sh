#!/bin/bash
SESSION=$USER

sessions=$(tmux ls | awk '{print $1}' | sed "s/://g")

for sess in $sessions
do
    tmux kill-session -t $sess
done