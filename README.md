# JustTodoIt

Just a todo widget app.

![App preview](/docs/app_preview.png)

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python app.py
```

## Building an Executable

To create a standalone executable file:

### Windows

1. Ensure all dependencies are installed:

    ```bash
    pip install -r requirements.txt
    ```

2. Run the build script:

    ```powershell
    .\build_exe.ps1
    ```

3. The executable will be created in the `dist/` folder as `JustTodoIt.exe`

### Linux/macOS

1. Ensure all dependencies are installed:

    ```bash
    pip install -r requirements.txt
    ```

2. Make the script executable and run it:

    ```bash
    chmod +x build_exe.sh
    ./build_exe.sh
    ```

3. The executable will be created in the `dist/` folder as `JustTodoIt`

## How to Use

1. **Add a Task**: Type your task in the input field and press Enter or click "Add"
2. **Do the task!**
3. **Mark the task as done** Set the task as done by clicking the checkbox
4. **Delete Task**: Select a task and click "Delete Selected"
