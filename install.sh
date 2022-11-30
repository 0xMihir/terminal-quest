#!/bin/bash
git clone https://github.com/0xMihir/terminal-quest.git .terminal-quest-git
cd .terminal-quest-git || exit 
python3 setup.py install --user

if [[ "$SHELL" == *"bash"* ]]; then
    echo "export PATH=\"\$PATH:\$HOME/.local/bin\"" >> ~/.bashrc
    source ~/.bashrc
    echo "Wrote to ~/.bashrc"
    echo "To play, type terminal-quest in your terminal."
elif [[ "$SHELL" == *"zsh"* ]]; then
    echo "export PATH=\"\$PATH:\$HOME/.local/bin\"" >> ~/.zshrc
    source ~/.zshrc
    echo "Wrote to ~/.zshrc"
    echo "To play, type terminal-quest in your terminal."
else
    echo "Shell not supported. Please add \$HOME/.local/bin to your PATH variable."
fi

cd ..