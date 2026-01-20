# storagesim
Simulation of solar panel to storage tank heat transfer.

# Equations
Hottel-Whillier model is used to find the heat transferred to the fluid (water in this case) from the solar panel. The 
equation is:

$$ \dot{Q}_{sp} = A_{sp} \left[F_{R}\left(\tau\alpha\right)G - F_{R}U_{L,sp}\left(T_{t} - T_{a}\right)\right]$$

where
- $ A_{sp} $ is the surface area of the solar panel in $ m^2 $
- $ F_{R} $ is the heat removal factor
- $ \tau\alpha $ is the transmittance-absorptance product
- $ G $ is the solar irradiance in $ \frac{W}{m^2} $
- $ U_{L,sp} $ is the loss coefficient for the solar panel in $ \frac{W}{m^2 \cdot K} $
- $ T_{t} $ is the storage tank temperature in $ K $
- $ T_{a} $ is the ambient temperature in $ K $

It is assumed that the tank is mixed well (no temperature gradients inside) and no additional heat losses in the pipes 
connecting the solar panel to the storage tank.

The inlet temperature of the storage tank is given by:
$$ T_{in} = T_{t} + \frac{\dot{Q}_{sp}}{\dot{m}c_{p}} $$
where 
- $ \dot{m} $ is the flow rate of the water in $ \frac{kg}{s} $
- $ c_{p} $ is the specific heat of water $ \left(4180 \frac{J}{kg \cdot K}\right) $

The storage tank differential equation is:

$$ Mc_{p}\frac{T_{t}}{dt} = \dot{m}c_{p}\left(T_{in} - T_{t}\right) - U_{t}A_{t}\left(T_{t}-T_{a}\right) $$
where
- $ M $ is the mass of water in the storage tank in $ kg $
- $ U_{t}A_{t} $ is the heat loss coefficient for the storage tank in $ \frac{W}{K} $

# Usage
The class object to use is the `Simulator` class object. 

## `Simulator` Class Inputs
The inputs are the following:
- `ta`: transmittance-absorptance of solar panel, $\left(\tau\alpha\right)$ in the equations above, (default value is 0.85)
- `f_r`: heat removal factor of solar panel, $ F_{R} $ in the equations above, (default value is 0.85)
- `panel_area`: area of solar panel in $ m^2 $, $ A_{sp} $ in the equations above, (default value is 1.5)
- `panel_loss`: solar panel loss factor in $ \frac{W}{m^2 \cdot K} $, $ U_{L,sp} $ in the equations above, (default value is 3)
- `g`: solar irradiance in $ \frac{W}{m^2} $, $ G $ in the equations above, (default value is 500)
- `t_a`: ambient temperature in Celsius, $ T_{a} $ in the equations above, (default value is 20)
- `m_dot`: mass flow rate of water in $ \frac{kg}{s} $, $ \dot{m} $ in the equations above, (default value is 0.02)
- `tank_volume`: storage tank volume in liters (default value is 150)
- `tank_temp`: storage tank initial temperature in Celsius (default value is 15)
- `tank_loss`: storage tank loss coefficient in $ \frac{W}{K} $, $ U_{t}A_{t} $ in the equations above, (default value is 5)

## `solve_ivp` Method
The `solve_ivp` method performs the simulation and returns an array of times and tank temperatures. The inputs to this
method are:
- `duration`: length of time for the simulation in seconds
- `t_eval`: time points in seconds to return (optional)

An example script is given in `plot.py` and a plot is shown in `simulation.pdf`. `tests/test_simulation.py` also shows 
a number of use cases for the `Simulator` object.
