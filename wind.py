import os
import sys
import time
import signal

rpc = None

def handle_exit(signum, frame):
    global rpc
    if rpc is not None:
        try:
            rpc.close()
        except Exception:
            pass
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

def main():
    global rpc
    try:
        from pypresence import Presence
    except ImportError:
        return

    if getattr(sys, 'frozen', False):
        script_name = os.path.basename(sys.executable)
    else:
        script_name = os.path.basename(__file__)

    game_name = os.path.splitext(script_name)[0]
    CLIENT_ID = "1505505383723171871"

    rpc = Presence(CLIENT_ID)
    start_time = int(time.time())

    try:
        rpc.connect()
        while True:
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
            time.sleep(15)
    except Exception:
        pass
    finally:
        if rpc is not None:
            try:
                rpc.close()
            except Exception:
                pass

if __name__ == "__main__":
    main()