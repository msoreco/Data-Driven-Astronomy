#
# Simple example connecting to PostreSQL database from Python.  Note will not
# be able to connect to db unles user creates it locally.
#

import psycopg2
import numpy as np

def column_stats(table, column):
    conn = psycopg2.connect(dbname='db', user='grok')
    cursor = conn.cursor()
    cursor.execute('select ' + column + ' from ' + table)
    results = cursor.fetchall()
    data = np.array(results)
    return data.mean(), np.median(data)

if __name__ == '__main__':
    print(column_stats('Planet', 'radius'))
