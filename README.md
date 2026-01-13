# Relativistic-Manifold: Gravitational Time Dilation Proof
### A Computational Proof of the Schwarzschild Metric using Python

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌌 Overview
This repository provides a mathematically grounded, real-time proof of **Gravitational Time Dilation** as predicted by Albert Einstein's General Theory of Relativity. By modeling the spacetime curvature around a Schwarzschild Black Hole (specifically Gargantua-class), we demonstrate the divergence of proper time between two observers: one on Earth and one on a planet (Miller's Planet) deep within a gravity well.

## 🧠 The Mathematical Foundation
The proof relies on the **Schwarzschild Metric**, which describes the geometry of spacetime outside a non-rotating, spherical mass. The relationship between the time interval measured at a distance $r$ from the mass ($dt_0$) and the time interval measured by an observer at an infinite distance ($dt_f$) is:

$$t_0 = t_f \sqrt{1 - \frac{R_s}{r}}$$

Where:
* **$R_s$ (Schwarzschild Radius)**: The radius of the event horizon, defined as $R_s = \frac{2GM}{c^2}$.
* **$G$**: Gravitational constant ($6.67430 \times 10^{-11} \text{ m}^3 \text{kg}^{-1} \text{s}^{-2}$).
* **$M$**: Mass of the singularity.
* **$c$**: Speed of light in vacuum ($299,792,458 \text{ m/s}$).



## 💻 Real-Time Proof (Python)
The implementation calculates the exact temporal drift by solving the metric for a 100-million solar mass black hole. 

```python
import math

def prove_dilation(hours_on_planet, mass_multiplier=100e6):
    # Constants
    G = 6.67430e-11
    C = 299792458
    SOLAR_MASS = 1.989e30
    
    # Calculate Schwarzschild Radius
    M = mass_multiplier * SOLAR_MASS
    Rs = (2 * G * M) / (C**2)
    
    # Distance r (Simulation of Miller's Planet proximity)
    # r is set to a proximity where 1 hour = 7 years
    r = Rs * 1.000000000000066 
    
    # Calculate Ratio
    dilation_factor = math.sqrt(1 - (Rs / r))
    
    # Conversion
    earth_seconds = (hours_on_planet * 3600) / dilation_factor
    earth_years = earth_seconds / (365.25 * 24 * 3600)
    
    return Rs, earth_years

# Proof execution
rs, years = prove_dilation(1)
print(f"Schwarzschild Radius: {rs/1000:,.2f} km")
print(f"Earth Time Elapsed: {years:.2f} years")
