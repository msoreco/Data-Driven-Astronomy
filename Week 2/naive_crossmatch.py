import numpy as np

#
# Function hms2dec
#
# Converts right ascension in hours/min/sec to decimal degrees
#
# args:
#   h - hours
#   m - minutes
#   s - seconds
#
# returns:
#   right ascension in decimal degrees
#
def hms2dec(h, m, s):
  return (dms2dec(h, m, s)/24)*360

#
# Function dms2dec
#
# Converts value in deg/min/sec to decimal degrees.  Used for both
# declination values, and right ascension values (after ra hrs are 
# converted to deg).
#
# args:
#   d - degrees
#   m - minutes
#   s - seconds
#
# returns:
#   value in decimal degrees
#
def dms2dec(d, m, s):
  if d < 0.0:
    return d - m/60 - s/60**2
  else:
    return d + m/60 + s/60**2

#
# Function import_bss
#
# Loads radio survey data from BSS catalogue (Bright Source Sample of AT20G Survey)
# http://cdsarc.u-strasbg.fr/viz-bin/Cat?J/MNRAS/384/775
#
# returns:
#   output - list of BSS entries with each entry consisting of a tuple
#            of (id, right ascension, declination)
#
def import_bss():
  output = []
  #bss_cat = np.loadtxt('data/bss.dat', usecols=range(1, 7))
  bss_cat = np.loadtxt('data/table2.dat', usecols=range(1, 7))
  for i in range(0, len(bss_cat)):
    ra = hms2dec(bss_cat[i][0], bss_cat[i][1], bss_cat[i][2])
    d = dms2dec(bss_cat[i][3], bss_cat[i][4], bss_cat[i][5])
    output.append((i+1, ra, d))
  return output

#
# Function import_bss
#
# Load optical survey data SuperCOSMOS all-sky catalogue
# http://ssa.roe.ac.uk/allSky
#
# returns:
#   output - list of BSS entries with each entry consisting of a tuple
#            of (id, right ascension, declination)
#
def import_super():
  output = []
  super_cat = np.loadtxt('data/super.csv', delimiter=',', skiprows=1, usecols=[0,1])
  for i in range(0, len(super_cat)):
    output.append((i+1, super_cat[i][0], super_cat[i][1]))
  return output

#
# Function angular_dist
#
# Calculates the angular distance between 2 objects. Internally converts to
# radians for numpy calculations and then converts result back to degrees.
#
# args:
#   ra1_d, d1_d, ra2_d, d2_d - right ascension and declination values in
#                              degrees for object 1 and object 2
#
# returns:
#   angular distance in degrees
#
def angular_dist(ra1_d, d1_d, ra2_d, d2_d):
  
  # Convert from degress to radians
  ra1_r = np.radians(ra1_d)
  d1_r = np.radians(d1_d)
  ra2_r = np.radians(ra2_d)
  d2_r = np.radians(d2_d)
  
  # Calculate angular distance
  a = np.sin(np.abs(d1_r - d2_r)/2)**2
  b = np.cos(d1_r)*np.cos(d2_r)*np.sin(np.abs(ra1_r - ra2_r)/2)**2
  angular_dist_r = 2*np.arcsin(np.sqrt(a + b))
  
  # Convert back to degrees and return
  return np.degrees(angular_dist_r)

#
# Function find_closest
#
# Finds the object in catalogue with the smallest angular distance from
# an object with given right ascension and declination.
#
# args:
#   catalogue - catalogue of objects to compare against
#   ra - right ascension of the object being checked
#   d - declination of object being checked
#
# returns:
#   closest - id of closest object in catalogue
#   min_dist - angular distance of closest object from object being checked
#
def find_closest(catalogue, ra, d):
  closest = 0
  min_dist = float('inf')
  for item in catalogue:
    dist = angular_dist(item[1], item[2], ra, d)
    if dist < min_dist:
      closest = item[0]
      min_dist = dist
  return closest, min_dist

#
# Function crossmatch
#
# Matches objects in 2 catalogues within the given angular distance from each other.
#
# args;
#   cat1, cat2 - the catalogues being compared
#   max_dist - maximum distance to qualify as a match
#
# returns:
#   matches - list of matching pairs of objects, as a tuple (id of obj in cat1, id of obj
#             in cat2, distance)
#   no_matches - list of ids in cat1 for which no match was found
#
def crossmatch(cat1, cat2, max_dist):
  
  # Initialize output lists
  matches = []
  no_matches = []
  
  # Perform crossmatch
  for i in range(0, len(cat1)):
    closest = find_closest(cat2, cat1[i][1], cat1[i][2])
    if closest[1] <= max_dist:
      matches.append((i+1, closest[0], closest[1]))
    else:
      no_matches.append(i+1)
  
  # Return lists
  return matches, no_matches


#
# __main__ execution exercises above code
#
if __name__ == '__main__':
  bss_cat = import_bss()
  super_cat = import_super()

  # First example 
  max_dist = 40/3600
  matches, no_matches = crossmatch(bss_cat, super_cat, max_dist)
  print(matches[:3])
  print(no_matches[:3])
  print(len(no_matches))

  # Second example
  max_dist = 5/3600
  matches, no_matches = crossmatch(bss_cat, super_cat, max_dist)
  print(matches[:3])
  print(no_matches[:3])
  print(len(no_matches))


