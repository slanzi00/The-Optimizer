import optimizer
import optimizer.metrics
import numpy as np
import matplotlib.pyplot as plt

num_agents = 100
num_iterations = 100
num_params = 30

lb = [0.] * num_params
ub = [1.] * num_params

optimizer.Logger.setLevel('DEBUG')

def zdt1_objective(x):
    f1 = x[0]
    g = 1 + 9.0 / (len(x)-1) * sum(x[1:])
    h = 1.0 - np.sqrt(f1 / g)
    f2 = g * h
    return f1, f2

def true_pareto(x):
    f1 = x
    f2 = 1-np.sqrt(x)
    return f1, f2
    
optimizer.Randomizer.rng = np.random.default_rng(46)

optimizer.FileManager.loading_enabled = False
optimizer.FileManager.saving_enabled = False

objective = optimizer.ElementWiseObjective(zdt1_objective, 2, true_pareto=true_pareto)

pso = optimizer.MOPSO(objective=objective, lower_bounds=lb, upper_bounds=ub,
                      num_particles=num_agents,
                      inertia_weight=0.4, cognitive_coefficient=1.5, social_coefficient=2,
                      initial_particles_position='random', exploring_particles=True, max_pareto_lenght=2*num_agents)

# run the optimization algorithm
pso.optimize(num_iterations, max_iterations_without_improvement=5)

print("Generational distance: " ,pso.get_metric(optimizer.metrics.generational_distance))
print("Inverted generational distance: " ,pso.get_metric(optimizer.metrics.inverted_generational_distance))
print("Hypervolume: " ,pso.get_metric(optimizer.metrics.hypervolume_indicator))

fig, ax = plt.subplots()
pareto_x = [particle.fitness[0] for particle in pso.pareto_front]
pareto_y = [particle.fitness[1] for particle in pso.pareto_front]
x = (np.linspace(0, 1, 100))
real_x, real_y = true_pareto(x)
plt.scatter(pareto_x, pareto_y, s=5)
plt.scatter(real_x, real_y, s=5, c='red')
plt.show()