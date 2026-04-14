# GTA V Fishing Automation

A Python automation script for the fishing minigame in a GTA V roleplay server.

## How it works
- Uses `pyautogui` for screen-state detection via image recognition
- Monitors a bobber's colour state (green/yellow/red) in real time
- Automates mouse input to reel in fish at the correct moment
- Handles edge cases: fish escaping, timeouts, turtle events

## Tech
Python · pyautogui · pynput · win32api · computer vision · state machine logic

## Note
Built for a specific private RP server. Image assets (bobber reference images)
not included, these are screenshots taken from the game.
