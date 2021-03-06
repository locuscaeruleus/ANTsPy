"""
Get local ANTsPy data
"""

__all__ = ['get_ants_data']

import os 
data_path = os.path.expanduser('~/.antspy/')

def get_ants_data(name):
    """
    Get ANTsPy test data filename

    ANTsR function: `getANTsRData`
    
    Arguments
    ---------
    name : string
        name of test image tag to retrieve
        Options:
            - 'r16'
            - 'r27'
            - 'r64'
            - 'r85'
            - 'mni'
            - 'surf'
    Returns
    -------
    string
        filepath of test image
    """
    datapath = None
    for fname in os.listdir(data_path):
        if name in fname:
            datapath = os.path.join(data_path, fname)

    if datapath is None:
        raise ValueError('File doesnt exist. Options: ' , os.listdir(data_path))
    return datapath
