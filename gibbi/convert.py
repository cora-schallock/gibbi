from math import pi

def can_float(to_check):
    try:
        float(to_check)
        return True
    except Exception:
        return False

def convert_matlab_to_cartessian(inputCenterC,inputCenterR):
    cx = inputCenterC - 1.5
    cy = inputCenterR - 1.5
    return (cx,cy)

def convert_disk_angle_to_bisection_angle(diskMajAxsAngle):
    return diskMajAxsAngle * -1.0

def normalize_angle(angle_in_rads: float) -> float:
    """Given an angle measured in radians, convert angle so that angle ∈ [0.0,2.0 * pi]
            (NOTE: measured counterclockwise from right-hand side of x-axis)
        Args:
            angle_in_rads: an angle in radians
        Returns:
            normalized angle (normalized angle ∈ [0.0,2.0 * pi]),
                (NOTE: measured counterclockwise from right-hand side of x-axis)"""

    if angle_in_rads >= 0.0:
        return angle_in_rads % (2.0 * pi)
    else:
        return (angle_in_rads % (-2.0 * pi)) + (2.0 * pi)