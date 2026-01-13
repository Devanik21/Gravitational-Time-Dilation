import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, FancyBboxPatch, Arc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime
import io
import base64

# ============================================================================
# PHYSICAL CONSTANTS
# ============================================================================
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
C = 299792458    # Speed of light (m/s)
SOLAR_MASS = 1.989e30  # Solar mass (kg)
AU = 1.496e11    # Astronomical Unit (m)
PLANCK_LENGTH = 1.616255e-35  # Planck length (m)
PARSEC = 3.086e16  # Parsec (m)
HBAR = 1.054571817e-34  # Reduced Planck constant
K_B = 1.380649e-23  # Boltzmann constant
STEFAN_BOLTZMANN = 5.670374419e-8  # Stefan-Boltzmann constant

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="⚛️ Relativistic Spacetime Analyzer",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS - ULTIMATE CYBERPUNK DARK MODE
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1c24 50%, #0e1117 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    ::-webkit-scrollbar-track {
        background: #0e1117;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #ff3366, #9933ff);
        border-radius: 5px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #00ffcc, #ffcc00);
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Orbitron', sans-serif !important;
        color: #00ffcc !important;
        text-shadow: 0 0 10px rgba(0, 255, 204, 0.5);
    }
    
    p, div, span, label {
        font-family: 'Share Tech Mono', monospace !important;
        color: #b0b8c5 !important;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        color: #00ffcc !important;
        font-family: 'Orbitron', sans-serif !important;
        text-shadow: 0 0 15px rgba(0, 255, 204, 0.6);
    }
    
    [data-testid="stMetricLabel"] {
        color: #ffcc00 !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #ff3366 !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1c24 0%, #0e1117 100%);
        border-right: 2px solid #00ffcc;
        box-shadow: 5px 0 20px rgba(0, 255, 204, 0.2);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #00ffcc;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #ff3366, #9933ff) !important;
    }
    
    .stSlider > div > div > div {
        background: #1a1c24 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #ff3366 0%, #9933ff 100%);
        color: white;
        border: 2px solid #00ffcc;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 20px rgba(255, 51, 102, 0.5);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #00ffcc 0%, #ffcc00 100%);
        color: #0e1117;
        box-shadow: 0 0 30px rgba(0, 255, 204, 0.8);
        transform: translateY(-2px);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, #1a1c24, #252830);
        border: 2px solid #00ffcc;
        border-radius: 10px;
        color: #00ffcc !important;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
    }
    
    .streamlit-expanderContent {
        background: #1a1c24;
        border: 1px solid #333;
        border-radius: 0 0 10px 10px;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #0e1117;
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #1a1c24, #252830);
        border: 2px solid #333;
        border-radius: 8px;
        color: #00ffcc;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #ff3366, #9933ff);
        border-color: #00ffcc;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.5);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00ffcc, #ffcc00) !important;
        color: #0e1117 !important;
        border-color: #00ffcc !important;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.7);
    }
    
    /* Dataframe styling */
    .dataframe {
        background: #1a1c24 !important;
        color: #00ffcc !important;
        border: 2px solid #00ffcc !important;
        border-radius: 10px !important;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #ff3366, #9933ff) !important;
        color: white !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
    }
    
    .dataframe td {
        background: #1a1c24 !important;
        color: #00ffcc !important;
        border-color: #333 !important;
    }
    
    /* Info/Warning/Success boxes */
    .stAlert {
        background: linear-gradient(135deg, #1a1c24, #252830);
        border-left: 5px solid #00ffcc;
        border-radius: 10px;
        color: #00ffcc;
    }
    
    /* Custom classes */
    .hero-section {
        background: linear-gradient(135deg, #1a1c24 0%, #0e1117 100%);
        border: 3px solid #00ffcc;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 0 30px rgba(0, 255, 204, 0.3);
        text-align: center;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(90deg, #ff3366, #9933ff, #00ffcc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: none;
        margin-bottom: 0.5rem;
        letter-spacing: 5px;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: #ffcc00 !important;
        font-style: italic;
        margin-top: 0.5rem;
    }
    
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1a1c24, #252830);
        border: 2px solid #00ffcc;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.2);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 30px rgba(0, 255, 204, 0.5);
        border-color: #ffcc00;
    }
    
    .metric-card-title {
        color: #ffcc00 !important;
        font-size: 0.9rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-card-value {
        color: #00ffcc !important;
        font-size: 1.8rem;
        font-weight: 900;
        font-family: 'Orbitron', sans-serif;
        text-shadow: 0 0 10px rgba(0, 255, 204, 0.6);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #2a1a1a, #1a1c24);
        border: 3px solid #ff3366;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 0 25px rgba(255, 51, 102, 0.3);
    }
    
    .warning-box-title {
        color: #ff3366 !important;
        font-size: 1.3rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
    }
    
    .highlight-box {
        background: linear-gradient(135deg, #ff3366, #9933ff);
        border: 3px solid #00ffcc;
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: 0 0 40px rgba(255, 51, 102, 0.5);
    }
    
    .highlight-value {
        font-size: 3rem;
        font-weight: 900;
        color: white !important;
        font-family: 'Orbitron', sans-serif;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.8);
        margin: 1rem 0;
        letter-spacing: 3px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# RELATIVISTIC CALCULATOR CLASS
# ============================================================================
class RelativisticCalculator:
    def __init__(self, mass_multiplier, distance_offset_log, spin_param=0, observer_velocity=0, theta=np.pi/2):
        self.M = mass_multiplier * 1e6 * SOLAR_MASS
        self.a = spin_param  # Dimensionless spin parameter (0 to 0.998)
        self.v_obs = observer_velocity * C
        self.theta = theta  # Polar angle for Kerr metric
        
        # Schwarzschild radius
        self.Rs = (2 * G * self.M) / (C**2)
        
        # Kerr metric parameters
        self.r_g = G * self.M / (C**2)
        self.a_kerr = self.a * self.r_g  # Spin parameter in meters
        
        # Critical radii
        self.r_isco = self.calculate_isco()
        self.r_photon = self.calculate_photon_sphere()
        self.r_ergosphere = self.calculate_ergosphere()
        
        # Distance from center
        self.r = self.Rs + (10**distance_offset_log)
        
        # Kerr metric functions
        self.Sigma = self.r**2 + (self.a_kerr * np.cos(self.theta))**2
        self.Delta = self.r**2 - self.Rs * self.r + self.a_kerr**2
        self.rho = np.sqrt(self.Sigma)
        
        # Calculate all effects
        self.gravitational_dilation = self.calc_gravitational_dilation()
        self.kerr_time_dilation = self.calc_kerr_time_dilation()
        self.frame_dragging = self.calc_frame_dragging()
        self.doppler_shift = self.calc_doppler_effect()
        self.total_dilation = self.calc_total_dilation()
        self.tidal_force = self.calc_tidal_forces()
        self.escape_velocity = self.calc_escape_velocity()
        self.orbital_velocity = self.calc_orbital_velocity()
        self.hawking_temp = self.calc_hawking_temperature()
        self.bekenstein_hawking_entropy = self.calc_bekenstein_entropy()
        self.gravitational_redshift = self.calc_gravitational_redshift()
        self.geodesic_precession = self.calc_geodesic_precession()
        self.kretschmann_scalar = self.calc_kretschmann_scalar()
        self.luminosity = self.calc_luminosity()
        
    def calculate_isco(self):
        """Calculate ISCO for Kerr black hole (prograde orbit)"""
        a = self.a
        Z1 = 1 + (1 - a**2)**(1/3) * ((1 + a)**(1/3) + (1 - a)**(1/3))
        Z2 = np.sqrt(3 * a**2 + Z1**2)
        r_isco = self.r_g * (3 + Z2 - np.sqrt((3 - Z1) * (3 + Z1 + 2*Z2)))
        return r_isco
    
    def calculate_photon_sphere(self):
        """Calculate photon sphere radius for Kerr metric"""
        return self.r_g * (2 * (1 + np.cos(2/3 * np.arccos(-self.a))))
    
    def calculate_ergosphere(self):
        """Calculate ergosphere radius at given theta"""
        return self.r_g * (1 + np.sqrt(1 - self.a**2 * np.cos(self.theta)**2))
    
    def calc_gravitational_dilation(self):
        """Schwarzschild time dilation"""
        if self.r <= self.Rs:
            return 0
        return np.sqrt(1 - (self.Rs / self.r))
    
    def calc_kerr_time_dilation(self):
        """Full Kerr metric time dilation"""
        if self.Delta <= 0:
            return 0
        g_tt = -(1 - self.Rs * self.r / self.Sigma)
        if g_tt >= 0:
            return 0
        return np.sqrt(-g_tt)
    
    def calc_frame_dragging(self):
        """Frame dragging angular velocity (Lense-Thirring effect)"""
        omega = (2 * self.a_kerr * G * self.M) / (C * self.r**3)
        return omega
    
    def calc_doppler_effect(self):
        """Special relativistic time dilation"""
        if self.v_obs >= C:
            return 0
        gamma = 1 / np.sqrt(1 - (self.v_obs / C)**2)
        return 1 / gamma
    
    def calc_total_dilation(self):
        """Combined gravitational and kinematic dilation"""
        if self.kerr_time_dilation == 0:
            return 0
        return self.kerr_time_dilation * self.doppler_shift
    
    def calc_tidal_forces(self):
        """Tidal acceleration gradient"""
        return (2 * G * self.M) / (self.r**3)
    
    def calc_escape_velocity(self):
        """Escape velocity at distance r"""
        v_esc = np.sqrt(2 * G * self.M / self.r)
        return min(v_esc / C, 1.0)
    
    def calc_orbital_velocity(self):
        """Circular orbital velocity"""
        v_orb = np.sqrt(G * self.M / self.r)
        return min(v_orb / C, 1.0)
    
    def calc_hawking_temperature(self):
        """Hawking temperature"""
        return (HBAR * C**3) / (8 * np.pi * K_B * G * self.M)
    
    def calc_bekenstein_entropy(self):
        """Bekenstein-Hawking entropy"""
        A = 4 * np.pi * (self.Rs / 2)**2 * (1 + np.sqrt(1 - self.a**2))
        return (K_B * C**3 * A) / (4 * G * HBAR)
    
    def calc_gravitational_redshift(self):
        """Gravitational redshift factor"""
        if self.gravitational_dilation == 0:
            return float('inf')
        return 1 / self.gravitational_dilation - 1
    
    def calc_geodesic_precession(self):
        """Geodesic precession rate"""
        return 6 * np.pi * G * self.M / (C**2 * self.r)
    
    def calc_kretschmann_scalar(self):
        """Kretschmann scalar (spacetime curvature invariant)"""
        return 48 * (G * self.M / C**2)**2 / self.r**6
    
    def calc_luminosity(self):
        """Hawking radiation luminosity"""
        A = 4 * np.pi * (self.Rs / 2)**2
        return STEFAN_BOLTZMANN * A * self.hawking_temp**4
    
    def calc_energy_extraction_efficiency(self):
        """Penrose process efficiency"""
        if self.a == 0:
            return 0.0
        return (1 - np.sqrt(1 - self.a**2)) * 100
    
    def calc_orbital_frequency(self):
        """Orbital frequency in Hz"""
        if self.orbital_velocity == 0:
            return 0
        return (self.orbital_velocity * C) / (2 * np.pi * self.r)
    
    def calc_specific_angular_momentum(self):
        """Specific angular momentum for circular orbit"""
        return self.r * self.orbital_velocity * C

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================
def format_time_elapsed(seconds):
    """Convert seconds to human-readable format"""
    years = seconds / (365.25 * 24 * 3600)
    
    if years >= 1e12:
        return f"{years/1e12:.3f} Trillion Years"
    elif years >= 1e9:
        return f"{years/1e9:.3f} Billion Years"
    elif years >= 1e6:
        return f"{years/1e6:.3f} Million Years"
    elif years >= 1000:
        return f"{years/1000:.3f} Thousand Years"
    elif years >= 1:
        days = (years % 1) * 365.25
        hours = (days % 1) * 24
        return f"{int(years)} Years, {int(days)} Days, {int(hours)} Hours"
    else:
        days = years * 365.25
        if days >= 1:
            hours = (days % 1) * 24
            minutes = (hours % 1) * 60
            return f"{int(days)} Days, {int(hours)} Hours, {int(minutes)} Minutes"
        else:
            hours = days * 24
            if hours >= 1:
                minutes = (hours % 1) * 60
                seconds_rem = (minutes % 1) * 60
                return f"{int(hours)} Hours, {int(minutes)} Minutes, {int(seconds_rem)} Seconds"
            else:
                minutes = hours * 60
                seconds_rem = (minutes % 1) * 60
                return f"{int(minutes)} Minutes, {int(seconds_rem)} Seconds"

def format_scientific(value, precision=3):
    """Format number in scientific notation"""
    return f"{value:.{precision}e}"

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================
def create_matplotlib_visualization(calc):
    """Create comprehensive matplotlib visualization"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 14))
    fig.patch.set_facecolor('#0e1117')
    
    # Plot 1: Schwarzschild Geometry
    ax1.set_facecolor('#1a1c24')
    theta = np.linspace(0, 2*np.pi, 1000)
    
    # Event horizon
    eh_x = calc.Rs/1e9 * np.cos(theta)
    eh_y = calc.Rs/1e9 * np.sin(theta)
    ax1.fill(eh_x, eh_y, color='black', alpha=1)
    ax1.plot(eh_x, eh_y, color='#ff3366', linewidth=3, label='Event Horizon')
    
    # Ergosphere
    if calc.a > 0:
        erg_x = calc.r_ergosphere/1e9 * np.cos(theta)
        erg_y = calc.r_ergosphere/1e9 * np.sin(theta)
        ax1.plot(erg_x, erg_y, '-.', color='#ff3366', linewidth=2, label='Ergosphere', alpha=0.5)
    
    # Photon sphere
    ps_x = calc.r_photon/1e9 * np.cos(theta)
    ps_y = calc.r_photon/1e9 * np.sin(theta)
    ax1.plot(ps_x, ps_y, '--', color='#ffcc00', linewidth=2, label='Photon Sphere', alpha=0.7)
    
    # ISCO
    isco_x = calc.r_isco/1e9 * np.cos(theta)
    isco_y = calc.r_isco/1e9 * np.sin(theta)
    ax1.plot(isco_x, isco_y, '--', color='#00ffcc', linewidth=2, label='ISCO', alpha=0.7)
    
    # Observer position
    pos_angle = np.pi/4
    pos_x = calc.r/1e9 * np.cos(pos_angle)
    pos_y = calc.r/1e9 * np.sin(pos_angle)
    ax1.plot(pos_x, pos_y, 'o', color='#00ff00', markersize=15, label='Observer', zorder=5)
    
    # Accretion disk rings
    for i in range(8):
        radius = calc.r_isco/1e9 + i * calc.Rs/1e9 * 0.3
        alpha_val = 0.4 - i*0.04
        circle = Circle((0, 0), radius, fill=False, color='#ff9933', 
                       alpha=max(alpha_val, 0.05), linewidth=1.5)
        ax1.add_patch(circle)
    
    max_radius = max(calc.r/1e9*1.5, calc.r_isco/1e9*2)
    ax1.set_xlim(-max_radius, max_radius)
    ax1.set_ylim(-max_radius, max_radius)
    ax1.set_xlabel('Distance (million km)', color='white', fontsize=11)
    ax1.set_ylabel('Distance (million km)', color='white', fontsize=11)
    ax1.set_title('Schwarzschild Geometry & Critical Radii', color='#00ffcc', 
                 fontsize=13, fontweight='bold')
    ax1.tick_params(colors='white')
    ax1.legend(loc='upper right', facecolor='#1a1c24', edgecolor='#00ffcc', 
              labelcolor='white', fontsize=9)
    ax1.grid(True, alpha=0.2, color='#444')
    ax1.set_aspect('equal')
    
    # Plot 2: Time Dilation Profile
    ax2.set_facecolor('#1a1c24')
    r_range = np.linspace(calc.Rs * 1.001, calc.Rs * 20, 2000)
    dilation_curve = []
    for r_val in r_range:
        if r_val > calc.Rs:
            dil = 1 / np.sqrt(1 - calc.Rs / r_val)
            dilation_curve.append(dil)
        else:
            dilation_curve.append(np.nan)
    
    ax2.plot(r_range/calc.Rs, dilation_curve, color='#00ffcc', linewidth=3)
    ax2.axvline(calc.r/calc.Rs, color='#ff3366', linestyle='--', linewidth=2, 
               label=f'Current: {calc.r/calc.Rs:.4f} Rs')
    if calc.gravitational_dilation > 0:
        ax2.axhline(1/calc.gravitational_dilation, color='#ff3366', linestyle='--', 
                   linewidth=2, alpha=0.5)
    
    ax2.set_xlabel('Distance (Schwarzschild Radii)', color='white', fontsize=11)
    ax2.set_ylabel('Time Dilation Factor', color='white', fontsize=11)
    ax2.set_title('Gravitational Time Dilation Profile', color='#00ffcc', 
                 fontsize=13, fontweight='bold')
    ax2.set_xlim(1, 20)
    ax2.tick_params(colors='white')
    ax2.legend(facecolor='#1a1c24', edgecolor='#00ffcc', labelcolor='white', fontsize=9)
    ax2.grid(True, alpha=0.2, color='#444')
    ax2.set_yscale('log')
    
    # Plot 3: Tidal Forces
    ax3.set_facecolor('#1a1c24')
    r_range_tidal = np.linspace(calc.Rs * 1.001, calc.Rs * 50, 2000)
    tidal_forces = (2 * G * calc.M) / (r_range_tidal**3)
    
    ax3.plot(r_range_tidal/calc.Rs, tidal_forces, color='#ff3366', linewidth=3)
    ax3.axvline(calc.r/calc.Rs, color='#00ffcc', linestyle='--', linewidth=2, 
               label=f'Current: {calc.tidal_force:.2e} m/s²/m')
    ax3.axhline(10, color='#ffcc00', linestyle=':', linewidth=2, 
               label='Human tolerance (~10 m/s²/m)', alpha=0.7)
    
    ax3.set_xlabel('Distance (Schwarzschild Radii)', color='white', fontsize=11)
    ax3.set_ylabel('Tidal Gradient (m/s²/m)', color='white', fontsize=11)
    ax3.set_title('Tidal Force Gradient (Spaghettification)', color='#00ffcc', 
                 fontsize=13, fontweight='bold')
    ax3.tick_params(colors='white')
    ax3.legend(facecolor='#1a1c24', edgecolor='#00ffcc', labelcolor='white', fontsize=9)
    ax3.grid(True, alpha=0.2, color='#444')
    ax3.set_yscale('log')
    
    # Plot 4: Effective Potential
    ax4.set_facecolor('#1a1c24')
    r_pot = np.linspace(calc.Rs * 1.5, calc.Rs * 30, 2000)
    
    L_values = [2.5, 3, 3.5, 4, 5]
    colors = ['#ff3366', '#ff6699', '#ffcc00', '#00ffcc', '#9933ff']
    
    for L, color in zip(L_values, colors):
        V_eff = -1/r_pot + L**2/(2*r_pot**2) - (calc.Rs * L**2)/(r_pot**3)
        ax4.plot(r_pot/calc.Rs, V_eff * 1e6, color=color, linewidth=2.5, 
                label=f'L = {L}√(GM/c)', alpha=0.8)
    
    ax4.axvline(calc.r/calc.Rs, color='white', linestyle='--', linewidth=2, alpha=0.5)
    ax4.axvline(calc.r_isco/calc.Rs, color='#00ffcc', linestyle=':', linewidth=2, 
               label='ISCO', alpha=0.7)
    
    ax4.set_xlabel('Distance (Schwarzschild Radii)', color='white', fontsize=11)
    ax4.set_ylabel('Effective Potential (×10⁻⁶)', color='white', fontsize=11)
    ax4.set_title('Effective Potential for Orbital Motion', color='#00ffcc', 
                 fontsize=13, fontweight='bold')
    ax4.tick_params(colors='white')
    ax4.legend(facecolor='#1a1c24', edgecolor='#00ffcc', labelcolor='white', fontsize=8)
    ax4.grid(True, alpha=0.2, color='#444')
    ax4.set_ylim(-4, 1)
    
    plt.tight_layout()
    return fig

def create_plotly_3d_visualization(calc):
    """Create interactive 3D visualization of spacetime curvature"""
    # Create grid for embedding diagram
    u = np.linspace(0, 2*np.pi, 100)
    v = np.linspace(0, calc.r*3, 100)
    U, V = np.meshgrid(u, v)
    
    # Calculate embedding surface (simplified)
    depth = -np.sqrt(np.maximum(calc.Rs - V, 0)) * 0.5
    
    X = V * np.cos(U)
    Y = V * np.sin(U)
    Z = depth
    
    fig = go.Figure(data=[go.Surface(
        x=X/1e9, y=Y/1e9, z=Z/1e9,
        colorscale=[
            [0, '#0e1117'],
            [0.3, '#1a1c24'],
            [0.5, '#ff3366'],
            [0.7, '#9933ff'],
            [1, '#00ffcc']
        ],
        showscale=False,
        opacity=0.9
    )])
    
    # Add event horizon circle
    theta_eh = np.linspace(0, 2*np.pi, 100)
    x_eh = calc.Rs/1e9 * np.cos(theta_eh)
    y_eh = calc.Rs/1e9 * np.sin(theta_eh)
    z_eh = np.zeros_like(x_eh)
    
    fig.add_trace(go.Scatter3d(
        x=x_eh, y=y_eh, z=z_eh,
        mode='lines',
        line=dict(color='#ff3366', width=5),
        name='Event Horizon'
    ))
    
    fig.update_layout(
        scene=dict(
            xaxis=dict(backgroundcolor='#0e1117', gridcolor='#333', showbackground=True, 
                      title='X (million km)', tickfont=dict(color='#00ffcc')),
            yaxis=dict(backgroundcolor='#0e1117', gridcolor='#333', showbackground=True,
                      title='Y (million km)', tickfont=dict(color='#00ffcc')),
            zaxis=dict(backgroundcolor='#0e1117', gridcolor='#333', showbackground=True,
                      title='Curvature', tickfont=dict(color='#00ffcc')),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
        ),
        paper_bgcolor='#0e1117',
        plot_bgcolor='#0e1117',
        title=dict(
            text='3D Spacetime Embedding Diagram',
            font=dict(color='#00ffcc', size=18, family='Orbitron')
        ),
        font=dict(color='#00ffcc'),
        showlegend=True,
        legend=dict(bgcolor='#1a1c24', bordercolor='#00ffcc', font=dict(color='#00ffcc')),
        height=600
    )
    
    return fig

# ============================================================================
# MAIN APPLICATION
# ============================================================================
def main():
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">⚛️ RELATIVISTIC SPACETIME ANALYZER ⚛️</div>
        <div class="hero-subtitle">Journey to the Edge of Black Holes - Where Time Itself Breaks Down</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Controls
    with st.sidebar:
        st.markdown("## 🎛️ CONTROL PARAMETERS")
        
        # Preset scenarios
        st.markdown("### 🎬 Preset Scenarios")
        scenario = st.selectbox(
            "Select Scenario",
            ["Custom", "Miller's Planet (Interstellar)", "Sagittarius A*", "M87*", "Stellar Black Hole", "Maximum Spin Test"]
        )
        
        # Apply presets
        if scenario == "Miller's Planet (Interstellar)":
            default_mass = 100.0
            default_dist = 3.5
            default_spin = 0.998
            default_vel = 0.0
        elif scenario == "Sagittarius A*":
            default_mass = 4.3
            default_dist = 8.0
            default_spin = 0.5
            default_vel = 0.0
        elif scenario == "M87*":
            default_mass = 6500.0
            default_dist = 10.0
            default_spin = 0.9
            default_vel = 0.0
        elif scenario == "Stellar Black Hole":
            default_mass = 0.01
            default_dist = 5.0
            default_spin = 0.7
            default_vel = 0.0
        elif scenario == "Maximum Spin Test":
            default_mass = 100.0
            default_dist = 2.0
            default_spin = 0.998
            default_vel = 0.0
        else:
            default_mass = 100.0
            default_dist = 3.0
            default_spin = 0.0
            default_vel = 0.0
        
        st.markdown("### 🌌 Primary Controls")
        
        mass = st.slider(
            "Black Hole Mass (×10⁶ M☉)",
            min_value=0.001,
            max_value=10000.0,
            value=default_mass,
            step=0.1,
            help="Mass of the black hole in millions of solar masses"
        )
        
        distance_log = st.slider(
            "Distance Offset (log₁₀ meters)",
            min_value=-5.0,
            max_value=10.0,
            value=default_dist,
            step=0.01,
            help="Distance from event horizon on logarithmic scale"
        )
        
        st.markdown("### ⚡ Advanced Parameters")
        
        spin = st.slider(
            "Spin Parameter (a/M)",
            min_value=0.0,
            max_value=0.998,
            value=default_spin,
            step=0.001,
            help="0 = Schwarzschild (non-rotating), 0.998 = near-extremal Kerr"
        )
        
        velocity = st.slider(
            "Observer Velocity (fraction of c)",
            min_value=0.0,
            max_value=0.99,
            value=default_vel,
            step=0.001,
            help="Velocity as fraction of speed of light"
        )
        
        theta = st.slider(
            "Polar Angle θ (radians)",
            min_value=0.0,
            max_value=np.pi,
            value=np.pi/2,
            step=0.01,
            help="Angle from rotation axis (π/2 = equatorial plane)"
        )
        
        st.markdown("---")
        st.markdown("### 📊 Export Options")
        
        if st.button("📥 Export Data as CSV"):
            calc = RelativisticCalculator(mass, distance_log, spin, velocity, theta)
            data = {
                "Parameter": ["Mass (×10⁶ M☉)", "Distance (Rs)", "Spin", "Velocity (c)", 
                             "Time Dilation", "Escape Velocity", "Orbital Velocity",
                             "Tidal Force", "Hawking Temp"],
                "Value": [mass, calc.r/calc.Rs, spin, velocity,
                         1/calc.total_dilation if calc.total_dilation > 0 else float('inf'),
                         calc.escape_velocity, calc.orbital_velocity,
                         calc.tidal_force, calc.hawking_temp]
            }
            df = pd.DataFrame(data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"spacetime_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    # Calculate physics
    calc = RelativisticCalculator(mass, distance_log, spin, velocity, theta)
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard", "🔬 Physics Analysis", "📈 Visualizations", 
        "🧮 Advanced Metrics", "📚 Education"
    ])
    
    with tab1:
        # Time displacement highlight
        hour_on_planet = 3600
        if calc.total_dilation > 0:
            earth_seconds = hour_on_planet / calc.total_dilation
            earth_time_str = format_time_elapsed(earth_seconds)
            
            st.markdown(f"""
            <div class="highlight-box">
                <div style="font-size: 1.5rem; color: #ffcc00; font-weight: 700;">
                    ⏱️ TEMPORAL DISPLACEMENT CALCULATION
                </div>
                <div style="margin: 1rem 0; color: white; font-size: 1.2rem;">
                    For every <span style="color: #00ffcc; font-weight: 900;">1 HOUR</span> experienced by the observer:
                </div>
                <div class="highlight-value">
                    {earth_time_str}
                </div>
                <div style="color: #ffcc00; font-size: 1.2rem; margin-top: 0.5rem;">
                    passes on Earth
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("⚠️ SINGULARITY REACHED: Inside event horizon - time dilation is infinite!")
        
        # Key metrics grid
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Time Dilation Factor",
                f"{1/calc.total_dilation:,.2f}×" if calc.total_dilation > 0 else "∞",
                delta="Gravitational + Kinematic"
            )
        
        with col2:
            st.metric(
                "Distance from Center",
                f"{calc.r/calc.Rs:.6f} Rs",
                delta=f"{(calc.r-calc.Rs)/1e3:.2f} km from horizon"
            )
        
        with col3:
            st.metric(
                "Escape Velocity",
                f"{calc.escape_velocity:.6f} c",
                delta=f"{calc.escape_velocity*C/1e3:.0f} km/s"
            )
        
        with col4:
            st.metric(
                "Tidal Gradient",
                f"{calc.tidal_force:.2e} m/s²/m",
                delta="Spaghettification"
            )
        
        # Danger warning
        spaghettification = calc.tidal_force * 2  # 2m human
        if spaghettification > 100:
            st.markdown(f"""
            <div class="warning-box">
                <div class="warning-box-title">⚠️ EXTREME DANGER ZONE</div>
                <p style="color: #ff6666; font-size: 1.1rem;">
                    Tidal forces exceed survivable limits! Structural integrity of any object would be compromised.
                    A 2-meter tall human would experience <strong>{spaghettification:.2e} m/s²</strong> differential force.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Black hole parameters
        st.markdown("### 🌌 Black Hole Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">Total Mass</div>
                <div class="metric-card-value">{calc.M:.3e} kg</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">Schwarzschild Radius</div>
                <div class="metric-card-value">{calc.Rs/1e6:.4f} million km</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">ISCO Radius</div>
                <div class="metric-card-value">{calc.r_isco/1e6:.4f} million km</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">Photon Sphere</div>
                <div class="metric-card-value">{calc.r_photon/1e6:.4f} million km</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">Hawking Temperature</div>
                <div class="metric-card-value">{calc.hawking_temp:.3e} K</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">Spin Parameter</div>
                <div class="metric-card-value">{spin:.3f}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("## ⚡ Relativistic Effects Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Gravitational Dilation", 
                     f"{1/calc.gravitational_dilation:,.4f}×" if calc.gravitational_dilation > 0 else "∞")
            st.metric("Kerr Time Dilation",
                     f"{1/calc.kerr_time_dilation:,.4f}×" if calc.kerr_time_dilation > 0 else "∞")
            st.metric("Kinematic Dilation (SR)",
                     f"{1/calc.doppler_shift:,.4f}×")
        
        with col2:
            st.metric("Gravitational Redshift (z)",
                     f"{calc.gravitational_redshift:.6f}" if calc.gravitational_redshift != float('inf') else "∞")
            st.metric("Frame Dragging (ω)",
                     f"{calc.frame_dragging:.3e} rad/s")
            st.metric("Geodesic Precession",
                     f"{np.degrees(calc.geodesic_precession):.6f}°/orbit")
        
        with col3:
            st.metric("Kretschmann Scalar",
                     f"{calc.kretschmann_scalar:.3e} m⁻⁴")
            st.metric("Bekenstein Entropy",
                     f"{calc.bekenstein_hawking_entropy:.3e} J/K")
            st.metric("Hawking Luminosity",
                     f"{calc.luminosity:.3e} W")
        
        st.markdown("---")
        st.markdown("## 🚀 Orbital Mechanics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            orbital_period = 2 * np.pi * calc.r / (calc.orbital_velocity * C) if calc.orbital_velocity > 0 else 0
            orbital_freq = calc.calc_orbital_frequency()
            
            st.metric("Circular Orbital Velocity",
                     f"{calc.orbital_velocity:.6f} c",
                     delta=f"{calc.orbital_velocity*C:,.0f} m/s")
            st.metric("Orbital Period",
                     f"{orbital_period/3600:.3f} hours" if orbital_period > 0 else "N/A")
            st.metric("Orbital Frequency",
                     f"{orbital_freq:.6e} Hz" if orbital_freq > 0 else "N/A")
        
        with col2:
            spec_ang_mom = calc.calc_specific_angular_momentum()
            
            st.metric("Specific Angular Momentum",
                     f"{spec_ang_mom:.3e} m²/s")
            
            if spin > 0:
                penrose_eff = calc.calc_energy_extraction_efficiency()
                st.metric("Penrose Process Efficiency",
                         f"{penrose_eff:.2f}%",
                         delta="Energy extraction from rotation")
            
            st.metric("Distance to ISCO",
                     f"{abs(calc.r - calc.r_isco)/1e3:.2f} km",
                     delta="Stable orbit boundary")
        
        st.markdown("---")
        st.markdown("## 💀 Tidal Forces & Structural Stress")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Tidal Gradient",
                     f"{calc.tidal_force:.3e} m/s²/m")
            st.metric("Spaghettification Force (2m object)",
                     f"{spaghettification:.3e} m/s²",
                     delta=f"{spaghettification/9.81:,.0f} g")
        
        with col2:
            # Calculate stretch for different objects
            stretch_1m = calc.tidal_force * 1
            stretch_10m = calc.tidal_force * 10
            
            st.metric("Tidal Force (1m separation)",
                     f"{stretch_1m:.3e} m/s²")
            st.metric("Tidal Force (10m separation)",
                     f"{stretch_10m:.3e} m/s²")
    
    with tab3:
        st.markdown("## 📊 Scientific Visualizations")
        
        # Matplotlib visualization
        with st.spinner("Generating matplotlib visualizations..."):
            fig_mpl = create_matplotlib_visualization(calc)
            st.pyplot(fig_mpl)
            plt.close()
        
        st.markdown("---")
        
        # 3D Plotly visualization
        st.markdown("### 🌐 Interactive 3D Spacetime Curvature")
        with st.spinner("Generating 3D visualization..."):
            fig_3d = create_plotly_3d_visualization(calc)
            st.plotly_chart(fig_3d, use_container_width=True)
        
        # Additional Plotly charts
        st.markdown("---")
        st.markdown("### 📈 Interactive Analysis Plots")
        
        # Time dilation vs distance
        r_range = np.linspace(calc.Rs * 1.01, calc.Rs * 50, 1000)
        dilation_vals = []
        for r in r_range:
            if r > calc.Rs:
                dilation_vals.append(1 / np.sqrt(1 - calc.Rs / r))
            else:
                dilation_vals.append(np.nan)
        
        fig_dilation = go.Figure()
        fig_dilation.add_trace(go.Scatter(
            x=r_range/calc.Rs,
            y=dilation_vals,
            mode='lines',
            name='Time Dilation',
            line=dict(color='#00ffcc', width=3)
        ))
        fig_dilation.add_vline(x=calc.r/calc.Rs, line_dash="dash", line_color="#ff3366",
                              annotation_text="Current Position")
        fig_dilation.update_layout(
            title="Time Dilation vs Distance",
            xaxis_title="Distance (Schwarzschild Radii)",
            yaxis_title="Time Dilation Factor",
            yaxis_type="log",
            paper_bgcolor='#0e1117',
            plot_bgcolor='#1a1c24',
            font=dict(color='#00ffcc'),
            xaxis=dict(gridcolor='#333'),
            yaxis=dict(gridcolor='#333')
        )
        st.plotly_chart(fig_dilation, use_container_width=True)
    
    with tab4:
        st.markdown("## 🧮 Advanced Metrics & Calculations")
        
        # Comprehensive data table
        data = {
            "Metric": [
                "Black Hole Mass",
                "Schwarzschild Radius",
                "ISCO Radius",
                "Photon Sphere Radius",
                "Ergosphere Radius (θ=π/2)",
                "Observer Distance",
                "Distance in Rs",
                "Proximity to Horizon",
                "Gravitational Time Dilation",
                "Kerr Time Dilation",
                "Total Time Dilation",
                "Gravitational Redshift",
                "Frame Dragging Frequency",
                "Geodesic Precession",
                "Escape Velocity",
                "Orbital Velocity",
                "Orbital Period",
                "Orbital Frequency",
                "Tidal Gradient",
                "Kretschmann Scalar",
                "Hawking Temperature",
                "Bekenstein-Hawking Entropy",
                "Hawking Luminosity",
                "Specific Angular Momentum"
            ],
            "Value": [
                f"{calc.M:.6e} kg",
                f"{calc.Rs:.6e} m",
                f"{calc.r_isco:.6e} m",
                f"{calc.r_photon:.6e} m",
                f"{calc.r_ergosphere:.6e} m",
                f"{calc.r:.6e} m",
                f"{calc.r/calc.Rs:.8f}",
                f"{(calc.r-calc.Rs):.6e} m",
                f"{1/calc.gravitational_dilation:.6e}×" if calc.gravitational_dilation > 0 else "∞",
                f"{1/calc.kerr_time_dilation:.6e}×" if calc.kerr_time_dilation > 0 else "∞",
                f"{1/calc.total_dilation:.6e}×" if calc.total_dilation > 0 else "∞",
                f"{calc.gravitational_redshift:.6e}" if calc.gravitational_redshift != float('inf') else "∞",
                f"{calc.frame_dragging:.6e} rad/s",
                f"{calc.geodesic_precession:.6e} rad/orbit",
                f"{calc.escape_velocity:.8f} c",
                f"{calc.orbital_velocity:.8f} c",
                f"{2*np.pi*calc.r/(calc.orbital_velocity*C):.6e} s" if calc.orbital_velocity > 0 else "N/A",
                f"{calc.calc_orbital_frequency():.6e} Hz",
                f"{calc.tidal_force:.6e} m/s²/m",
                f"{calc.kretschmann_scalar:.6e} m⁻⁴",
                f"{calc.hawking_temp:.6e} K",
                f"{calc.bekenstein_hawking_entropy:.6e} J/K",
                f"{calc.luminosity:.6e} W",
                f"{calc.calc_specific_angular_momentum():.6e} m²/s"
            ],
            "Unit": [
                "kg", "m", "m", "m", "m", "m", "Rs", "m",
                "dimensionless", "dimensionless", "dimensionless",
                "dimensionless", "rad/s", "rad/orbit", "c", "c",
                "s", "Hz", "m/s²/m", "m⁻⁴", "K", "J/K", "W", "m²/s"
            ]
        }
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, height=800)
        
        # Additional calculations
        st.markdown("---")
        st.markdown("### 🔬 Specialized Calculations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Coordinate Time Differential")
            if calc.total_dilation > 0:
                coord_diff = (hour_on_planet / calc.total_dilation) - hour_on_planet
                st.write(f"**{coord_diff/86400:.6f}** days")
                st.write(f"**{coord_diff:,.2f}** seconds")
            else:
                st.write("Infinite (inside horizon)")
            
            st.markdown("#### Proximity in Planck Lengths")
            planck_distance = (calc.r - calc.Rs) / PLANCK_LENGTH
            st.write(f"**{planck_distance:.3e}** ℓₚ")
            
            st.markdown("#### Gravitational Binding Energy")
            binding = -G * calc.M / calc.r
            st.write(f"**{binding:.3e}** J/kg")
        
        with col2:
            if spin > 0:
                st.markdown("#### Penrose Process Analysis")
                penrose_eff = calc.calc_energy_extraction_efficiency()
                max_energy = calc.M * C**2 * penrose_eff / 100
                st.write(f"**Efficiency:** {penrose_eff:.3f}%")
                st.write(f"**Max Extractable Energy:** {max_energy:.3e} J")
                st.write(f"**Equivalent Mass:** {max_energy/C**2:.3e} kg")
            
            st.markdown("#### Schwarzschild Radius Ratios")
            st.write(f"**r/Rs:** {calc.r/calc.Rs:.6f}")
            st.write(f"**r_ISCO/Rs:** {calc.r_isco/calc.Rs:.6f}")
            st.write(f"**r_photon/Rs:** {calc.r_photon/calc.Rs:.6f}")
    
    with tab5:
        st.markdown("## 📚 Educational Resources")
        
        st.markdown("""
        ### 🧮 The Science Behind the Simulator
        
        This simulator is based on rigorous calculations from Einstein's **General Theory of Relativity** 
        and the **Kerr Metric** for rotating black holes.
        """)
        
        # Expanders for educational content
        with st.expander("📐 Einstein Field Equations"):
            st.markdown("""
            The foundation of General Relativity:
            
            $$R_{\\mu\\nu} - \\frac{1}{2}g_{\\mu\\nu}R + \\Lambda g_{\\mu\\nu} = \\frac{8\\pi G}{c^4}T_{\\mu\\nu}$$
            
            Where:
            - $R_{\\mu\\nu}$ is the Ricci curvature tensor
            - $g_{\\mu\\nu}$ is the metric tensor
            - $R$ is the Ricci scalar
            - $\\Lambda$ is the cosmological constant
            - $T_{\\mu\\nu}$ is the stress-energy tensor
            """)
        
        with st.expander("🌀 Schwarzschild Metric"):
            st.markdown("""
            For non-rotating black holes:
            
            $$ds^2 = -\\left(1 - \\frac{R_s}{r}\\right)c^2dt^2 + \\left(1 - \\frac{R_s}{r}\\right)^{-1}dr^2 + r^2d\\Omega^2$$
            
            Schwarzschild radius:
            
            $$R_s = \\frac{2GM}{c^2}$$
            
            Time dilation factor:
            
            $$\\frac{t_{observer}}{t_{Earth}} = \\sqrt{1 - \\frac{R_s}{r}}$$
            """)
        
        with st.expander("⚫ Kerr Metric (Rotating Black Holes)"):
            st.markdown("""
            Much more complex! For rotating black holes:
            
            $$ds^2 = -\\left(1 - \\frac{R_s r}{\\Sigma^2}\\right)c^2dt^2 - \\frac{R_s r}{\\Sigma^2}a\\sin^2\\theta \\ c \\ dt \\ d\\phi$$
            $$+ \\frac{\\Sigma^2}{\\Delta}dr^2 + \\Sigma^2 d\\theta^2 + \\frac{\\sin^2\\theta}{\\Sigma^2}[(r^2+a^2)^2 - \\Delta a^2\\sin^2\\theta]d\\phi^2$$
            
            Where:
            - $\\Sigma^2 = r^2 + a^2\\cos^2\\theta$
            - $\\Delta = r^2 - R_s r + a^2$
            - $a = J/(Mc)$ is the spin parameter
            """)
        
        with st.expander("💫 Key Physical Concepts"):
            st.markdown("""
            **Event Horizon:** Point of no return
            $$r_{horizon} = R_s = \\frac{2GM}{c^2}$$
            
            **ISCO (Innermost Stable Circular Orbit):**
            - Non-rotating: $r_{ISCO} = 3R_s$
            - Maximally rotating (prograde): $r_{ISCO} ≈ R_s$
            
            **Photon Sphere:** Where light orbits
            $$r_{photon} = 1.5R_s$$
            
            **Frame Dragging:** Spacetime rotation
            $$\\omega = \\frac{2aGM}{cr^3}$$
            
            **Hawking Temperature:**
            $$T_H = \\frac{\\hbar c^3}{8\\pi k_B GM}$$
            
            **Bekenstein-Hawking Entropy:**
            $$S = \\frac{k_B c^3 A}{4G\\hbar}$$
            """)
        
        with st.expander("🎬 Real-World Black Holes"):
            st.markdown("""
            ### Famous Black Holes:
            
            **Sagittarius A*** (Milky Way Center)
            - Mass: ~4.3 million M☉
            - Schwarzschild Radius: ~12.7 million km
            - Distance from Earth: ~26,000 light-years
            
            **M87*** (First Photographed)
            - Mass: ~6.5 billion M☉
            - Schwarzschild Radius: ~19 billion km
            - Distance from Earth: ~55 million light-years
            
            **Gargantua** (Interstellar Movie)
            - Mass: ~100 million M☉
            - Near-maximal spin: a ≈ 0.998
            - Time dilation: ~61,000× near horizon
            """)
        
        st.markdown("---")
        st.markdown("""
        ### 📖 References
        
        1. Misner, C. W., Thorne, K. S., & Wheeler, J. A. (1973). *Gravitation*
        2. Carroll, S. M. (2004). *Spacetime and Geometry: An Introduction to General Relativity*
        3. Thorne, K. S. (2014). *The Science of Interstellar*
        4. Chandrasekhar, S. (1983). *The Mathematical Theory of Black Holes*
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p style='font-size: 0.9rem;'>
            <i>Calculations based on Einstein's General Relativity & Kerr Metric</i><br>
            <i>Physical Constants: G = 6.674×10⁻¹¹ m³kg⁻¹s⁻², c = 299,792,458 m/s</i>
        </p>
        <p style='font-size: 1.2rem; color: #00ffcc; margin-top: 1rem;'>
            Made with ⚛️ by the Laws of Physics
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
