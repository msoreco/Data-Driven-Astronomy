# helper was provided in class on remote Grok environment, so this file will not run locally
from helper import running_stats
import numpy as np
from astropy.io import fits

#
# Function median_bins_fits
#
# args:
#   fits_files - list of FITS format files
#   B - number of bins
#
# returns:
#   means - per-pixel mean values
#   stds - per-pixel standard deviations
#   left_bin_counts - number of data points with values less than the mean - std dev for each pixel
#   bin_counts - number of data points contained in each bin for each pixel
#
def median_bins_fits(fits_files, B):
    
    num_files = len(fits_files)

    # Load FITS data into 3-d numpy array
    data = np.zeros((200, 200, num_files))
    for i in range(0, num_files):
        hdulist = fits.open(fits_files[i])
        data[:,:,i] = hdulist[0].data

    # Initialize bin counts, one for each bin for each pixel
    bin_counts = np.zeros((200, 200, B))

    # Calculate per-pixel mean, std deviations (200 x 200 arrays)
    (means, stds) = running_stats(fits_files)

    # Calculate per-pixel bin boundaries/widths
    minvals = means - stds
    bin_widths = 2 * stds / B

    # Per-pixel number of values in left (ignore) bin, this is the number of data points
    # with values less than the mean - std dev for each pixel.
    left_bin_counts = sum([data[:,:,i] < minvals for i in range(0, num_files)])
    left_bin_counts = np.array(left_bin_counts, float)

    # Calculate bin counts
    for i in range(0, B):
        bin_mins = minvals + i * bin_widths
        bin_maxs = minvals + (i+1) * bin_widths
        for j in range(0, num_files):
            in_this_bin = np.logical_and(data[:,:,j] >= bin_mins, data[:,:,j] < bin_maxs)
            bin_counts[:,:,i] += in_this_bin

    # return results
    return means, stds, left_bin_counts, bin_counts

#
# Function median_approx_fits
#
# args:
#   fits_files - list of FITS format files
#   B - number of bins
#
# returns:
#   medians - median value for each pixel
#
def median_approx_fits(fits_files, B):
    
    (means, stds, left_bin_counts, bin_counts) = median_bins_fits(fits_files, B)

    # Calculate bin dimensions (some duplication here)
    minvals = means - stds
    bin_widths = 2 * stds / B
    
    # Threshold is half of number of files
    threshold = (len(fits_files) + 1) / 2
    
    # Initialize counts at number of values in left bin
    counts = left_bin_counts
                
    medians = np.empty((200, 200))

    # Determine which bin contains "(n + 1)/2"-th value by incrementally adding number of
    # values in each bin (for each pixel) and stopping when count reaches threshold.
    for i in range(0, B):
        old_counts = np.array(counts)
        counts += bin_counts[:,:,i]
        median_in_this_bin = np.logical_and(old_counts < threshold, counts >= threshold)
        medians[median_in_this_bin] = minvals[median_in_this_bin] \
            + (i + 0.5)*bin_widths[median_in_this_bin]

    return medians

#
# __main__ execution exercises above code
#
if __name__ == '__main__':
    median = median_approx_fits(['data/image0.fits', 'data/image1.fits', 'data/image2.fits'], 5)
    print(median[100,100])
