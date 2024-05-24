import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Updated mean and standard deviation for init time
mean_init_time = 2.61
std_init_time = 0.37

# Define the range for plotting the Gaussian distribution
x_range = np.linspace(1, 4, 1000)
y = norm.pdf(x_range, mean_init_time, std_init_time)

# Plotting
plt.figure(figsize=(8, 6))
plt.plot(x_range, y, color='blue', label=f'Mean init time (Mean: {mean_init_time}, SD: {std_init_time})')
plt.fill_between(x_range, y, color='blue', alpha=0.2)

# Calculate 95% confidence interval
conf_int = norm.interval(0.95, loc=mean_init_time, scale=std_init_time)
plt.axvline(conf_int[0], color='red', linestyle='--', label=f'95% CI: [{conf_int[0]:.2f}, {conf_int[1]:.2f}]')
plt.axvline(conf_int[1], color='red', linestyle='--')

# Labels and title
plt.title('Mean init time')
plt.xlabel('Value')
plt.ylabel('Probability Density')
plt.legend()
plt.grid(True)
plt.show()
