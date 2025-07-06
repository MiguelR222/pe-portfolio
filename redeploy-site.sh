#!/bin/bash
tmux kill-server

cd pe-portfolio

git fetch
git reset origin/main --hard

tmux new-session -s flask-dev -d \; \
    send-keys 'python3 -m venv python3-virtualenv' C-m \; \
    send-keys 'source python3-virtualenv/bin/activate' C-m \; \
    send-keys 'pip install -r requirements.txt' C-m \; \
    send-keys 'export FLASK_ENV=development' C-m \; \
    send-keys 'flask run --host=0.0.0.0' C-m

tmux attach-session -t flask-dev
