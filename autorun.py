"""Start me and leave me to run

This checks every n hours if any exam information has
changed, changes are also logged in the exam_changes.log file
"""
import threading
import check_exams as exams
import sys


def check_for_updates(interval=3600, on_change_callback=None):
    """Checks for exam updates every 'interval' seconds
    If any exam data has changed sinced last check, then that data
    is passed through the callback function as:
        on_exam_change_callback(changed_data)

    The data variable here contains a list where each element in the list
    is a string saying what particularly was changed.
    """
    # Check for exam changes, run callback if changed data
    changed_data = exams.check()
    if changed_data and on_change_callback is not None:
        on_change_callback(changed_data)

    # Restart the thread timer to run again
    threading.Timer(interval, check_for_updates, [
                    interval, on_change_callback]).start()
    INTERVAL_AS_HOURS = interval / 60 / 60
    print('Running again in {0:.4f} hours'.format(INTERVAL_AS_HOURS))


if __name__ == '__main__':
    # The amount of seconds before re checking changes
    INTERVAL = 43200 if (len(sys.argv) != 2) else int(sys.argv[1])
    check_for_updates(INTERVAL, None)
