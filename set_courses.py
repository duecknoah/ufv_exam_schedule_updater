"""Gets users input for their course numbers (CRNs), then storing it in
the CRNs.dat file for further use.
"""
import pickle

if __name__ == '__main__':
    do_start = input("Warning: This will reset any set CRNs from before, continue?\nyes(y) no(n): ")

    if (do_start == 'y' or do_start == 'yes'):
        uin = ''
        i = 1
        crns = []

        print('Enter your course numbers (CRNs), type \'done\' to finish.')
        while True:
            uin = input('CRN #{}: '.format(i))

            if uin == 'done':
                break

            try:
                crn = int(uin)
                crns.append(crn)
                i += 1
            except ValueError:
                print('Please enter a valid course number (CRN)')
        print(crns)
        print('{} courses set.'.format(i - 1))
        pickle.dump(crns, open('crns.dat', 'wb'))
        print('Saved, done.')
    else:
        print("Cancelling ...")