import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

# ===== 测开路电压 Voc =====
circuit = Circuit('Voc Test')
circuit.V('dd', 'VDD', circuit.gnd, 5@u_V)
circuit.R(1, 'VDD', 'out', 1@u_kOhm)
circuit.R(2, 'out', circuit.gnd, 2@u_kOhm)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.operating_point()
voc = float(analysis['out'][0])
print(f"Voc = {voc:.4f} V")

# ===== 测短路电流 Isc =====
circuit2 = Circuit('Isc Test')
circuit2.V('dd', 'VDD', circuit2.gnd, 5@u_V)
circuit2.R(1, 'VDD', 'out', 1@u_kOhm)
circuit2.R(2, 'out', circuit2.gnd, 2@u_kOhm)
circuit2.R('short', 'out', circuit2.gnd, 0.001@u_Ohm)

simulator2 = circuit2.simulator(temperature=25, nominal_temperature=25)
analysis2 = simulator2.operating_point()
v_out2 = float(analysis2['out'][0])
isc = v_out2 / 0.001
print(f"Isc = {isc*1000:.4f} mA")

# ===== 算等效电阻 =====
rth = voc / isc
print(f"Rth = Voc/Isc = {rth:.2f} Ω")