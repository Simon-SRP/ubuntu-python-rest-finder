#!/bin/bash

# Создаем папку Desktop если её нет
mkdir -p ~/Desktop

# Создаем .desktop файл
cat > ~/Desktop/RestFinder.desktop <<EOL
[Desktop Entry]
Name=Rest Finder
Comment=Приложение для поиска мест отдыха
Exec=$(pwd)/RestFinder.AppDir/AppRun
Icon=$(pwd)/RestFinder.AppDir/restfinder.png
Terminal=false
Type=Application
Categories=Utility;
EOL

# Даем права на выполнение
chmod +x ~/Desktop/RestFinder.desktop
chmod +x $(pwd)/RestFinder.AppDir/AppRun

echo "Ярлык создан на рабочем столе!"

