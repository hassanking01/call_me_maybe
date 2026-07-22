"""
Educational demonstration of Rich visual features:
1. Console.status (Spinners / Loading indicators)
2. rich.progress.track (Progress bars)
3. rich.live.Live (Real-time live updating displays)

This file demonstrates generic patterns using simulated tasks (time.sleep)
so you can observe how terminal state, context managers, and rendering work.
"""

import time
from rich.console import Console
from rich.progress import track
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

console = Console()

def demo_status_spinner():
    """
    CONCEPT 1: Console.status Context Manager
    -----------------------------------------
    - 'console.status' creates a background animated spinner.
    - Python's 'with' block ensures the spinner starts when entering
      and automatically stops/clears when leaving the block.
    """
    console.print("[bold blue]=== Concept 1: Status Spinner ===[/bold blue]")
    
    # Simulate a long computation (e.g., model inference or token processing)
    with console.status("[bold green]Processing items with spinner...[/bold green]", spinner="dots"):
        for i in range(5):
            time.sleep(0.5)  # Simulated work
            
    console.print("[bold check]Done![/bold check] Spinner stopped when exiting the 'with' block.\n")


def demo_progress_bar():
    """
    CONCEPT 2: rich.progress.track
    ------------------------------
    - 'track' wraps any iterable (list, range, generator).
    - On each iteration of the loop, Rich updates a progress bar,
      percentage, and time estimates in the terminal.
    """
    console.print("[bold blue]=== Concept 2: Progress Tracking ===[/bold blue]")
    
    items = ["Task A", "Task B", "Task C", "Task D"]
    
    # 'track' automatically monitors iteration progress
    for item in track(items, description="[cyan]Iterating sequence...[/cyan]"):
        time.sleep(0.4)  # Simulated work per item
        
    console.print("[bold check]Completed tracking sequence![/bold check]\n")


def demo_live_display():
    """
    CONCEPT 3: rich.live.Live
    -------------------------
    - 'Live' creates a region in the terminal that can be updated in-place.
    - Instead of printing new lines repeatedly, it redraws the same visual element.
    """
    console.print("[bold blue]=== Concept 3: Live Real-Time Updates ===[/bold blue]")
    
    # Create an initial renderable object (Panel with Text)
    display_text = Text("Starting live output...")
    panel = Panel(display_text, title="Live Dynamic Region", border_style="magenta")
    
    # The Live context manager handles overwriting lines cleanly
    with Live(panel, refresh_per_second=4) as live:
        for step in range(1, 6):
            time.sleep(0.5)
            # Update the underlying content structure
            display_text.append(f"\nAdded token/step #{step}")
            # Refresh the live panel in terminal
            live.update(Panel(display_text, title=f"Live Dynamic Region (Step {step}/5)", border_style="magenta"))
            
    console.print("[bold check]Live updating finished![/bold check]\n")


if __name__ == "__main__":
    demo_status_spinner()
    demo_progress_bar()
    demo_live_display()
