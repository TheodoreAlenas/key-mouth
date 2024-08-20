#!/bin/sh

set -e

bspc rule --add '*:emacs:*'   --one-shot desktop=^1
bspc rule --add 'firefox:*:*' --one-shot desktop=^2

tmux new-session -d -t key-mouth

ip="$(ip addr | sed -n 's|.*inet \(.*\)/24.*|\1|p')"

tmux new-window -t key-mouth:1
tmux send-keys  -t key-mouth:1 "export KEYMOUTH_UI=http://$ip:3000" C-m
tmux send-keys  -t key-mouth:1 "export KEYMOUTH_API=http://$ip:8000" C-m
tmux send-keys  -t key-mouth:1 "export KEYMOUTH_WS=ws://$ip:8000" C-m
tmux send-keys  -t key-mouth:1 "cd js" C-m
tmux send-keys  -t key-mouth:1 "npm run dev" C-m


tmux new-window -t key-mouth:2
tmux send-keys  -t key-mouth:2 "cd python" C-m
tmux send-keys  -t key-mouth:2 ". venv/bin/activate" C-m
tmux send-keys  -t key-mouth:2 "export KEYMOUTH_RAM_DB=yes" C-m
tmux send-keys  -t key-mouth:2 "export KEYMOUTH_CORS_ALL=yes" C-m
cmd="uvicorn main:app --host $ip --port 8000 --reload"
tmux send-keys  -t key-mouth:2 "$cmd" C-m

tmux new-window -t key-mouth:3
tmux send-keys  -t key-mouth:3 ". python/venv/bin/activate" C-m
tmux send-keys  -t key-mouth:3 "emacs" C-m

(firefox $ip:3000 2>&1 \
     | grep --line-buffered -v mesa_glthread \
            > git-ignores/logs-firefox.gitig) &

tmux select-window -t key-mouth:0
tmux attach-session -t key-mouth
