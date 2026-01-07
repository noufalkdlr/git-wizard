
# Git Wizard (gset) 🧙‍♂️

A simple CLI tool to automate Git setup and streamline everyday version control tasks.

## 🚀 Features

- **Global Configuration**: Interactively set your global Git user name and email.
- **Smart Push**: Automatically stages changes, commits with a message, and pushes to the remote repository. Handles basic errors and suggests fixes.

## 📋 Requirements

- Python 3.9+
- Git installed and available in your system's PATH.

## 📦 Installation

You can install `gset` directly from GitHub using pip:

```bash
pip install git+https://github.com/yourusername/git-wizard.git
```

> **Note:** Replace `yourusername` with your actual GitHub username.

### For Development (Editable Install)

If you want to contribute or modify the code:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/git-wizard.git
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
gset --help
```

### 2. Configure Git (Global)
Set up your global git user.name and user.email interactively:
```bash
gset config
```

### 3. Push Changes
Stage all files, commit, and push in one go:
```bash
gset push
```


## 📄 License

This project is licensed under the GNU General Public License v3.0 (GPLv3). See the [LICENSE](LICENSE) file for details.

