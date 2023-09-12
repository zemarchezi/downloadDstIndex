"""Print the version number for the current installation."""


def version():
    """
    Print the pysatdata version number.

    Returns
    -------
    None.

    """
    import importlib.metadata
    ver = importlib.metadata.version('dstdownloader')
    print("dstdownloader version: " + ver)