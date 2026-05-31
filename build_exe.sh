#!/bin/bash
# Run this script to generate the executable using PyInstaller

WITH_ICON=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --with-icon)
            WITH_ICON=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

if ! python3 -m pip show pyinstaller > /dev/null 2>&1; then
    echo "PyInstaller not found. Installing..."
    python3 -m pip install pyinstaller
fi

echo "Building JustTodoIt executable..."

BUILD_CMD="pyinstaller --onefile --windowed --name=JustTodoIt app.py"

if [ "$WITH_ICON" = true ] && [ -f "icon.ico" ]; then
    BUILD_CMD="$BUILD_CMD --icon=icon.ico"
    echo "Using custom icon..."
fi

eval $BUILD_CMD

if [ $? -eq 0 ]; then
    echo -e "\033[32mBuild successful! Executable located at: dist/JustTodoIt\033[0m"
else
    echo -e "\033[31mBuild failed!\033[0m"
    exit 1
fi
