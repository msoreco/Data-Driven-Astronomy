import numpy as np
from matplotlib import pyplot as plt

#
# Scatter Plot visualization of redshift values for combination of 2 color indexes
#
if __name__ == "__main__":
    
    data = np.load('data/sdss_galaxy_colors.npy')
    
    cmap = plt.get_cmap('YlOrRd')
    
    # Define our colour indexes u-g and r-i
    ug = data['u'] - data['g']
    ri = data['r'] - data['i']
    
    # Make a redshift array
    redshift = data['redshift']
    
    # Create the plot with plt.scatter and plt.colorbar
    plt.scatter(ug, ri, c=redshift, linewidths=0, s=3, cmap=cmap)
    plt.xlabel('Colour index u-g')
    plt.ylabel('Colour index r-i')
    plt.title('Redshift (colour) u-g versus r-i')
    
    plt.xlim(-0.5, 2.5)
    plt.ylim(-0.5, 1.0)
    plt.colorbar()
    plt.show()
