import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
import numpy as np
import matplotlib.pyplot as plt

circuit = Circuit('RC Low Pass - Square Wave')

circuit.PulseVoltageSource('input', 'vin', circuit.gnd,
                           initial_value=0@u_V,
                           pulsed_value=1@u_V,
                           pulse_width=0.5@u_ms,
                           period=1@u_ms,
                           rise_time=1@u_ns,
                           fall_time=1@u_ns)

circuit.R(1, 'vin', 'vout', 1@u_kOhm)
circuit.C(1, 'vout', circuit.gnd, 1@u_uF)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=1@u_us, end_time=10@u_ms)  # 改成 10ms

time = np.array(analysis.time)
v_in = np.array(analysis['vin'])
v_out = np.array(analysis['vout'])

# 只取最后 1ms（稳态最后一个周期）
mask = time >= 9e-3
time_steady = time[mask]
v_out_steady = v_out[mask]

# 画图
plt.figure(figsize=(10, 5))
plt.plot(time*1000, v_in, label='Vin (square)', linewidth=1.5)
plt.plot(time*1000, v_out, label='Vout', linewidth=2)
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (V)')
plt.title('RC Low-Pass: Square Wave Response')
plt.legend()
plt.grid(True)
plt.savefig('rc_square_transient.png', dpi=150)
plt.show()

# 稳态峰峰值
v_pp = max(v_out_steady) - min(v_out_steady)
print("稳态输出最大值:", max(v_out_steady))
print("稳态输出最小值:", min(v_out_steady))
print("稳态输出峰峰值:", v_pp)