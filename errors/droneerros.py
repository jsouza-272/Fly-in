class DroneError():
    """Base error related to the drone domain."""

    pass


class DroneRunningError(DroneError):
    """Error for inconsistencies during drone execution."""

    pass
