import os
import shutil
import subprocess
import sys
import time
import json
import ctypes
import signal
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TimeElapsedColumn, TimeRemainingColumn, TextColumn

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def restart_as_admin():
    script_path = os.path.abspath(sys.argv[0])
    params = f'"{script_path}" ' + " ".join([f'"{arg}"' for arg in sys.argv[1:]])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)

def kill_process_by_pid(pid):
    try:
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.OpenProcess(0x0001 | 0x0400 | 0x0010, False, pid)
        if handle:
            kernel32.TerminateProcess(handle, 0)
            kernel32.CloseHandle(handle)
            return True
    except:
        pass
    return False

def kill_process_by_name(name):
    try:
        subprocess.call(f"taskkill /F /T /IM \"{name}\" >nul 2>&1", shell=True)
        return True
    except:
        pass
    return False

def load_games_pool():
    cdn_url = "https://github.com/vexikoff/cdn/raw/refs/heads/main/frr/list.json"
    try:
        req = Request(cdn_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=10) as response:
            data = response.read().decode('utf-8')
            games = json.loads(data)
            if not isinstance(games, list) or not all('folder' in g and 'exe' in g for g in games):
                raise ValueError("Invalid CDN data format")
            return games
    except (URLError, HTTPError, json.JSONDecodeError, ValueError, TimeoutError) as e:
        console = Console()
        console.print(f"[bold red]CRITICAL: Failed to load games list from CDN.[/bold red]")
        console.print(f"[bold red]Error: {e}[/bold red]")
        console.print("[bold red]Check your internet connection or CDN availability.[/bold red]")
        input("\nPress Enter to exit...")
        sys.exit(1)

active_process = None
active_pid = None
active_exe_name = None
shutdown_flag = False

def cleanup_all():
    global active_process, active_pid, active_exe_name, shutdown_flag
    if shutdown_flag:
        return
    shutdown_flag = True
    if active_exe_name is not None:
        kill_process_by_name(active_exe_name)
        time.sleep(0.3)
    if active_pid is not None:
        kill_process_by_pid(active_pid)
        time.sleep(0.3)
    if active_process is not None:
        try:
            if active_process.poll() is None:
                active_process.terminate()
                time.sleep(0.3)
                if active_process.poll() is None:
                    active_process.kill()
                    time.sleep(0.3)
        except:
            pass
    active_process = None
    active_pid = None
    active_exe_name = None

def signal_handler(signum, frame):
    cleanup_all()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if sys.platform == "win32":
    def console_ctrl_handler(dwCtrlType):
        if dwCtrlType in (0, 2, 3):
            cleanup_all()
            time.sleep(0.5)
            return True
        return False
    try:
        handler_type = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_uint)
        ctypes.windll.kernel32.SetConsoleCtrlHandler(handler_type(console_ctrl_handler), True)
    except:
        pass

if __name__ == "__main__":
    if not is_admin():
        restart_as_admin()
        sys.exit()

console = Console()
GAMES_POOL = load_games_pool()

def main():
    global active_process, active_pid, active_exe_name

    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(Panel("Free Reward Routine", style="bold blue", border_style="blue"))

    # Определение пути к wind.exe внутри архива PyInstaller или в папке скрипта
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    
    wind_exe_source = os.path.join(base_path, "wind.exe")

    use_custom = Confirm.ask("\nUse custom .exe name instead of game list?", default=False)

    if use_custom:
        custom_exe_name = Prompt.ask("Enter custom .exe filename (e.g., MyGame.exe)")
        if not custom_exe_name.lower().endswith('.exe'):
            custom_exe_name += '.exe'
        game_folder_name = "CustomGame"
        game_exe_name = custom_exe_name
    else:
        display_list = GAMES_POOL

        while True:
            search_query = Prompt.ask("\nSearch by name (Enter = all, q = exit, c = custom)", default="")
            if search_query.lower() == 'q':
                cleanup_all()
                sys.exit(0)
            if search_query.lower() == 'c':
                custom_exe_name = Prompt.ask("Enter custom .exe filename (e.g., MyGame.exe)")
                if not custom_exe_name.lower().endswith('.exe'):
                    custom_exe_name += '.exe'
                game_folder_name = "CustomGame"
                game_exe_name = custom_exe_name
                break

            if search_query:
                display_list = [g for g in GAMES_POOL if search_query.lower() in g["folder"].lower() or search_query.lower() in g["exe"].lower()]
            else:
                display_list = GAMES_POOL

            if not display_list:
                console.print("[bold red]Nothing found. Try another query.[/bold red]")
                continue

            table = Table(title=f"Results ({len(display_list)} found)", show_header=True, header_style="bold magenta", border_style="cyan")
            table.add_column("ID", style="dim", width=5, justify="right")
            table.add_column("Game Name", style="cyan", no_wrap=False)
            table.add_column("Executable", style="green", no_wrap=False)

            for i, game in enumerate(display_list, 1):
                table.add_row(str(i), game["folder"], game["exe"])

            console.print(table)

            try:
                choice_input = Prompt.ask("\nEnter game ID to launch")
                if choice_input.lower() == 'q':
                    cleanup_all()
                    sys.exit(0)
                choice_idx = int(choice_input)
                if 1 <= choice_idx <= len(display_list):
                    selected_game = display_list[choice_idx - 1]
                    game_folder_name = selected_game["folder"]
                    game_exe_name = selected_game["exe"]
                    break
                else:
                    console.print("[bold red]ID out of range.[/bold red]")
            except ValueError:
                console.print("[bold red]Enter a valid number.[/bold red]")

    target_dirs = os.path.join(os.getenv('TEMP'), 'Free Rewards Routine')
    target_dir = os.path.join(target_dirs, game_folder_name)
    target_wind_path = os.path.join(target_dir, game_exe_name)

    console.print(f"\n[bold cyan]Selected: {game_exe_name}[/bold cyan]")

    duration_minutes = int(Prompt.ask("\nSet duration in minutes (1-60)", default="15"))
    duration_seconds = max(1, min(60, duration_minutes)) * 60

    try:
        os.makedirs(target_dir, exist_ok=True)
    except PermissionError:
        console.print("[bold red]ERROR: Access denied. Run as administrator.[/bold red]")
        cleanup_all()
        input("\nPress Enter to exit...")
        sys.exit()

    active_process = None
    active_pid = None
    active_exe_name = None

    try:
        # Всегда перезаписываем/копируем файл из временной папки сборки, чтобы гарантировать актуальность
        shutil.copy2(wind_exe_source, target_wind_path)
        console.print(f"[bold green]Payload placed: {target_wind_path}[/bold green]")

        active_process = subprocess.Popen(
            [target_wind_path, str(os.getpid())],
            cwd=target_dir,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

        active_pid = active_process.pid
        active_exe_name = game_exe_name

        time.sleep(1)

        console.print("[bold yellow]Window launched. Discord should detect activity.[/bold yellow]")

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        cleanup_all()
        input("\nPress Enter to exit...")
        sys.exit()

    console.print(Panel(f"Running for {duration_minutes} minutes. Process will auto-close when done.", border_style="green"))

    try:
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Waiting...", total=duration_seconds)
            while not progress.finished:
                time.sleep(1)
                progress.update(task, advance=1)
    finally:
        cleanup_all()
        time.sleep(1)

    console.print("\n[bold blue]Done. You can now claim your Discord reward.[/bold blue]")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    finally:
        cleanup_all()
        time.sleep(1)