# interface.py

from time import sleep
from colorama import Fore, init
from pyfiglet import figlet_format
from rich.console import Console

# Initialize colorama and rich
init(autoreset=True)
console = Console()

# Loading effect
def loading_animation():
    for i in range(8):
        console.print(f"[bold green]Loading DARKKING... {'█' * i}[/bold green]")
        sleep(0.2)

# Simulated hacking theme
def hacking_theme():
    console.print("[bold green]Initializing interface...[/bold green]")
    sleep(1)

# Show title screen
def show_title():
    console.print(figlet_format("DARKKING", font="slant"), style="bold cyan")
    console.print("[bold white]Made by [bold magenta]Dhani[/bold magenta]", justify="center")
    console.print("[green]Version:[/] v1.0 | [cyan]Owner:[/] [link=https://t.me/D4RK_KlNG]@D4RK_KlNG[/link]\n")

# Show menu
def show_menu():
    console.print("\n[bold green]=== TOOL MENU ===[/bold green]")
    console.print("[1] 4-Digit PIN Cracker")
    console.print("[0] Exit\n")
