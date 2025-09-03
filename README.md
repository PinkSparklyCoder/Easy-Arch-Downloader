# Easy-Arch-Downloader
A simple ISO downloader for Arch Linux ISO
# Arch Linux ISO Downloader

A small Python utility that discovers Arch Linux mirrors, ranks them by responsiveness, and downloads the latest ISO with resume, progress and a simple GUI. The same utilities are available from a command-line mode.

Key code references
- Script: [arch downloader.py](arch downloader.py)  
- GUI entrypoint: [`main_gui`](arch downloader.py)  
- CLI entrypoint: [`main_cli`](arch downloader.py)  
- Mirror discovery: [`get_mirrors`](arch downloader.py)  
- Country detection: [`get_country`](arch downloader.py)  
- Find latest ISO on a mirror: [`get_latest_iso_url`](arch downloader.py)  
- Robust downloader (resume, progress, cancel): [`download_iso`](arch downloader.py)

Why this is useful
- Automatically finds nearby Arch Linux mirrors and ranks them by responsiveness so downloads are faster and more reliable.  
- Supports HTTP Range resume so interrupted downloads can be continued without restarting from zero.  
- Provides both a graphical interface for users who prefer buttons and progress bars and a CLI mode for scripting or advanced use.  
- Shows live download speed and ETA, and performs a basic free-space check before downloading.

Main features
- Mirror discovery and ranking (responsiveness test).  
- Auto-detection of country to filter mirrors.  
- ISO discovery on a selected mirror (parses mirror listing).  
- Download with resume support, periodic speed updates and cancellation.  
- Simple GUI with language translations and a determinate/indeterminate progress bar.  
- CLI mode for interactive mirror selection and console progress.

Dependencies
- Python 3.7+  
- requests  
- tqdm  
- tkinter (commonly included with system Python)

Basic usage
- Start the GUI (default behavior): run the script; the GUI auto-refreshes and lists ranked mirrors. See [`main_gui`](arch downloader.py).  
- CLI mode: run the script with the --cli flag to use the interactive command-line flow. See [`main_cli`](arch downloader.py).

Troubleshooting
- Network or mirror failures are logged; check runtime logs produced by the script for detailed exceptions.  
- If a server does not support HTTP Range, the downloader falls back to re-downloading the file. Progress and resume behavior are implemented in [`download_iso`](arch downloader.py).

Notes for contributors
- Mirror list retrieval and parsing are centralized so improving parsing or adding alternate sources is straightforward. See [`get_mirrors`](arch downloader.py) and [`get_latest_iso_url`](arch downloader.py).  
- Download logic is isolated in [`download_iso`](arch downloader.py), making it easy to add features such as checksum verification or parallel downloading.

License
- No license specified. Add a LICENSE file to clarify
