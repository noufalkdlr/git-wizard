
# Git Wizard (gitw) 🧙‍♂️

A simple CLI tool to automate Git setup and streamline everyday version control tasks.

## 🚀 Features

- **Global Configuration**: Interactively set your global Git user name and email.
- **Smart Push**: Automatically stages changes, commits with a message, and pushes to the remote repository. Handles basic errors and suggests fixes.

## 📋 Requirements

- Python 3.9+
- Git installed and available in your system's PATH.

## 📦 Installation

### PyPI

You can install `git-wizard` directly from PyPI using pip:
```bash
pip install git-wizard
```

### AUR (Arch Linux)

Install from the AUR using `yay`:
```bash
yay -S git-wizard
```
> **Note**: This package depends on `python-inquirer`, which is available in the AUR. Using an AUR helper like `yay` or `paru` is recommended to handle dependencies automatically. If you are building manually, please ensure `python-inquirer` is installed first.

### Debian/Ubuntu (.deb)

Download the latest `.deb` release from the [Releases page](https://github.com/noufalkdlr/git-wizard/releases).
```bash
sudo apt install ./git-wizard_*.deb
```

### Fedora/RedHat (.rpm)

Download the latest `.rpm` release from the [Releases page](https://github.com/noufalkdlr/git-wizard/releases).
```bash
sudo dnf install ./git-wizard-*.rpm
```

### For Development (Editable Install)

If you want to contribute or modify the code:

1. Clone the repository:
   ```bash
   git clone https://github.com/noufalkdlr/git-wizard.git
   cd git-wizard
   ```

2. Create a virtual environment and install:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -e .
   ```

## 💻 Usage

### 1. Help Command
View all available commands and options:
```bash
gitw --help
```

### 2. Configure Git (Global)
Set up your global git user.name and user.email interactively:
```bash
gitw config
```

### 3. Push Changes
Stage all files, commit, and push in one go:
```bash
gitw push
```

### 4. Connect Repository
Initialize a local repository, create a commit, and push to GitHub in a single command. It supports both SSH and HTTPS protocols and integrates with GitHub CLI for seamless authentication.
```bash
gitw connect
```
> 💡 **Pro Tip:** Install [GitHub CLI](https://cli.github.com/) (`gh`) for the best experience. It allows `git-wizard` to automatically detect your GitHub username and preferred protocol (SSH/HTTPS), skipping those prompts!



## 📄 License

This project is licensed under the GNU General Public License v3.0 (GPLv3). See the [LICENSE](LICENSE) file for details.

