import matplotlib.pyplot as plt
import numpy as np
from storagesim.simulation import Simulator

if __name__ == "__main__":
    # use the default values in the Simulator object
    sim = Simulator()
    # run for 4 hours
    t_eval = np.arange(0, 4 * 3600, 5 * 60)
    t, T = sim.solve_ivp(duration=4 * 3600, t_eval=t_eval)
    # plot
    fig, ax = plt.subplots()
    ax.plot(t / 60, T.reshape(-1))
    ax.set_xlabel("Minutes")
    ax.set_ylabel("Storage Tank Temperature [C]")
    fig.savefig("simulation.pdf", format="pdf")
