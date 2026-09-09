import sys
import os
import random

# Ensure safe UTF-8 output on Windows consoles
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QPoint, QEasingCurve, QSize
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QGraphicsDropShadowEffect,
    QFrame
)
from PyQt6.QtGui import QMovie, QColor, QFont, QGuiApplication

# ==========================================
# CONFIGURATION
# ==========================================
# Set TEST_MODE to True for 10-second test cycles, or False for standard 1-hour interval
TEST_MODE = False
INTERVAL_SECONDS = 10 if TEST_MODE else 60 * 60  # 1 hour = 3600 seconds

# Asset filenames (Custom Cartoon Girl from User Reference)
ASSET_WALK_LEFT = "walk_left.gif"
ASSET_DRINK = "drink.gif"
ASSET_WALK_RIGHT = "walk_right.gif"

# Fallback Emojis
FALLBACK_WALK_LEFT = "👧"
FALLBACK_DRINK = "🥤"
FALLBACK_WALK_RIGHT = "🏃‍♀️"

# Cute Dialogue Collections
REMINDER_MESSAGES = [
    "Take a tiny pause & sip some water! ✨",
    "I walked all the way here to bring you a sip! 🌸",
    "Stay cute, stay hydrated! 💧",
    "Time for a refreshing glass of water! 🥤",
    "Your skin & body will thank you! 🌸",
    "Glug glug! Let's drink together! 💖"
]

DRANK_FEEDBACK_MESSAGES = [
    "Yay! You're the best! 🎉",
    "Level up! Hydration +10 🌟",
    "Great job staying hydrated! Keep shining! ✨",
    "Woohoo! Hydration champion! 🏆",
    "So proud of you! See you next hour! 💖"
]

NOT_DRANK_FEEDBACK_MESSAGES = [
    "Don't forget next time! I'll be back to check! 🐾",
    "Take a sip when you're ready, okay? 🚰",
    "Your water glass misses you! Drink soon! 💧",
    "Promise to take a sip soon, okay? 🌸"
]

# UI Dimensions
WINDOW_WIDTH = 340
WINDOW_HEIGHT = 410
ANIMATION_DURATION_MS = 1500


class PetReminderOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.movie = None
        self.anim = None
        self.target_pos = QPoint(0, 0)
        self.offscreen_pos = QPoint(0, 0)
        
        self.init_window_flags()
        self.init_ui()
        self.calculate_positions()
        
        # Start in hidden offscreen position
        self.move(self.offscreen_pos)
        self.hide()

        # Interval Timer setup (1 hour / 3600s by default)
        self.interval_timer = QTimer(self)
        self.interval_timer.timeout.connect(self.trigger_reminder)
        self.interval_timer.start(INTERVAL_SECONDS * 1000)
        
        mode_str = "10s (TEST_MODE)" if TEST_MODE else "1 hour (3600s)"
        print(f"[Pet Reminder] Started main timer. Interval: {mode_str}.")

    def init_window_flags(self):
        """Configure completely frameless, stay-on-top, translucent overlay window."""
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
            | Qt.WindowType.SubWindow
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

    def init_ui(self):
        """Construct the vertical layout: Cartoon Girl on Top (100% transparent, no background circles) + Text Down Below."""
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(10, 0, 10, 10)
        root_layout.setSpacing(4)
        root_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ----------------- Top: Cartoon Girl Character (NO background circles/boxes) -----------------
        self.character_label = QLabel()
        self.character_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.character_label.setFixedSize(240, 280)
        self.character_label.setStyleSheet("background: transparent; border: none;")
        root_layout.addWidget(self.character_label, 0, Qt.AlignmentFlag.AlignHCenter)

        # ----------------- Down: Speech Bubble & Action Buttons -----------------
        self.bubble_frame = QFrame()
        self.bubble_frame.setObjectName("speechBubble")
        self.bubble_frame.setStyleSheet("""
            QFrame#speechBubble {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 255, 255, 0.96), stop:1 rgba(254, 242, 242, 0.94));
                border: 1.5px solid rgba(244, 114, 182, 0.6);
                border-radius: 16px;
            }
        """)
        
        # Add soft drop shadow to bottom speech bubble
        bubble_shadow = QGraphicsDropShadowEffect(self)
        bubble_shadow.setBlurRadius(20)
        bubble_shadow.setColor(QColor(244, 114, 182, 60))
        bubble_shadow.setOffset(0, 4)
        self.bubble_frame.setGraphicsEffect(bubble_shadow)

        bubble_layout = QVBoxLayout(self.bubble_frame)
        bubble_layout.setContentsMargins(14, 10, 14, 10)
        bubble_layout.setSpacing(8)

        # Message Text Label
        self.msg_label = QLabel(random.choice(REMINDER_MESSAGES))
        self.msg_label.setWordWrap(True)
        self.msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.msg_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.msg_label.setStyleSheet("color: #831843; background: transparent;")
        bubble_layout.addWidget(self.msg_label)

        # Action Buttons Layout
        self.btn_layout = QHBoxLayout()
        self.btn_layout.setSpacing(10)

        self.btn_drank = QPushButton("✓ Drank")
        self.btn_drank.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_drank.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:1 #059669);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 6px 14px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #34d399, stop:1 #10b981);
            }
            QPushButton:pressed {
                background: #047857;
            }
        """)
        self.btn_drank.clicked.connect(self.on_drank_clicked)

        self.btn_not_drank = QPushButton("✗ Not Drank")
        self.btn_not_drank.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_not_drank.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f43f5e, stop:1 #e11d48);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 6px 14px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #fb7185, stop:1 #f43f5e);
            }
            QPushButton:pressed {
                background: #be123c;
            }
        """)
        self.btn_not_drank.clicked.connect(self.on_not_drank_clicked)

        self.btn_layout.addWidget(self.btn_drank)
        self.btn_layout.addWidget(self.btn_not_drank)
        bubble_layout.addLayout(self.btn_layout)

        root_layout.addWidget(self.bubble_frame)

    def calculate_positions(self):
        """Compute off-screen starting point and bottom-right target point above taskbar."""
        screen = QGuiApplication.primaryScreen()
        avail_geo = screen.availableGeometry()

        margin_right = 24
        margin_bottom = 16

        target_x = avail_geo.x() + avail_geo.width() - WINDOW_WIDTH - margin_right
        target_y = avail_geo.y() + avail_geo.height() - WINDOW_HEIGHT - margin_bottom
        self.target_pos = QPoint(target_x, target_y)

        # Offscreen to the right
        offscreen_x = avail_geo.x() + avail_geo.width() + 40
        self.offscreen_pos = QPoint(offscreen_x, target_y)

    def set_character_state(self, gif_name: str, fallback_emoji: str):
        """Load GIF if present, otherwise cleanly display fallback emoji."""
        if self.movie:
            self.movie.stop()
            self.movie.deleteLater()
            self.movie = None

        script_dir = os.path.dirname(os.path.abspath(__file__))
        gif_path = os.path.join(script_dir, gif_name)

        if os.path.exists(gif_path):
            self.character_label.setText("")
            self.movie = QMovie(gif_path)
            self.movie.setScaledSize(QSize(240, 280))
            self.character_label.setMovie(self.movie)
            self.movie.start()
        else:
            # Fallback to emoji representation
            self.character_label.setMovie(None)
            self.character_label.setFont(QFont("Segoe UI Emoji", 48))
            self.character_label.setText(fallback_emoji)

    # ----------------- State Machine / Workflow -----------------

    def trigger_reminder(self):
        """Step 1: Walk in from offscreen right with random cute message."""
        chosen_message = random.choice(REMINDER_MESSAGES)
        print(f"[Pet Reminder] Triggering reminder: '{chosen_message}'. Girl walking in...")
        
        self.interval_timer.stop()
        self.calculate_positions()

        # Reset bubble state with new dialogue down below
        self.msg_label.setText(chosen_message)
        self.btn_drank.show()
        self.btn_not_drank.show()
        self.btn_drank.setEnabled(True)
        self.btn_not_drank.setEnabled(True)
        self.bubble_frame.show()

        # Step 1: Set walk-left animation state
        self.set_character_state(ASSET_WALK_LEFT, FALLBACK_WALK_LEFT)

        # Move to offscreen start and make window visible
        self.move(self.offscreen_pos)
        self.show()
        self.raise_()

        # Animate sliding into target position
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(ANIMATION_DURATION_MS)
        self.anim.setStartValue(self.offscreen_pos)
        self.anim.setEndValue(self.target_pos)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.finished.connect(self.step_action_in_place)
        self.anim.start()

    def step_action_in_place(self):
        """Step 2 & 3: In place, girl drinks water and waits for user response."""
        print("[Pet Reminder] Arrived in place. Drinking water & reminding...")
        if self.anim:
            self.anim.finished.disconnect(self.step_action_in_place)
        
        # Step 2: Swap to drink animation / emoji
        self.set_character_state(ASSET_DRINK, FALLBACK_DRINK)

    def on_drank_clicked(self):
        """Step 4: Feedback on Drank with random cute congratulations."""
        feedback = random.choice(DRANK_FEEDBACK_MESSAGES)
        self.handle_feedback(feedback)

    def on_not_drank_clicked(self):
        """Step 4: Feedback on Not Drank with encouraging message."""
        feedback = random.choice(NOT_DRANK_FEEDBACK_MESSAGES)
        self.handle_feedback(feedback)

    def handle_feedback(self, text: str):
        """Show feedback message, disable buttons, and trigger walk-out after 2 seconds."""
        print(f"[Pet Reminder] Feedback: {text}")
        self.msg_label.setText(text)
        self.btn_drank.setEnabled(False)
        self.btn_not_drank.setEnabled(False)

        # Step 5: After 2-second pause, walk out
        QTimer.singleShot(2000, self.step_walk_out)

    def step_walk_out(self):
        """Step 5: Swap to walk-right animation and slide offscreen."""
        print("[Pet Reminder] Walking out...")
        # Hide speech bubble while walking away
        self.bubble_frame.hide()

        # Swap character to walk right
        self.set_character_state(ASSET_WALK_RIGHT, FALLBACK_WALK_RIGHT)

        # Animate offscreen
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(ANIMATION_DURATION_MS)
        self.anim.setStartValue(self.pos())
        self.anim.setEndValue(self.offscreen_pos)
        self.anim.setEasingCurve(QEasingCurve.Type.InCubic)
        self.anim.finished.connect(self.on_walk_out_finished)
        self.anim.start()

    def on_walk_out_finished(self):
        """Finish walk-out: hide window and restart interval timer (1 hour)."""
        interval_desc = f"{INTERVAL_SECONDS}s" if TEST_MODE else "1 hour"
        print(f"[Pet Reminder] Offscreen. Sleeping for {interval_desc}.")
        if self.anim:
            self.anim.finished.disconnect(self.on_walk_out_finished)
        self.hide()
        # Restart interval timer for next cycle
        self.interval_timer.start(INTERVAL_SECONDS * 1000)


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Keep running background overlay

    overlay = PetReminderOverlay()

    # Trigger welcome walk-in after 1 second so user sees the reminder right away
    QTimer.singleShot(1000, overlay.trigger_reminder)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
