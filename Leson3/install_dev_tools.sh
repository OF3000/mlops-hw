#!/bin/bash
LOG_FILE="install.log"
# Використовуємо простіший метод логування для сумісності
exec > >(tee -a "$LOG_FILE") 2>&1

echo "--- Start: $(date) ---"

check_and_install() {
    if ! command -v "$1" &> /dev/null; then
        echo "Installing $1..."
        sudo apt-get update && sudo apt-get install -y $2
    else
        # Видалили [cite] та додали лапки для безпеки
        echo "$1 is already installed: $($1 --version | head -n 1)"
    fi
}

# Встановлення Docker та Compose
check_and_install "docker" "docker.io"
check_and_install "docker-compose" "docker-compose"

# Встановлення Python та pip
check_and_install "python3" "python3 python3-pip"

# Встановлення ML бібліотек
echo "Installing Python dependencies..."
# Використовуємо python3 -m pip для надійності
python3 -m pip install --upgrade pip
python3 -m pip install torch torchvision pillow Django

echo "--- Versions Check ---"
python3 --version
docker --version
python3 -m pip show torch | grep Version || echo "Torch not found"

echo "--- End: $(date) ---"