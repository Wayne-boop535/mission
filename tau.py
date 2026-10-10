import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
import numpy as np
import matplotlib.pyplot as plt

circuit = Circuit('RC Step Response')

# 阶跃信号：0V 跳到 1V，脉宽很长
circuit.PulseVoltageSource('input', 'vin', circuit.gnd,
                           initial_value=0@u_V,
                           pulsed_value=1@u_V,
                           delay_time=0@u_s,
                           rise_time=1@u_ns,
                           fall_time=1@u_ns,
                           pulse_width=10@u_ms,
                           period=20@u_ms)

circuit.R(1, 'vin', 'vout', 1@u_kOhm)
circuit.C(1, 'vout', circuit.gnd, 1@u_uF)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=1@u_us, end_time=5@u_ms)

time = np.array(analysis.time)
v_out = np.array(analysis['vout'])

# 找 0.632V 对应的时间
target = 0.632
idx = np.argmin(np.abs(v_out - target))
tau_sim = time[idx]

print(f"仿真 τ = {tau_sim*1000:.4f} ms")

plt.figure(figsize=(8, 4))
plt.plot(time*1000, v_out, linewidth=2)
plt.axhline(target, color='r', linestyle='--', label=f'63.2% = {target}V')
plt.axvline(tau_sim*1000, color='g', linestyle='--', label=f'τ={tau_sim*1000:.4f}ms')
plt.xlabel('Time (ms)')
plt.ylabel('Vout (V)')
plt.title('RC Step Response - τ Measurement')
plt.legend()
plt.grid(True)
plt.savefig('rc_step_tau.png', dpi=150)
plt.show()