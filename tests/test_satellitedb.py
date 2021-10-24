from satellitedb import __version__


def test_version():
    """Main method, testing
    Args:
    Returns:
    """
    if __version__ != '0.1.0':
        raise AssertionError
