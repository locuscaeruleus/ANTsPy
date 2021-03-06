
 

__all__ = ['get_mask']

from ..core import ants_image as iio
from .threshold_image import threshold_image
from .label_clusters import label_clusters
from .iMath import iMath
from .. import lib


def get_mask(img, low_thresh=None, high_thresh=None, cleanup=2):
    """
    Get a binary mask image from the given image after thresholding

    ANTsR function: `getMask`

    Arguments
    ---------
    img : ANTsImage
        image from which mask will be computed. Can be an antsImage of 2, 3 or 4 dimensions.
    
    low_thresh : scalar (optional)   
        An inclusive lower threshold for voxels to be included in the mask.
        If not given, defaults to image mean.
    
    high_thresh : scalar (optional) 
        An inclusive upper threshold for voxels to be included in the mask.
        If not given, defaults to image max
    
    cleanup : integer
        If > 0, morphological operations will be applied to clean up the mask by eroding away small or weakly-connected areas, and closing holes.
        If cleanup is >0, the following steps are applied
            1. Erosion with radius 2 voxels
            2. Retain largest component
            3. Dilation with radius 1 voxel
            4. Morphological closing
    
    Returns
    -------
    ANTsImage
    
    Example
    -------
    >>> img = ants.image_read( ants.get_ants_data('r16') )
    >>> mask = ants.get_mask(img)
    """
    cleanup = int(cleanup)
    if isinstance(img, iio.ANTsImage):
        if img.pixeltype != 'float':
            img = img.clone('float')

    if low_thresh is None:
        low_thresh = img.mean()
    if high_thresh is None:
        high_thresh = img.max()

    mask_img = threshold_image(img, low_thresh, high_thresh)
    if cleanup > 0:
        mask_img = iMath(mask_img, 'ME', cleanup)
        mask_img = iMath(mask_img, 'GetLargestComponent')
        mask_img = iMath(mask_img, 'MD', cleanup)
        mask_img = iMath(mask_img, 'FillHoles')
        while ((mask_img.min() == mask_img.max()) and (cleanup > 0)):
            cleanup = cleanup - 1
            mask_img = threshold_image(img, low_thresh, high_thresh)
            if cleanup > 0:
                mask_img = iMath(mask_img, 'ME', cleanup)
                mask_img = iMath(mask_img, 'MD', cleanup)
                mask_img = iMath(mask_img, 'FillHoles')

            #if cleanup == 0:
            #    clustlab = label_clusters(mask_img, 1)
            #    mask_img = threshold_image(clustlab, 1, 1)

    return mask_img







