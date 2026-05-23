# Free Reward Routine (FRR) v0.1r

Free Reward Routine (FRR) is a lightweight, automated Windows utility designed to help you claim Discord Quests and activity-based rewards without downloading, installing, or running heavy game clients.

By emulating specific game executables and leveraging Discord Rich Presence via a dual-process system, FRR safely simulates game activity, allowing your local Discord client to detect that you are playing the required game.

## 💻 Features

* Cloud-Synced Game List: Dynamically fetches the latest eligible games and their exact executable names from a remote database.
* Custom Spoofing Support: Allows you to manually type any .exe file name if a newly released quest game is not yet listed in the cloud database.
* Dual-Process Architecture: Spawns an isolated background game worker (wind.exe) inside a separate console window to ensure stable Discord detection.
* Automated Process Lifecycle: Constantly monitors the parent session. The spoofed game process automatically cleans up and terminates as soon as the countdown timer finishes.
* Clean Terminal UI: Powered by an advanced console wrapper providing clear tables, responsive prompts, and detailed visual progress bars.

## 🚀 How It Works

1. Privilege Request: The application automatically requests Administrator privileges on startup to handle Windows process mapping and internal binary deployment securely.
2. Game Matching: It downloads the active reward pool or lets you define a custom target game.
3. Payload Isolation: It dynamically copies its internal execution worker into a dedicated directory, renaming it to look identical to the target game.
4. Rich Presence Loop: The worker initializes an interface window (using standard Windows GUI components) and maintains a persistent application signal that Discord registers as active gameplay.

## 📋 Requirements

* Windows OS (7 / 10 / 11)
* Only 64bit system
* Discord Desktop Client (running and logged in)

## 🛠️ Installation & Quick Start

1. Go to the Releases page.
2. Download the latest frr.exe binary.
3. Simply launch frr.exe (the program will automatically request UAC/Admin rights if needed).
4. Select your desired game from the menu or type a custom executable name, set your duration, and let it run in the background.

## ⚠️ Disclaimer

This utility is intended for educational, research, and convenience purposes. Use it at your own discretion. This project is entirely independent and not officially affiliated with Discord or any game developers.
