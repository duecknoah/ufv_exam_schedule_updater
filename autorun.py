"""Start me and leave me to run

This checks every 12 hours if any exam information has
changed, and will notify via email the changes. Changes
are also logged in the updates.log file
"""
import threading
import check_exams as exams
import json

# The amount of seconds before re checking changes
INTERVAL = 43200

def check_for_updates():
    threading.Timer(INTERVAL, check_for_updates).start()
    exams.check()

check_for_updates()