"""Heater control for the GHU-2 greenhouse (percent power, 0 to 100).

Owner: <Giuliana Cavaleri>
"""
from .helpers import _clamp


def control_heater(readings, setpoints, dt, state) -> float:
    kp = 0.25
    ki = 0.01
    temp = readings.temperature_c  # units=C
    target = setpoints.temperature_c  # units=C
    error = target - temp
    integral = state.get("heater_total", 0.0)
    # integral=integral+error*dt (C*s)
    proposed_integral = integral + (error * dt)
    unsaturated_output = (kp * error) + (ki * proposed_integral)
    # Windup defense
    if 0.0 < unsaturated_output < 100.0:
        integral = proposed_integral
    state["heater_total"] = integral
    output = (kp * error) + (ki * integral)
    return _clamp(output, 0.0, 100.0)
