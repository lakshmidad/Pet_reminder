# 🐾 Desktop Pet & Water Reminder Overlay

A lightweight, background desktop pet utility for Windows and macOS built with Python and PyQt6.

## ✨ Features

- **Frameless & Translucent**: Seamlessly floats above your desktop/taskbar in the bottom-right corner without borders or background boxes.
- **Cute Character Animations**: Supports customizable animated GIFs (`walk_left.gif`, `drink.gif`, `walk_right.gif`).
- **Resilient Fallbacks**: If any GIF is missing or deleted, the app gracefully switches to emoji states (`🚶‍♀️`, `🥤`, `🏃‍♀️`) without crashing.
- **Glassmorphic Speech Bubble**: Modern UI with drop-shadows and vibrant responsive buttons (`[✓] Drank` and `[✗] Not Drank`).
- **Smooth Easing Animations**: Character slides into view and walks away using cubic easing curves.
- **Test Mode**: Instant 10-second timer for rapid testing, easily toggleable to 60 minutes for daily usage.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python main.py
```

---

## ⚙️ Configuration

In [main.py](file:///c:/Users/mindy/OneDrive/Desktop/Petreminder/main.py):

- **`TEST_MODE`**:
  - `True`: Triggers every **10 seconds** and launches an initial reminder immediately for demonstration.
  - `False`: Triggers every **60 minutes** (standard hydration interval).
- **Custom Assets**: Place your own `walk_left.gif`, `drink.gif`, and `walk_right.gif` in the project root folder.
