#
# Simple demonstration of python code equivalent of SQL queries. Generally
# shows SQL syntax is simpler, especially for more complicated queries.
#

import numpy as np

#
# Equivalent of SQL query:
#
# SELECT kepler_id, radius
# FROM Star
# WHERE radius > 1.0;
#
def query1(file):
    data = np.loadtxt(file, usecols=[0, 2], delimiter=',')
    return data[data[:,1] > 1.0]

#
# Equivalent of SQL query:
#
# SELECT kepler_id, radius
# FROM Star
# WHERE radius > 1.0
# ORDER BY radius ASC;
#
def query2(file):
    select_out = np.loadtxt(file, usecols=[0, 2], delimiter=',')
    rgt1 = select_out[select_out[:,1] > 1.0]
    sorted_indices = np.argsort(rgt1[:,1])
    rgt1_asc = rgt1[sorted_indices]
    return rgt1_asc

#
# Equivalent of SQL query:
#
# SELECT p.radius/s.radius AS radius_ratio
# FROM Planet AS p
# INNER JOIN star AS s USING (kepler_id)
# WHERE s.radius > 1.0
# ORDER BY p.radius/s.radius ASC;
#
def query3(file1, file2):
    
    s = np.loadtxt(file1, usecols=[0, 2], delimiter=',')
    p = np.loadtxt(file2, usecols=[0, 5], delimiter=',')
    s_rgt1 = s[s[:,1] > 1.0]

    output = []
    for star in s_rgt1:
        for planet in p:
            if star[0] == planet[0]:
                output.append(planet[1]/star[1])
            
    arr_out = np.array(output)
    sorted_indices = np.argsort(arr_out)
    arr_out = arr_out[sorted_indices]
    return arr_out.reshape((len(arr_out), 1))

if __name__ == '__main__':

    # Test query1
    result = query1('stars.csv')
    print(result)

    # Test query2
    result = query2('stars.csv')
    print(result)

    # Test query3
    result = query3('stars.csv')
    print(result)
