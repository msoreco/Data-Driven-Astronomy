import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
import time

#
# Function create_cat
#
# Creates a random catalogue
#
# args:
#   n - number of entries in the catalogue
#
# return:
#   2d array of randomly generated right ascension and declination pairs
#
def create_cat(n):
    ras = np.random.uniform(0, 360, size=(n, 1))
    decs = np.random.uniform(-90, 90, size=(n, 1))
    return np.hstack((ras, decs))

#
# Function crossmatch
#
# Uses astropy.coordinates.SkyCoord module to crossmatch objects in two catalogues. The
# SkyCoord module maps the catalogues into k-d trees internally in order to make the
# matching process much more efficient.
#
# args:
#   cat1, cat2 - the catalogues being matched
#   max_dist - maximum angular distance between matches
#
# return:
#   matches - list of matching pairs of objects, as a tuple (id of obj in cat1, id of obj
#             in cat2, distance)
#   no_matches - list of ids in cat1 for which no match was found
#   elapsed time to run cross-match algorithm
#
def crossmatch(cat1, cat2, max_dist):
    
    # Start timer
    start = time.perf_counter()

    # Create SkyCoords objects
    skycat1 = SkyCoord(cat1*u.degree, frame='icrs')
    skycat2 = SkyCoord(cat2*u.degree, frame='icrs')
        
    # Calculate closest pairs and distances
    (cat2_ids, dists_q, _) = skycat1.match_to_catalog_sky(skycat2)
    dists = dists_q.value
            
    # Initialize output lists
    matches = []
    no_matches = []

    # Perform crossmatch
    for i in range(0, len(cat1)):
        if dists[i] <= max_dist:
            matches.append((i, cat2_ids[i], dists[i]))
        else:
            no_matches.append(i)
                                
    # Return lists
    return matches, no_matches, time.perf_counter() - start



#
# __main__ execution exercises above code
#
if __name__ == '__main__':
    
    cat1 = np.array([[180, 30], [45, 10], [300, -45]])
    cat2 = np.array([[180, 32], [55, 10], [302, -44]])
    matches, no_matches, time_taken = crossmatch(cat1, cat2, 5)
    print('matches:', matches)
    print('unmatched:', no_matches)
    print('time taken:', time_taken)
    
    np.random.seed(0)
    cat1 = create_cat(100)
    cat2 = create_cat(200)
    matches, no_matches, time_taken = crossmatch(cat1, cat2, 5)
    print('matches:', matches)
    print('unmatched:', no_matches)
    print('time taken:', time_taken)


