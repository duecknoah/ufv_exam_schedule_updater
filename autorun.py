"""Start me and leave me to run

This checks every n hours if any exam information has
changed, changes are also logged in the exam_changes.log file
"""
import threading
import check_exams as exams
import sys

def check_for_updates(interval=43200):
    """Checks for exam updates every 'interval' seconds"""
    exams.check()
    threading.Timer(interval, check_for_updates, [interval]).start()
    INTERVAL_AS_HOURS = interval / 60 / 60
    print('Running again in {0:.4f} hours'.format(INTERVAL_AS_HOURS))

if __name__ == '__main__':
    # The amount of seconds before re checking changes
    INTERVAL = 43200 if (len(sys.argv) != 2) else int(sys.argv[1])
    check_for_updates(INTERVAL)