from reportlab.lib.units import mm


def dx(n):
    """Dimensioning in mm. Along the X-axis"""
    return n*mm


def dy(n):
    """Dimensioning in mm. Along the Y-axis"""
    return n*mm


def px(n):
    """Positioning the X-Coordinate in mm for An A4 Paper"""
    return (n/100 * 210)*mm


def py(n):
    """Positioning the X-Coordinate in mm for An A4 Paper"""
    return (n / 100 * 297)*mm
