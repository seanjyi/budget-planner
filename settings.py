'''
Handles dropdown and page sizes. Additionally,
can delete income and expense data.
'''

import sqlite3

connection = sqlite3.connect(':memory:') # change to 'data/budget.db'
