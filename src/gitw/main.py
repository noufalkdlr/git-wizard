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
    connect new created repo to local directory
    """

    def find_username():
        try:
            result = subprocess.run(
                ["gh", "api", "user", "-q", ".login"],
                check=True,
                text=True,
                capture_output=True,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except FileNotFoundError:
            return None
        except subprocess.CalledProcessError:
            while True:
                try:
                    choice = typer.prompt("Do you want to setup github cli? (y/n)")
                    if choice in ["y", "yes"]:
                        try:
                            result = subprocess.run(["gh", "auth", "login"])
                            if result.returncode == 0:
                                print("succsess fully loged in gh")
                                break
                            else:
                                print(result.stderr.strip())
                        except subprocess.CalledProcessError as e:
                            print("afs", e.stderr)
                            break
                    elif choice in ["n", "no"]:
                        print("operaton stoped")
                        break
                    else:
                        print("please select y or n or ctrl + c for quit")
                except KeyboardInterrupt:
                    print("operation cancelld by user")
                    return None

    def find_remote():
        try:
            result = subprocess.run(
                ["gh", "config", "get", "git_protocol"], capture_output=True, text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except FileNotFoundError:
            return None
        except subprocess.CalledProcessError as e:
            print("gh installed. Not login (remote)")
            print(e.stderr)
            return None

    if find_remote():
        remote = find_remote()

    else:
        questions = [
            inquirer.List(
                "protocol",
                message="Select remote protocol",
                choices=["ssh", "http"],
            ),
        ]
        answer = inquirer.prompt(questions)
        if not answer:
            raise typer.Exit()
        remote = answer["protocol"]

    if find_username():
        username = find_username()
    else:
        username = typer.prompt("Enter username")

    repo_name = typer.prompt("Enter repo name")

    run_git_command(["git", "init"])
    run_git_command(["git", "add", "."])
    run_git_command(["git", "commit", "-m", "'first commit'"])
    run_git_command(["git", "branch", "-M", "main"])
    if remote == "https":
        https = f"https://github.com/{username}/{repo_name}.git"
        run_git_command(["git", "remote", "add", "origin", https])
    elif remote == "ssh":
        ssh = f"git@github.com:{username}/{repo_name}.git"
        run_git_command(["git", "remote", "add", "origin", ssh])
    run_git_command(["git", "push", "-u", "origin", "main"])
    print("succsess")


if __name__ == "__main__":
    app()
