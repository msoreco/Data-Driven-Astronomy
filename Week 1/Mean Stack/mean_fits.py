from astropy.io import fits
import numpy as np

#
# Function mean_fits
#
# Calculates the per-pixel mean of data in a list of files in the FITS format.
# The FITS files only contain data in the first element of the hdulist array.
# An hdulist (HDU -> "Header-Data Unit") is the data structure contained within a FITS file.
#
def mean_fits(fits_files):
  
  num_files = len(fits_files)
  
  # Copy data from first FITS file in list into 2-d numpy data array of same size.
  hdulist = fits.open(fits_files[0])
  data = hdulist[0].data
  
  # Iterate through data in remaining FITS files, adding values to the current
  # values in the 2-d data array.
  for i in range(1,num_files):
    hdulist = fits.open(fits_files[i])
    data += hdulist[0].data
  
  # Return per-pixel mean
  return (data/num_files)

#
# __main__ execution exercises above code
#
if __name__ == '__main__':
  
  # Execution 1
  data1  = mean_fits(['data/image0.fits', 'data/image1.fits', 'data/image2.fits'])
  print(data1[100, 100])
  print()
  
  # Execution 2
  data2  = mean_fits(['data/image0.fits', 'data/image1.fits', 'data/image3.fits'])
  print(data2[100, 100])
  print()
  
  # Execution 3
  data3  = mean_fits(['data/image0.fits', 'data/image1.fits', 'data/image2.fits', 'data/image3.fits', 'data/image4.fits'])
  print(data3[100, 100])

  # Plot the results
  import matplotlib.pyplot as plt
  plt.imshow(data3, cmap=plt.cm.viridis)
  plt.colorbar()
  plt.show()
