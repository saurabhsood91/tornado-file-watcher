### A Small Proof of Concept to watch for directory changes with a Tornado backend.

Watches for specified directories using either pyinotify or watchdog, running a Tornado backend

Set the directories to be watched in the `WATCH_DIRECTORIES` tuple in `settings.py`

To run with pyinotify, pass `--notifier=pyinotify`. Notifier defaults to watchdog
