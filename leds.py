"""LED control for the GHU-2 greenhouse (percent intensity, 0 to 100).

Owner: <Corrine Pixton>
"""
from .helpers import _clamp


def control_leds(readings, setpoints, dt, state) -> float:
    if setpoints.is_daytime is True:
        if readings.par_umol_m2_s < 200:
            output = 100.0
        elif readings.par_umol_m2_s < 400:
            output = 50.0
        else:
            output = 0.0
    else:
        output = 0.0
    return _clamp(output, 0.0, 100.0)
