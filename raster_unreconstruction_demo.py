import pygplates
import numpy as np  

from gprm import ReconstructionModel, GPlatesRaster
from gprm.utils.raster import reconstruct_raster, xyz2grd
from gprm.utils.fileio import write_netcdf_grid 


# Specify input files and parameters
rotation_filename = './Matthews_etal_GPC_2016_410-0Ma_GK07.rot'
static_polygon_filename = './Matthews_etal_GPC_2016_ContinentalPolygons.gpmlz'
raster_file = './earth_relief_10m.nc'

# output files will be based on this filename, with the reconstruction time added
# through the format statement
output_file_template = 'reconstructed_earth_relief_{:0.1f}Ma.nc'

grid_sampling=0.5
min_reconstruction_time = 10.
max_reconstruction_time = 200.
reconstruction_time_step = 10.

# End of input specification


reconstruction_model = ReconstructionModel('M2016')
reconstruction_model.add_rotation_model(rotation_filename)
reconstruction_model.add_static_polygons(static_polygon_filename)

reconstruction_times = np.arange(min_reconstruction_time,
                                 max_reconstruction_time+reconstruction_time_step,
                                 reconstruction_time_step)

# Create coordinates of output grid, assumed to be global in extent
grid_longitudes = np.arange(-180.,180.0001,grid_sampling)
grid_latitudes = np.arange(-90.,90.0001,grid_sampling)


for reconstruction_time in reconstruction_times:
    
    print('\nWorking on time {:f} Ma'.format(reconstruction_time))
    
    # More generally, this could be a reference to a time-dependent raster series with reconstruction
    # times corresponding to the values being looped through 
    ptopo = GPlatesRaster(raster_file)
    
    from_time = reconstruction_time
    to_time = 0

    (reconstructed_point_lons,
     reconstructed_point_lats,
     reconstructed_point_zvals) = reconstruct_raster(ptopo, 
                                                     reconstruction_model.static_polygons, 
                                                     reconstruction_model.rotation_model,
                                                     from_time, to_time, 
                                                     grid_sampling=grid_sampling)

    
    res = xyz2grd(reconstructed_point_lons,reconstructed_point_lats,reconstructed_point_zvals,
                  grid_longitudes,grid_latitudes)

    write_netcdf_grid(output_file_template.format(reconstruction_time), 
                      grid_longitudes, grid_latitudes, res, 
                      xname='x', yname='y', zname='z', format='NETCDF4')             