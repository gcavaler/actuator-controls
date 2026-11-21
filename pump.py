"""Pump control for the GHU-2 greenhouse (percent speed, 0 to 100).

Owner: <Dillon Mackenzie>
"""
from .helpers import _clamp

PUMP_KP = 2000.0      # pump % per unit VWC below setpoint
PUMP_VWC_OFF = 0.50   # pump off at or above this VWC


def control_pump(readings, setpoints, dt, state) -> float:
    if readings.soil_vwc >= PUMP_VWC_OFF:
        output = 0.0
    else:
        output = PUMP_KP * (setpoints.soil_vwc - readings.soil_vwc)
    return _clamp(output, 0.0, 100.0)
