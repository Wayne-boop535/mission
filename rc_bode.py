import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
import numpy as np
import matplotlib.pyplot as plt

circuit = Circuit('RC Low Pass - AC')

circuit.SinusoidalVoltageSource('input', 'vin', circuit.gnd,
                                amplitude=1@u_V, frequency=1@u_kHz)
circuit.R(1, 'vin', 'vout', 1@u_kOhm)
circuit.C(1, 'vout', circuit.gnd, 1@u_uF)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
ac = simulator.ac(start_frequency=10@u_Hz,
                  stop_frequency=100@u_kHz,
                  number_of_points=100,
                  variation='dec')

freq = np.array(ac.frequency)
v_out = np.abs(np.array(ac['vout']))
gain_db = 20 * np.log10(v_out)
phase_deg = np.angle(np.array(ac['vout']), deg=True)

# 找 -3dB 截止频率
idx_3db = np.argmin(np.abs(gain_db - (-3)))
fc_sim = freq[idx_3db]
print(f"仿真截止频率 fc = {fc_sim:.2f} Hz")

# 画波特图
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

ax1.semilogx(freq, gain_db, linewidth=2)
ax1.axvline(fc_sim, color='r', linestyle='--', label=f'fc={fc_sim:.1f}Hz')
ax1.axhline(-3, color='gray', linestyle=':', linewidth=1)
ax1.set_ylabel('Gain (dB)')
ax1.set_title('RC Low-Pass Bode Plot')
ax1.grid(True, which='both')
ax1.legend()

ax2.semilogx(freq, phase_deg, linewidth=2)
ax2.axvline(fc_sim, color='r', linestyle='--')
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Phase (deg)')
ax2.grid(True, which='both')

plt.tight_layout()
plt.savefig('rc_bode.png', dpi=150)
plt.show()

# 打印1kHz处增益
idx_1k = np.argmin(np.abs(freq - 1000))
print(f"1kHz 处增益 = {gain_db[idx_1k]:.2f} dB")
print(f"1kHz 处幅度 = {v_out[idx_1k]:.4f} V")