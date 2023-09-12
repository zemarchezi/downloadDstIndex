"""Print the version number for the current installation."""


def version():
    """
    Print the pysatdata version number.

    Returns
    -------
    None.

    """
    import pkg_resources
    ver = pkg_resources.get_distribution("dstdownloader").version
    print("dstdownloader version: " + ver)