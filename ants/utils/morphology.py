
 

__all__ = ['morphology']

from .iMath import iMath

def morphology(img, operation, radius, mtype='binary', value=1,
               shape='ball', radius_is_parametric=False, thickness=1,
               lines=3, include_center=False):
    """
    Apply morphological operations to an image

    ANTsR function: `morphology`

    Arguments
    ---------
    input : ANTsImage  
        input image
    
    operation : string  
        operation to apply
            "close" Morpholgical closing
            "dilate" Morpholgical dilation
            "erode" Morpholgical erosion
            "open" Morpholgical opening
    
    radius : scalar 
        radius of structuring element
    
    mtype : string   
        type of morphology
            "binary" Binary operation on a single value
            "grayscale" Grayscale operations
    
    value : scalar
        value to operation on (type='binary' only)
    
    shape : string
        shape of the structuring element ( type='binary' only )
            "ball" spherical structuring element
            "box" box shaped structuring element
            "cross" cross shaped structuring element
            "annulus" annulus shaped structuring element
            "polygon" polygon structuring element
    
    radius_is_parametric : boolean  
        used parametric radius boolean (shape='ball' and shape='annulus' only)
    
    thickness : scalar
        thickness (shape='annulus' only)
    
    lines : integer  
        number of lines in polygon (shape='polygon' only)
    
    include_center : boolean   
        include center of annulus boolean (shape='annulus' only)
    
    Returns
    -------
    ANTsImage

    Example
    -------
    >>> fi = ants.image_read( ants.get_ants_data('r16') , 2 )
    >>> mask = ants.get_mask( fi )
    >>> dilated_ball = ants.morphology( mask, operation='dilate', radius=3, mtype='binary', shape='ball')
    >>> eroded_box = ants.morphology( mask, operation='erode', radius=3, mtype='binary', shape='box')
    >>> opened_annulus = ants.morphology( mask, operation='open', radius=5, mtype='binary', shape='annulus', thickness=2)
    """
    if img.components > 1:
        raise ValueError('multichannel images not yet supported')

    _sflag_dict = {'ball': 1, 'box': 2, 'cross': 3, 'annulus': 4, 'polygon': 5}
    sFlag = _sflag_dict.get(shape, 0)

    if sFlag == 0:
        raise ValueError('invalid element shape')

    if (mtype == 'binary'):
        if (operation == 'dilate'):
            if (sFlag == 5):
                ret = iMath(img, 'MD', radius, value, sFlag, lines)
            else:
                ret = iMath(img, 'MD', radius, value, sFlag, radius_is_parametric, thickness, include_center)
        elif (operation == 'erode'):
            if (sFlag == 5):
                ret = iMath(img, 'ME', radius, value, sFlag, lines)
            else:
                ret = iMath(img, 'ME', radius, value, sFlag, radius_is_parametric, thickness, include_center)
        elif (operation == 'open'):
            if (sFlag == 5):
                ret = iMath(img, 'MO', radius, value, sFlag, lines)
            else:
                ret = iMath(img, 'MO', radius, value, sFlag, radius_is_parametric, thickness, include_center)
        elif (operation == 'close'):
            if (sFlag == 5):
                ret = iMath(img, 'MC', radius, value, sFlag, lines)
            else:
                ret = iMath(img, 'MC', radius, value, sFlag, radius_is_parametric, thickness, include_center)
        else:
            raise ValueError('Invalid morphology operation')
    elif (mtype == 'grayscale'):
        if (operation == 'dilate'):
            ret = iMath(img, 'GD', radius)
        elif (operation == 'erode'):
            ret = iMath(img, 'GE', radius)
        elif (operation == 'open'):
            ret = iMath(img, 'GO', radius)
        elif (operation == 'close'):
            ret = iMath(img, 'GC', radius)
        else:
            raise ValueError('Invalid morphology operation')
    else:
        raise ValueError('Invalid morphology type')

    return ret

