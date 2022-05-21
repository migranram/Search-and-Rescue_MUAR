#!/usr/bin/bash
session=${USER}_SESSION

tmux -2 new-session -d -s $session

# Create roscore 
# send-keys writes the string into the sesssion (-t -> target session , C-m -> press Enter Button)
tmux new-window -t $session:0 -n 'gazebo'
tmux send-keys -t $session:0 "roslaunch sar_simulations no_gui.launch" C-m

sleep 5

tmux new-window -t $session:1 -n 'slam'
tmux send-keys -t $session:1 "roslaunch sar_SLAM hector_slam.launch" C-m

tmux new-window -t $session:2 -n 'move_base'
tmux send-keys -t $session:2 "roslaunch sar_SLAM move_base.launch" C-m

echo Finished!

tmux attach -t $session:0