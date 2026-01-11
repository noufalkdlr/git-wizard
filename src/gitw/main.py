import typer
import subprocess
from rich.console import Console
import inquirer


app = typer.Typer(help="Git Wizard (gset) - Simple Git Automation Tool")
console = Console()


def run_git_command(command: list):
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        console.print(
            f"[bold red]Error running command:[/bold red] {' '.join(command)}"
        )
        console.print(f"[red]{e.stderr}[/red]")
        raise typer.Exit(code=1)


@app.command()
def config():
    """
    Configure global Git user name and email interactively.
    """
    console.print("[bold blue]🔧 Git Global Configuration Wizard[/bold blue]")

    name = typer.prompt("Enter your full name")
    email = typer.prompt("Enter your email")

    with console.status("[bold green]Setting up configuration...[/bold green]"):
        run_git_command(["git", "config", "--global", "user.name", name])
        run_git_command(["git", "config", "--global", "user.email", email])

    console.print("[bold green]✅ Configuration Updated Successfully![/bold green]")
    console.print("[dim]Current Global Config:[/dim]")

    current_config = run_git_command(["git", "config", "--global", "--list"])
    console.print(f"[cyan]{current_config}[/cyan]")


@app.command()
def push():
    """
    Push current directory changes to GitHub.
    Handles empty commits and push errors gracefully.
    """

    status = run_git_command(["git", "status", "--porcelain"])

    if not status:
        console.print("[yellow]Nothing to commit, working tree clean.[/yellow]")
        raise typer.Exit()

    commit_message = typer.prompt("Enter commit message")

    with console.status("[bold green]Processing...[/bold green]"):
        run_git_command(["git", "add", "."])
        run_git_command(["git", "commit", "-m", commit_message])

    try:
        with console.status("[bold green]Processing...[/bold green]"):
            result = subprocess.run(["git", "push"], capture_output=True, text=True)
        if result.returncode != 0:
            console.print("[bold red]Push Failed![/bold red]")
            console.print(f"[red]{result.stderr.strip()}[/red]")

            if "updates were rejected" in result.stderr.strip():
                console.print(
                    "[yellow]Hint: Try pulling changes first using 'git pull'[/yellow]"
                )

            elif "has no upstream branch" in result.stderr.lower():
                console.print(
                    "[yellow]Hint: No remote branch. Try 'git push --set-upstream origin main'[/yellow]"
                )

            raise typer.Exit(code=1)

        console.print("[bold green]✅ Successfully pushed to github[/bold green]")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error:[/bold red] {e.stderr}")


@app.command()
def connect():
    """
    onnect a newly created GitHub repository to the current local directory
    """

    def get_github_username():
        try:
            gh_result = subprocess.run(
                ["gh", "api", "user", "-q", ".login"],
                check=True,
                text=True,
                capture_output=True,
            )
            if gh_result.returncode == 0:
                return gh_result.stdout.strip()
        except FileNotFoundError:
            return None
        except subprocess.CalledProcessError:
            choice = typer.confirm("Do you want to setup Github CLI?")
            if choice:
                try:
                    gh_result = subprocess.run(["gh", "auth", "login"], check=True)
                    print("Successfully logged in to GitHub CLI")
                except subprocess.CalledProcessError as e:
                    console.print("Error running command", e.stderr)
            else:
                console.print("Operation cancelled!")

    def get_git_protocol():
        try:
            protocol_result = subprocess.run(
                ["gh", "config", "get", "git_protocol"], capture_output=True, text=True
            )
            if protocol_result.returncode == 0:
                return protocol_result.stdout.strip()
        except FileNotFoundError:
            return None
        except subprocess.CalledProcessError as e:
            print("GitHub CLI is installed but not authenticated")
            print(e.stderr)
            return None

    protocol = get_git_protocol()
    if not protocol:
        questions = [
            inquirer.List(
                "protocol",
                message="Select remote protocol",
                choices=["ssh", "https"],
            ),
        ]
        answer = inquirer.prompt(questions)
        if not answer:
            raise typer.Exit()
        protocol = answer["protocol"]

    username = get_github_username()

    if not username:
        username = typer.prompt("Enter username")

    repo_name = typer.prompt("Enter repo name")

    try:
        with console.status("Initializing repository..."):
            run_git_command(["git", "init"])
            run_git_command(["git", "add", "."])
            run_git_command(["git", "commit", "-m", "first commit"])
            run_git_command(["git", "branch", "-M", "main"])
            if protocol == "https":
                https = f"https://github.com/{username}/{repo_name}.git"
                run_git_command(["git", "remote", "add", "origin", https])
            elif protocol == "ssh":
                ssh = f"git@github.com:{username}/{repo_name}.git"
                run_git_command(["git", "remote", "add", "origin", ssh])
            run_git_command(["git", "push", "-u", "origin", "main"])
        console.print(
            "[bold green]Successfully connected and pushed to GitHub![/bold green]"
        )
    except KeyboardInterrupt:
        print("Operation cancelled")


if __name__ == "__main__":
    app()
