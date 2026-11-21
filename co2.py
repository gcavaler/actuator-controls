"""CO2 valve control for the GHU-2 greenhouse (percent open, 0 to 100).

Owner: <Charlotte Martin>
"""
from .helpers import _clamp


def control_co2(readings, setpoints, dt, state) -> float:
    CO2_ON = 800  # units = ppm
    CO2_OFF = 850  # units = ppm
    CO2_DUTY = 75  # units = percent
    N_FREEZE = 5  # number of ticks to consider a sensor frozen
    CO2_DISAGREE = 200  # units = ppm, threshold for sensor disagreement

    k30 = readings.co2_ppm_primary
    scd41 = readings.co2_ppm_backup

    # 1a. Check if the K30 reading is the same as the previous one
    if k30 == state.get("co2_k30_prev"):
        state["co2_frozen_count"] = state.get("co2_frozen_count", 0) + 1
    else:
        state["co2_frozen_count"] = 0

    # Check if K30 is frozen or the sensors disagree
    # Choose which reading to use
    if (state["co2_frozen_count"] >= N_FREEZE
            or abs(k30 - scd41) > CO2_DISAGREE):
        co2 = scd41
    else:
        co2 = k30

    state["co2_k30_prev"] = k30

    # 1b. Turn the CO2 valve off if CO2 is too high and on if it is too low
    if co2 >= CO2_OFF:
        state["co2_latch"] = False
    elif co2 <= CO2_ON:
        state["co2_latch"] = True

    # Set the valve opening based on whether the CO2 latch is on or off
    if state.get("co2_latch", False):
        output = CO2_DUTY
    else:
        output = 0

    return _clamp(output, 0.0, 100.0)
