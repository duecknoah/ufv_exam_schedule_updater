"""This is the main module to run. """
import ifttt_handler
import autorun

def start():
    autorun.check_for_updates(
        on_change_callback=ifttt_handler.post_exam_changes
    )

if __name__ == '__main__':
    print('Exam schedule checker starting ...')
    start()