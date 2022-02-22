import ccdproc
import numpy as np
from astropy.stats import mad_std
import astropy.units as u
from astropy.nddata import CCDData

# stack a series of image using average with sigma clipping
def stack(fname,dirname):
     flist = ccdproc.ImageFileCollection(location=dirname+"/",find_fits_by_reading=True)
     combined_im = ccdproc.combine(flist.files_filtered(include_path=True),method='average',sigma_clip=True,sigma_clip_low_thresh=5,sigma_clip_high_thresh=5,sigma_clip_func=np.ma.median,sigma_clip_dev_func=mad_std,mem_limit=350e6,unit=u.adu)
     combined_im.write(fname+"_stacked.fits")



# calculate 1/median of an array
def inv_median(a):
    return 1/np.median(a)



# create a bias-subtracted stacked image
def sub_stack(fname,dirname,bias_comb):
     flist = ccdproc.ImageFileCollection(location=dirname+"/",find_fits_by_reading=True)
     i = 0
     for f in flist.files_filtered(include_path=True):
          f_sub = ccdproc.subtract_bias(CCDData.read(f,unit=u.adu),CCDData.read(bias_comb))
          f_sub.write(dirname + "/calib_" + str(i) + ".fits")
          i = i+1
     caliblist = ccdproc.ImageFileCollection(location=dirname+"/",find_fits_by_reading=True,glob_include="calib*")
     combined_im = ccdproc.combine(caliblist.files_filtered(include_path=True),method='average',scale=inv_median,sigma_clip=True,sigma_clip_low_thresh=5,sigma_clip_high_thresh=5,sigma_clip_func=np.ma.median,sigma_clip_dev_func=mad_std,mem_limit=350e6,unit=u.adu)
     combined_im.write(fname+"_stacked.fits")



# subtract darks and divide flats from a science frame
def reduce(fname,dirname,darkname,flatname,outname):
     reduced = ccdproc.subtract_dark(CCDData.read(dirname + "/" + fname,unit=u.adu),CCDData.read(darkname),exposure_time="exptime",exposure_unit=u.second)
     reduced = ccdproc.flat_correct(reduced,CCDData.read(flatname))
     reduced.write(outname)


# You'll need to modify everything below this line to correspond to the directory and file names for your data

#stack("bias","bias")
#stack("dark120","dark-120s")
#stack("dark240","dark-240s")

#sub_stack("flatL","flat-L","bias_stacked.fits")
#sub_stack("flatR","flat-R","bias_stacked.fits")
#sub_stack("flatB","flat-B","bias_stacked.fits")

#reduce("L1.FIT","science-L","dark120_stacked.fits","flatL_stacked.fits","L1calib.fits")
#reduce("L2.FIT","science-L","dark120_stacked.fits","flatL_stacked.fits","L2calib.fits")
#reduce("L3.FIT","science-L","dark120_stacked.fits","flatL_stacked.fits","L3calib.fits")
#reduce("R1.FIT","science-R","dark240_stacked.fits","flatR_stacked.fits","R1calib.fits")
#reduce("B1.FIT","science-B","dark240_stacked.fits","flatB_stacked.fits","B1calib.fits")
