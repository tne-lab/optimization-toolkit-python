import numpy as np


def ts_armcount(bookV):
    # Arm selected count and arm selected
    bookV['playArmSelected'][bookV['trial']] = bookV['armselected']
    print(bookV['trial'])
    bookV['playArmSelected_count'][bookV['armselected']] += 1
    bookV['selection_probability'].append((bookV['playArmSelected_count'] / np.sum(
        bookV['playArmSelected_count'])).tolist())

    return bookV
