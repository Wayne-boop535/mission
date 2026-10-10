import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

# ===== 原电路 =====
circuit = Circuit('Original')
circuit.V('dd', 'VDD', circuit.gnd, 5@u_V)
circuit.R(1, 'VDD', 'out', 1@u_kOhm)
circuit.R(2, 'out', circuit.gnd, 2@u_kOhm)
circuit.R('L', 'out', circuit.gnd, 1@u_kOhm)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.operating_point()

v_out_orig = float(analysis['out'][0])
i_rl_orig = v_out_orig / 1000.0
print(f"原电路 Vout = {v_out_orig:.4f} V")
print(f"原电路 I_RL = {i_rl_orig*1000:.4f} mA")

# ===== 戴维南等效电路 =====
circuit2 = Circuit('Thevenin Equivalent')
circuit2.V('th', 'th', circuit2.gnd, 3.333@u_V)
circuit2.R('th', 'th', 'load', 667@u_Ohm)
circuit2.R('L', 'load', circuit2.gnd, 1@u_kOhm)

simulator2 = circuit2.simulator(temperature=25, nominal_temperature=25)
analysis2 = simulator2.operating_point()

v_out_equiv = float(analysis2['load'][0])
i_rl_equiv = v_out_equiv / 1000.0
print(f"等效电路 Vout = {v_out_equiv:.4f} V")
print(f"等效电路 I_RL = {i_rl_equiv*1000:.4f} mA")

# ===== 误差 =====
print(f"Vout 误差 = {abs(v_out_orig - v_out_equiv)/v_out_orig*100:.2f}%")
print(f"I_RL 误差 = {abs(i_rl_orig - i_rl_equiv)/i_rl_orig*100:.2f}%")