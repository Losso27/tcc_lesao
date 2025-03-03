# Fuzzy Logic Example with SciKit-Fuzzy: Temperature Fuzzification and Defuzzification

# Import necessary libraries
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# Define the universe of discourse for the temperature
x_range = np.arange(0, 10, 1)  # Temperature range from 0 to 40 degrees Celsius

leve = fuzz.trapmf(x_range, [0, 0, 2, 3])
moderada = fuzz.trapmf(x_range, [2, 3, 5, 6])
intensa = fuzz.trapmf(x_range, [5, 6, 10, 10])

# Plot the membership functions
plt.figure(figsize=(10, 6))
plt.plot(x_range, leve, label='Leve', color='blue')
plt.plot(x_range, moderada, label='Moderada', color='green')
plt.plot(x_range, intensa, label='Intensa', color='red')
plt.title('Intensidade da Dor')
plt.xlabel('Escala de Dor')
plt.ylabel('Grau de Pertinência')
plt.legend()
plt.grid(True)
plt.show()
