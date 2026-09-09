"""
Automated unit & integration tests for Miss India Desktop Pet Water Reminder overlay.
"""
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from PyQt6.QtTest import QTest
from main import (
    PetReminderOverlay,
    REMINDER_MESSAGES,
    DRANK_FEEDBACK_MESSAGES,
    NOT_DRANK_FEEDBACK_MESSAGES,
    INTERVAL_SECONDS
)

def test_full_flow():
    app = QApplication.instance() or QApplication(sys.argv)
    overlay = PetReminderOverlay()
    
    # 1. Trigger reminder & check random dialogue
    overlay.trigger_reminder()
    assert overlay.isVisible(), "Overlay should be visible on trigger"
    assert overlay.msg_label.text() in REMINDER_MESSAGES, f"Unexpected message: {overlay.msg_label.text()}"
    assert overlay.btn_drank.isEnabled()
    assert overlay.btn_not_drank.isEnabled()
    print(f"[PASS] Trigger test passed with dialogue: '{overlay.msg_label.text()}'")

    # 2. Simulate action in place
    overlay.step_action_in_place()
    print("[PASS] In-place action state passed (Miss India drinking water)")

    # 3. Test 'Drank' click feedback with random cute message
    overlay.on_drank_clicked()
    assert overlay.msg_label.text() in DRANK_FEEDBACK_MESSAGES, f"Unexpected drank feedback: {overlay.msg_label.text()}"
    assert not overlay.btn_drank.isEnabled()
    assert not overlay.btn_not_drank.isEnabled()
    print(f"[PASS] Drank feedback test passed with message: '{overlay.msg_label.text()}'")

    # 4. Test walk-out transition
    overlay.step_walk_out()
    assert not overlay.bubble_frame.isVisible()
    print("[PASS] Walk-out initiated test passed")

    # 5. Test walk-out finished
    overlay.on_walk_out_finished()
    assert not overlay.isVisible()
    assert overlay.interval_timer.isActive()
    print("[PASS] Walk-out completed and timer reset test passed")

    # 6. Test 'Not Drank' click feedback
    overlay.trigger_reminder()
    overlay.step_action_in_place()
    overlay.on_not_drank_clicked()
    assert overlay.msg_label.text() in NOT_DRANK_FEEDBACK_MESSAGES, f"Unexpected not-drank feedback: {overlay.msg_label.text()}"
    print(f"[PASS] Not Drank feedback test passed with message: '{overlay.msg_label.text()}'")

    # 7. Test fallback resilience when GIF is missing
    overlay.set_character_state("non_existent_file.gif", "💃")
    assert overlay.character_label.text() == "💃"
    print("[PASS] Missing GIF fallback resilience test passed (emoji 💃)")

    print("\n[SUCCESS] ALL MISS INDIA CHARACTER & LAYOUT TESTS PASSED!")

if __name__ == "__main__":
    test_full_flow()
