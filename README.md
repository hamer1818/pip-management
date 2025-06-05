# 🐍 Modern Pip Package Manager

A modern desktop application developed to manage your pip packages with a user-friendly interface. This tool aims to simplify the daily tasks of Python developers, such as listing, searching, installing, uninstalling, updating, and managing packages.

![Application Screenshot](/images/pip-paket-yoneticisi.png)
*Please update this section with a current screenshot of your application.*

---

## ✨ Features

This package manager brings the command-line interface of pip to a graphical interface with rich features:

### Installed Packages Management
- **List and Filter:** Instantly list all installed packages and easily filter them with the search box.
- **Detailed Information:** View the current version, latest version, and disk size (calculated with `pip show --files`) of packages.
- **One-Click Update:** Check for outdated packages and update a selected package or all of them with a single click.
- **Easy Uninstall:** Safely uninstall a selected package.
- **Package Details:** View the output of the `pip show` command in a separate window.
- **Export:** Export your list of installed packages in `requirements.txt`, `JSON`, or `CSV` formats.

### PyPI Package Search & Installation
- **Smart Search:** Search for packages directly on PyPI (Python Package Index).
- **Advanced Installation:** Install packages with popular options like `--upgrade`, `--user`, and `--no-deps`.
- **Specify Version:** Easily install a specific package version (`==`, `>=`, `<`, etc.).

### `requirements.txt` Management
- **Create and Edit:** Generate a `requirements.txt` file from your current environment or edit an existing one.
- **Bulk Install:** Install all packages from a `requirements.txt` file at once.

### Pip and System Operations
- **Update Pip:** Update pip itself to the latest version.
- **Clear Cache:** Clear pip's cache (`pip cache purge`) to save space.
- **Check for Broken Packages:** Detect broken or incompatible dependencies in your environment with `pip check`.

### Modern and User-Friendly Interface
- **Tabbed Layout:** All features are organized under neat tabs.
- **Dark Theme:** Features a modern, easy-on-the-eyes dark theme.
- **Asynchronous Operations:** Thanks to `threading`, long-running operations (like installing or listing packages) do not freeze the UI.
- **Status Notifications:** A status bar and operation logs provide real-time feedback on actions performed.

---

## 🚀 Installation and Usage

Follow the steps below to run the application on your local machine.

### Prerequisites
- **Python 3.x:** You must have Python 3 installed on your system.

### Steps
1.  **Clone the Project:**
    ```bash
    git clone https://github.com/hamer1818/pip-management.git
    cd pip-management
    ```
    *Note: Don't forget to replace `hamer1818/pip-management` with your own details.*

2.  **(Recommended) Create a Virtual Environment:**
    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:
    -   On Windows: `venv\\Scripts\\activate`
    -   On macOS/Linux: `source venv/bin/activate`

3.  **Run the Application:**
    To start the application, run the `main.py` file:
    ```bash
    python main.py
    ```

---

## 🛠️ Technical Stack

- **Language:** Python 3
- **GUI:** Tkinter (`tkinter.ttk` with custom styling)
- **Background-Processes:** Pip commands are executed using the `subprocess` module. All `subprocess` calls are managed in separate threads using `threading` to prevent the UI from freezing.
- **Modular Design:** The code is organized into a modular structure for better readability and maintainability:
    - `main.py`: The application's entry point.
    - `pip_manager/`: The main application package.
        - `app.py`: The main `ModernPipManager` class and orchestration.
        - `ui.py`: Functions for creating the Tkinter UI components.
        - `handlers.py`: Logic for handling events like button clicks.
        - `utils.py`: Utility functions (e.g., size calculation).

---

## 🤝 Contributing

Contributions will make the project better! Please follow these steps:

1.  **Fork** this repository.
2.  Create a new **branch** (`git checkout -b feature/new-feature`).
3.  **Commit** your changes (`git commit -am 'Add a new feature'`).
4.  **Push** your branch (`git push origin feature/new-feature`).
5.  Create a **Pull Request**.

---

## 📝 License

This project is licensed under the MIT License. See the `LICENSE` file for details. 