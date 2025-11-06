#!/bin/bash

# Check if 'tree' is installed
if ! command -v tree &> /dev/null; then
    echo "❌ 'tree' command not found."
    
    # Detect package manager
    if command -v apt &> /dev/null; then
        echo "→ Install it using: sudo apt install tree"
    elif command -v dnf &> /dev/null; then
        echo "→ Install it using: sudo dnf install tree"
    elif command -v pacman &> /dev/null; then
        echo "→ Install it using: sudo pacman -S tree"
    else
        echo "⚠️  No supported package manager detected. Please install 'tree' manually."
    fi
    
    exit 1
fi

# If installed, generate the tree
echo "✅ 'tree' found. Generating directory structure..."
tree -I 'node_modules|venv|__pycache__' -a > tree.txt
echo "📄 Tree structure saved to tree.txt"
