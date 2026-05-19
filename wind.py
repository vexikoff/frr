import os
import sys
import time
import ctypes
import threading

rpc = None
running = True

def is_process_alive(pid):
    try:
        handle = ctypes.windll.kernel32.OpenProcess(0x0400, False, pid)
        if not handle:
            return False
        exit_code = ctypes.c_ulong()
        ctypes.windll.kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code))
        ctypes.windll.kernel32.CloseHandle(handle)
        return exit_code.value == 259
    except:
        return False

def rpc_worker(game_name, parent_pid):
    global rpc, running
    try:
        from pypresence import Presence
    except ImportError:
        return

    CLIENT_ID = "1505505383723171871"
    rpc = Presence(CLIENT_ID)
    start_time = int(time.time())

    try:
        rpc.connect()
        while running:
            if parent_pid is not None and not is_process_alive(parent_pid):
                running = False
                break
            try:
                rpc.update(
                    state="Online",
                    details=f"Playing {game_name}",
                    large_image="default",
                    large_text=game_name,
                    small_image="default",
                    small_text="Free Reward Routine",
                    start=start_time,
                    buttons=[{"label": "Free Reward Routine", "url": "https://github.com/vexikoff/frr"}]
                )
            except Exception:
                pass
            
            for _ in range(15):
                if not running:
                    break
                time.sleep(1)
    except Exception:
        pass
    finally:
        if rpc is not None:
            try:
                rpc.close()
            except Exception:
                pass

def main():
    global running
    if getattr(sys, 'frozen', False):
        script_name = os.path.basename(sys.executable)
    else:
        script_name = os.path.basename(__file__)

    game_name = os.path.splitext(script_name)[0]
    ctypes.windll.kernel32.SetConsoleTitleW(game_name)

    parent_pid = None
    if len(sys.argv) > 1:
        try:
            parent_pid = int(sys.argv[1])
        except ValueError:
            pass

    try:
        import tkinter as tk
        root = tk.Tk()
        root.title(game_name)
        root.geometry("400x200")
        root.configure(bg='#ffffff')
        
        def check_parent():
            global running
            if parent_pid is not None and not is_process_alive(parent_pid):
                running = False
                root.quit()
                root.destroy()
                os._exit(0)
            else:
                root.after(200, check_parent)

        def on_close():
            global running
            running = False
            root.quit()
            root.destroy()
            os._exit(0)

        root.protocol("WM_DELETE_WINDOW", on_close)

        t = threading.Thread(target=rpc_worker, args=(game_name, parent_pid), daemon=True)
        t.start()

        root.after(200, check_parent)
        root.mainloop()
        
    except ImportError:
        t = threading.Thread(target=rpc_worker, args=(game_name, parent_pid), daemon=True)
        t.start()
        while running:
            if parent_pid is not None and not is_process_alive(parent_pid):
                running = False
                break
            time.sleep(0.2)
        os._exit(0)

if __name__ == "__main__":
    main()