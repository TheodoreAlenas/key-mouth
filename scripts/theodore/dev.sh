#!/bin/sh

set -e

bspc rule --add '*:emacs:*'   --one-shot desktop=^1
bspc rule --add 'firefox:*:*' --one-shot desktop=^2

tmux new-session -d -t key-mouth

tmux new-window -t key-mouth:1
tmux send-keys  -t key-mouth:1 \
     "cd js && npm run dev" C-m

tmux new-window -t key-mouth:2
tmux send-keys  -t key-mouth:2 \
     "cd python && . venv/bin/activate && fastapi dev main.py" C-m

tmux new-window -t key-mouth:3
tmux send-keys  -t key-mouth:3 \
     "cd python && . venv/bin/activate && cd .. && emacs" C-m

(firefox localhost:3000 2>&1 \
     | grep --line-buffered -v mesa_glthread \
            > git_ignores/logs-firefox) &

tmux select-window -t key-mouth:0
tmux attach-session -t key-mouth
