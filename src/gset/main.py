import typer
import subprocess
from rich import print
from rich.console import Console


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
    Push changes (Dummy for now)
    """
    print("Push command coming soon!")


if __name__ == "__main__":
    app()
