from math import sin, cos, acos, asin, pi
from typing import List, Tuple


def dist(ra0: float, dec0: float, ra1: float, dec1: float) -> float:
    """
    Calculate angular distance by 5 angles rule

    :param ra0: RA of first point in rad
    :param dec0: DEC of first point in rad
    :param ra1: RA of second point in rad
    :param dec1: DEC of second point in rad
    :return: angular distance in rad
    """
    return abs(acos(sin(dec0) * sin(dec1) + cos(dec0) * cos(dec1) * cos(ra1 - ra0)))


def inside_fov(ra0: float, dec0: float, ra1: float, dec1: float, fov_h: float, fov_v: float) -> bool:
    """
    Determine is object (ra1, dec1) lies inside rectangular FOV with center (ra0, dec0)
    and given half fov_h, fov_v

    :param ra0: RA of the center of FOV in rad
    :param dec0: DEC of the center of FOV in rad
    :param ra1: RA of the object in rad
    :param dec1: DEC of the object in rad
    :param fov_h: half horizontal field of view in rad
    :param fov_v: half vertical field of view in rad
    :return: true if inside
    """

    # tan, sin and cos of DEC of closest point (ra0, dec_min) with fixed ra0 to given object (ra1, dec1),
    # obtained by derivative
    t = sin(dec1) / (cos(dec1) * cos(ra1 - ra0))
    s = (t ** 2 / (1 + t ** 2)) ** 0.5
    c = (1 / (1 + t ** 2)) ** 0.5

    # Horizontal distances, 4 because of duality of arccos
    dh1 = acos(s * sin(dec1) + c * cos(dec1) * cos(ra1 - ra0))
    dh2 = acos(-s * sin(dec1) + c * cos(dec1) * cos(ra1 - ra0))
    dh3 = acos(s * sin(dec1) - c * cos(dec1) * cos(ra1 - ra0))
    dh4 = acos(-s * sin(dec1) - c * cos(dec1) * cos(ra1 - ra0))

    # Vertical distance obtained by rotating Z axis by angle dec0 and making transformation
    dec1_ = abs(asin(cos(ra1 - ra0) * cos(dec1) * sin(-dec0) + sin(dec1) * cos(-dec0)))

    # Returns opposite objects as well filtered separately
    return any((dh1 < fov_h, dh2 < fov_h, dh3 < fov_h, dh4 < fov_h)) and dec1_ < fov_v


def deg_to_rad(deg) -> float:
    return float(deg) * pi / 180


def quicksort(arr: List[Tuple[int, float]]) -> List[Tuple[int, float]]:
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0][1]
        left = []
        right = []
        for i in range(1, len(arr)):
            if arr[i][1] < pivot:
                left.append(arr[i])
            else:
                right.append(arr[i])
        return quicksort(left) + [(arr[0][0], pivot)] + quicksort(right)


def sorted_indices(arr: List[Tuple[int, float]]) -> List[int]:
    return [x[0] for x in quicksort(arr)]
