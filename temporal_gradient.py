from __future__ import print_function, division

__author__ = "christoph.sommer@ist.ac.at"

import os
import sys

from ij import IJ 
from net.imglib2.img.display.imagej import ImageJFunctions as IJF

from ij import CompositeImage
from io.scif.img import ImgSaver
from net.imagej.axis import Axes
from net.imglib2.view import Views
from net.imagej.ops import OpService as ops
from net.imglib2.util import Intervals
from net.imglib2.type.numeric import RealType
from net.imglib2.algorithm.gauss3 import Gauss3
from net.imglib2.img.array import ArrayImgFactory
from net.imglib2.type.numeric.real import FloatType
from net.imglib2.algorithm.gradient import PartialDerivative 
from net.imglib2.type.numeric.integer import UnsignedByteType
from net.imglib2.img.display.imagej import ImageJFunctions as IJF
from net.imagej.ops.convert.normalizeScale import NormalizeScaleRealTypes

def get_script_patch():
    import inspect
    return os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda:0)))

sys.path.append(get_script_patch())


def rescale_uint8(ops, img):
	scale_op = NormalizeScaleRealTypes()
	scale_op.setEnvironment(ops)
	scale_op.initialize()

	out_uint8 = ArrayImgFactory(UnsignedByteType()).create(img)
	ops.convert().imageType(out_uint8, img, scale_op)
	return out_uint8

def smooth_temporal_gradient(ops, img, sigma_xy, sigma_t, frame_start, frame_end, normalize_output):
	"""
	Smooth input image (imglib2 array) xyt with Gaussian and build temporal gradient 
	from frame_start to frame_end
	"""
	
	n = img.numDimensions()
	assert n == 3, "Input data needs to be 3-dimensional, 2D + time"
	 
	dims = [img.dimension(d) for d in range(n)]
	dim_x, dim_y, dim_t = dims
	
	if frame_end == -1:
		frame_end = dim_t
		
	if frame_end > dim_t:
		frame_end = dim_t

	assert frame_start < frame_end, "'Frame start' must be smaller than 'Frame end'"
		
	# crop image temporally by using a View
	
#	img_crop = Views.interval(img, [0, 0, frame_start], [dim_x-1, dim_y-1, frame_end-1])
	img_crop = ops.transform().crop(img, Intervals.createMinMax(0, 0, frame_start, dim_x-1, dim_y-1, frame_end-1))
	
	# create output for smoothing
	img_smooth = ArrayImgFactory(FloatType()).create(img_crop)

	# update dimensions
	dims = [img_crop.dimension(d) for d in range(n)]
	
	# smooth with Gaussian (use mirror as border treatment)
	Gauss3.gauss([sigma_xy, sigma_xy, sigma_t], Views.extendBorder(img_crop), img_smooth)
	
	# compute gradient along (time) axis 2
	gradient = ArrayImgFactory(FloatType()).create(dims)
	PartialDerivative.gradientBackwardDifference(Views.extendBorder(img_smooth), gradient, 2);
	
	# separate response into growing and shrinking part by thresholding and multiplying that mask
	thresholded = ops.run("threshold.apply", gradient, FloatType(0.))
	mask = ops.convert().float32(thresholded)
	grow = ops.run("math.multiply", gradient, mask)
	
	# same, but negate befor
	gradient_neg = ops.run("math.multiply", gradient, -1)
	thresholded = ops.run("threshold.apply", gradient_neg, FloatType(0.))
	mask = ops.convert().float32(thresholded)
	shrink = ops.run("math.multiply", gradient, mask)

	#shrink = ops.transform().crop(img, Intervals.createMinMax(0, 0, frame_start, dim_x-1, dim_y-1, frame_end-1))
	
	# concatenate output 
	if normalize_output:
		shrink     = rescale_uint8(ops, shrink)
		grow       = rescale_uint8(ops, grow)
		img_smooth = rescale_uint8(ops, img_smooth)
		
	out = Views.stack([shrink, grow, img_smooth])
	
	# permute channel with time to make time last dim (for back-conversion) 
	out = Views.permute(out, 2, 3)

	# crop view 1st time point result (empty since using backwardDifferences)
	out = Views.interval(out, [0, 0, 0, 1], [out.dimension(d)-1 for d in range(4)])

	# get ImagePlus back and set correct dimensions
	out_imp = IJF.wrap(out, "Grow and shrink")

	# resize IMP now one frame less (see crop view)
	out_imp.setDimensions(3, 1, frame_end - frame_start -1)
	out_imp.setDisplayMode(IJ.COMPOSITE)
#	IJ.save(out_imp, "H:/projects/032_loose_speckle/grow_and_shrink_ij.tif")

	return out_imp


if __name__ == "__main__":
	pass
	