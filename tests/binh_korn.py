from optimizer.mopso import MOPSO
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation


lb = [0.0, 0.0]
ub = [5.0, 3.0]

num_agents = 100
num_iterations = 100
num_params = 2

def f1(x, y):
    return 4 * x**2 + 4 * y**2

def f2(x, y):
    return (x - 5)**2 + (y - 5)**2

def f(params):
    return [[f1(params[i][0], params[i][1]), f2(params[i][0], params[i][1])] for i in range(len(params))]
        
pso = MOPSO(objective_functions=[f],lower_bounds=lb, upper_bounds=ub, 
            num_objectives=2, num_particles=num_agents, num_iterations=num_iterations, 
            inertia_weight=0.5, cognitive_coefficient=1, social_coefficient=1, 
            max_iter_no_improv=None, optimization_mode='global')

# run the optimization algorithm
# pso.optimize(history_dir='tmp/history', checkpoint_dir='tmp/checkpoint')

metrics = [pd.read_csv('tmp/history/iteration' + str(i) + '.csv', 
                       header=None, 
                       usecols=[num_params, num_params + 1]).transpose().to_numpy()
           for i in range(num_iterations)]


fig, ax = plt.subplots()

def animate(i):
    fig.clear()
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 70)
    ax.scatter(metrics[i][0], metrics[i][1], c='red', s=10)
    ax.set_title(str(i))

ani=animation.FuncAnimation(fig, animate, interval=200, frames=range(num_iterations))
ani.save('tmp/checkpoint/metrics.gif', writer='pillow')
