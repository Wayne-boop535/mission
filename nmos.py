import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
import numpy as np
import matplotlib.pyplot as plt

print("===== NMOS共源放大电路仿真 =====")

circuit = Circuit('NMOS Common Source')

# 电源与偏置
circuit.V('dd', 'VDD', circuit.gnd, 5@u_V)
circuit.R('g1', 'VDD', 'g', 60@u_kOhm)
circuit.R('g2', 'g', circuit.gnd, 40@u_kOhm)
circuit.R('d', 'VDD', 'd', 2@u_kOhm)
circuit.C('b1', 'vin', 'g', 1@u_mF)
circuit.SinusoidalVoltageSource('input', 'vin', circuit.gnd,
                                amplitude=10@u_mV, frequency=1@u_kHz)

# 2. 定义 NMOS 模型（修复了单位平方报错）
circuit.model('NMOS_model', 'NMOS',
              Vto=1,
              Kp=0.8e-3,
              Lambda=0.02)

circuit.MOSFET(1, 'd', 'g', circuit.gnd, circuit.gnd, model='NMOS_model')

sim = circuit.simulator(temperature=25, nominal_temperature=25)

# 直流工作点
op = sim.operating_point()
v_g = float(op['g'][0])
v_d = float(op['d'][0])
i_d = (5.0 - v_d) / 2000.0

print("\n----- 静态工作点（填入表格） -----")
print(f"V_GS = {v_g:.4f} V")
print(f"V_DS = {v_d:.4f} V")
print(f"I_D  = {i_d*1000:.4f} mA")
print(f"饱和区判断: V_DS({v_d:.2f}V) > V_GS-Vth({v_g-1:.2f}V) ? -> {v_d > (v_g-1)}")

# 瞬态分析
analysis = sim.transient(step_time=10@u_us, end_time=5@u_ms)
time = np.array(analysis.time)
v_in = np.array(analysis['vin'])
v_out = np.array(analysis['d'])

mask = time >= 4e-3
v_in_steady = v_in[mask]
v_out_steady = v_out[mask]

v_in_pp = max(v_in_steady) - min(v_in_steady)
v_out_pp = max(v_out_steady) - min(v_out_steady)
gain = v_out_pp / v_in_pp

print("\n----- 瞬态分析（填入表格） -----")
print(f"输入峰峰值 = {v_in_pp*1000:.4f} mV")
print(f"输出峰峰值 = {v_out_pp*1000:.4f} mV")
print(f"实测增益 Av = {gain:.4f}")

# 画图（反相放大）
v_out_ac = v_out - np.mean(v_out)

plt.figure(figsize=(10, 5))
plt.plot(time*1000, v_in*1000, label='Input (mV)', linewidth=1.5)
plt.plot(time*1000, v_out_ac*1000, label='Output AC (mV)', linewidth=2)
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (mV)')
plt.title('NMOS Common Source Amplifier (AC component)')
plt.legend()
plt.grid(True)
plt.savefig('nmos_cs_transient.png', dpi=150)
plt.show()
# ========== 追加：直流扫描法测 gm ==========
print("\n----- 仿真 gm（直流扫描法） -----")

# 新建一个专门用于测 gm 的电路
circuit_sweep = Circuit('GM Sweep')
circuit_sweep.V('dd', 'VDD', circuit_sweep.gnd, 5@u_V)

# 栅极直接加一个可以扫描的电压源（因为源极接地，所以 V_G = V_GS）
circuit_sweep.V('gate', 'g', circuit_sweep.gnd, 2@u_V)

circuit_sweep.R('d', 'VDD', 'd', 2@u_kOhm)
circuit_sweep.model('NMOS_model', 'NMOS', Vto=1, Kp=0.8e-3, Lambda=0.02)
circuit_sweep.MOSFET(1, 'd', 'g', circuit_sweep.gnd, circuit_sweep.gnd, model='NMOS_model')

sim_sweep = circuit_sweep.simulator(temperature=25, nominal_temperature=25)

# 扫描 V_G 从 1.9V 到 2.1V，步长 0.01V
sweep = sim_sweep.dc(Vgate=slice(1.9, 2.1, 0.01))

vgs_vals = np.array(sweep['g'])
vd_vals = np.array(sweep['d'])
id_vals = (5.0 - vd_vals) / 2000.0

# 找到 V_GS = 2.0V 对应的点
idx_mid = np.argmin(np.abs(vgs_vals - 2.0))

# 用中心差分法计算斜率，这就是 gm
gm_sim = (id_vals[idx_mid+1] - id_vals[idx_mid-1]) / (vgs_vals[idx_mid+1] - vgs_vals[idx_mid-1])

print(f"【填入表格】仿真 gm = {gm_sim*1000:.4f} mA/V")
print("✅ gm 仿真完成！")
print("\n✅ NMOS仿真完成，图片已保存为 nmos_cs_transient.png")