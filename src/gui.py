import sys
import numpy as np
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QTabWidget, QGroupBox, QDoubleSpinBox, QMessageBox, QTextEdit)
from PyQt5.QtGui import QFont
import traceback

from src.simulator import PumpSimulator
from src.performance import PumpPerformance
from src.matplotlib_widget import MatplotlibWidget

class PumpSimulatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.simulator = PumpSimulator()
        self.init_ui()
        self.set_default_values()

    def init_ui(self):
        self.setWindowTitle("Centrifugal Pump Simulator")
        self.setGeometry(100, 100, 1600, 1200)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        left_panel = QWidget()
        left_panel.setMaximumWidth(400)
        left_layout = QVBoxLayout(left_panel)
        mixture_group = QGroupBox("Mixture Composition")
        mixture_layout = QVBoxLayout(mixture_group)
        comp_layout = QHBoxLayout()
        self.component_combo = QComboBox()
        self.component_combo.addItems([
            'Water', 'Ethanol', 'Methanol', 'Propane', 'Butane', 
            'Nitrogen', 'Oxygen', 'CO2', 'Ammonia', 'Toluene'
        ])
        self.mole_fraction_input = QDoubleSpinBox()
        self.mole_fraction_input.setRange(0, 1)
        self.mole_fraction_input.setSingleStep(0.01)
        self.mole_fraction_input.setValue(1.0)
        self.mole_fraction_input.setDecimals(4)
        add_component_btn = QPushButton("Add Component")
        add_component_btn.clicked.connect(self.add_component)
        comp_layout.addWidget(QLabel("Fluid:"))
        comp_layout.addWidget(self.component_combo)
        comp_layout.addWidget(QLabel("Mole Fraction:"))
        comp_layout.addWidget(self.mole_fraction_input)
        comp_layout.addWidget(add_component_btn)
        mixture_layout.addLayout(comp_layout)
        self.component_table = QTableWidget(0, 2)
        self.component_table.setHorizontalHeaderLabels(["Component", "Mole Fraction"])
        self.component_table.setMaximumHeight(150)
        mixture_layout.addWidget(self.component_table)
        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.clear_components)
        mixture_layout.addWidget(clear_btn)
        left_layout.addWidget(mixture_group)
        conditions_group = QGroupBox("Operating Conditions")
        conditions_layout = QGridLayout(conditions_group)
        self.temp_input = QDoubleSpinBox()
        self.temp_input.setRange(200, 600)
        self.temp_input.setValue(298.15)
        self.temp_input.setSuffix(" K")
        self.pressure_input = QDoubleSpinBox()
        self.pressure_input.setRange(1000, 10000000)
        self.pressure_input.setValue(101325)
        self.pressure_input.setSuffix(" Pa")
        self.flow_rate_input = QDoubleSpinBox()
        self.flow_rate_input.setRange(0.001, 10)
        self.flow_rate_input.setValue(0.1)
        self.flow_rate_input.setSuffix(" m³/s")
        self.flow_rate_input.setDecimals(4)
        self.head_input = QDoubleSpinBox()
        self.head_input.setRange(1, 1000)
        self.head_input.setValue(50)
        self.head_input.setSuffix(" m")
        conditions_layout.addWidget(QLabel("Temperature:"), 0, 0)
        conditions_layout.addWidget(self.temp_input, 0, 1)
        conditions_layout.addWidget(QLabel("Pressure:"), 1, 0)
        conditions_layout.addWidget(self.pressure_input, 1, 1)
        conditions_layout.addWidget(QLabel("Flow Rate:"), 2, 0)
        conditions_layout.addWidget(self.flow_rate_input, 2, 1)
        conditions_layout.addWidget(QLabel("Head:"), 3, 0)
        conditions_layout.addWidget(self.head_input, 3, 1)
        left_layout.addWidget(conditions_group)
        pump_group = QGroupBox("Pump Parameters")
        pump_layout = QGridLayout(pump_group)
        self.impeller_diameter = QDoubleSpinBox()
        self.impeller_diameter.setRange(0.1, 2.0)
        self.impeller_diameter.setValue(0.3)
        self.impeller_diameter.setSuffix(" m")
        self.impeller_diameter.setDecimals(3)
        self.rotation_speed = QDoubleSpinBox()
        self.rotation_speed.setRange(100, 10000)
        self.rotation_speed.setValue(1750)
        self.rotation_speed.setSuffix(" rpm")
        self.efficiency = QDoubleSpinBox()
        self.efficiency.setRange(0.1, 1.0)
        self.efficiency.setValue(0.75)
        self.efficiency.setDecimals(3)
        pump_layout.addWidget(QLabel("Impeller Diameter:"), 0, 0)
        pump_layout.addWidget(self.impeller_diameter, 0, 1)
        pump_layout.addWidget(QLabel("Rotation Speed:"), 1, 0)
        pump_layout.addWidget(self.rotation_speed, 1, 1)
        pump_layout.addWidget(QLabel("Efficiency:"), 2, 0)
        pump_layout.addWidget(self.efficiency, 2, 1)
        left_layout.addWidget(pump_group)
        calculate_btn = QPushButton("Calculate Performance")
        calculate_btn.clicked.connect(self.calculate_performance)
        calculate_btn.setMinimumHeight(40)
        left_layout.addWidget(calculate_btn)
        left_layout.addStretch()
        right_panel = QTabWidget()
        results_tab = QWidget()
        results_layout = QVBoxLayout(results_tab)
        self.results_text = QTextEdit()
        self.results_text.setFont(QFont("Courier", 10))
        results_layout.addWidget(self.results_text)
        right_panel.addTab(results_tab, "Results")
        plots_tab = QWidget()
        plots_layout = QVBoxLayout(plots_tab)
        self.plot_widget = MatplotlibWidget()
        plots_layout.addWidget(self.plot_widget)
        right_panel.addTab(plots_tab, "Performance Curves")
        maps_tab = QWidget()
        maps_layout = QVBoxLayout(maps_tab)
        self.maps_widget = MatplotlibWidget()
        maps_layout.addWidget(self.maps_widget)
        right_panel.addTab(maps_tab, "Performance Maps")
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 2)

    def set_default_values(self):
        self.add_component()

    def add_component(self):
        component = self.component_combo.currentText()
        mole_fraction = self.mole_fraction_input.value()
        coolprop_names = {
            'Water': 'Water',
            'Ethanol': 'Ethanol',
            'Methanol': 'Methanol',
            'Propane': 'Propane',
            'Butane': 'Butane',
            'Nitrogen': 'Nitrogen',
            'Oxygen': 'Oxygen',
            'CO2': 'CarbonDioxide',
            'Ammonia': 'Ammonia',
            'Toluene': 'Toluene'
        }
        coolprop_name = coolprop_names.get(component, component)
        self.simulator.add_component(coolprop_name, mole_fraction)
        row = self.component_table.rowCount()
        self.component_table.insertRow(row)
        self.component_table.setItem(row, 0, QTableWidgetItem(component))
        self.component_table.setItem(row, 1, QTableWidgetItem(f"{mole_fraction:.4f}"))

    def clear_components(self):
        self.simulator = PumpSimulator()
        self.component_table.setRowCount(0)

    def calculate_performance(self):
        try:
            if len(self.simulator.components) == 0:
                QMessageBox.warning(self, "Warning", "Please add at least one component")
                return
            self.simulator.normalize_fractions()
            T = self.temp_input.value()
            P = self.pressure_input.value()
            Q = self.flow_rate_input.value()
            H = self.head_input.value()
            D_imp = self.impeller_diameter.value()
            N_rpm = self.rotation_speed.value()
            eta = self.efficiency.value()
            N = N_rpm * 2 * np.pi / 60
            rho, mu, cp, k = self.simulator.calculate_mixture_properties(T, P)
            performance = PumpPerformance.calculate_pump_performance(
                Q, H, rho, mu, D_imp, N, eta
            )
            self.display_results(T, P, Q, H, rho, mu, cp, k, performance)
            self.generate_performance_curves(Q, H, rho, mu, D_imp, N, eta)
            self.generate_performance_maps(rho, mu, D_imp, N, eta)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Calculation failed:\n{str(e)}")
            traceback.print_exc()

    def display_results(self, T, P, Q, H, rho, mu, cp, k, performance):
        results = f"""
CENTRIFUGAL PUMP PERFORMANCE ANALYSIS
====================================

MIXTURE COMPOSITION:
{'-'*40}
"""
        for i, (comp, x) in enumerate(zip(self.simulator.components, self.simulator.mole_fractions)):
            results += f"Component {i+1}: {comp:<15} Mole Fraction: {x:.4f}\n"
        results += f"""
OPERATING CONDITIONS:
{'-'*40}
Temperature:           {T:.2f} K ({T-273.15:.2f} °C)
Pressure:              {P/1000:.1f} kPa
Flow Rate:             {Q:.4f} m³/s ({Q*3600:.1f} m³/h)
Head:                  {H:.2f} m

FLUID PROPERTIES:
{'-'*40}
Density:               {rho:.2f} kg/m³
Dynamic Viscosity:     {mu*1000:.4f} mPa·s
Specific Heat:         {cp/1000:.3f} kJ/kg·K
Thermal Conductivity:  {k:.4f} W/m·K

PUMP PARAMETERS:
{'-'*40}
Impeller Diameter:     {self.impeller_diameter.value():.3f} m
Rotation Speed:        {self.rotation_speed.value():.0f} rpm
Efficiency:            {self.efficiency.value()*100:.1f}%

PERFORMANCE RESULTS:
{'-'*40}
Flow Coefficient (φ):      {performance['phi']:.6f}
Head Coefficient (ψ):      {performance['psi']:.6f}
Reynolds Number:           {performance['Re']:.0f}
Specific Speed (Ns):       {performance['Ns']:.2f}
NPSH Required:             {performance['NPSH_req']:.2f} m

POWER ANALYSIS:
{'-'*40}
Hydraulic Power:       {performance['P_hydraulic']/1000:.2f} kW
Shaft Power:           {performance['P_shaft']/1000:.2f} kW
Power Loss:            {(performance['P_shaft']-performance['P_hydraulic'])/1000:.2f} kW

DIMENSIONLESS ANALYSIS:
{'-'*40}
Flow Coefficient:      {performance['phi']:.6f}
Head Coefficient:      {performance['psi']:.6f}
Power Coefficient:     {performance['P_shaft']/(rho*(self.rotation_speed.value()*2*np.pi/60)**3*self.impeller_diameter.value()**5):.6f}
"""
        self.results_text.setText(results)

    def generate_performance_curves(self, Q_design, H_design, rho, mu, D_imp, N, eta):
        self.plot_widget.clear_plots()
        Q_range = np.linspace(0.1*Q_design, 1.5*Q_design, 50)
        heads = []
        powers = []
        efficiencies = []
        npsh_req = []
        for Q in Q_range:
            H = H_design * (1.2 - 0.8*(Q/Q_design)**2)
            performance = PumpPerformance.calculate_pump_performance(
                Q, H, rho, mu, D_imp, N, eta
            )
            heads.append(H)
            powers.append(performance['P_shaft']/1000)
            efficiencies.append(performance['eta_pump']*100)
            npsh_req.append(performance['NPSH_req'])
        fig = self.plot_widget.figure
        fig.suptitle('Pump Performance Curves', fontsize=14, fontweight='bold')
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.plot(Q_range*3600, heads, 'b-', linewidth=2, label='Head')
        ax1.axvline(Q_design*3600, color='r', linestyle='--', alpha=0.7, label='Design Point')
        ax1.set_xlabel('Flow Rate (m³/h)')
        ax1.set_ylabel('Head (m)')
        ax1.set_title('Head vs Flow Rate')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.plot(Q_range*3600, powers, 'g-', linewidth=2, label='Power')
        ax2.axvline(Q_design*3600, color='r', linestyle='--', alpha=0.7, label='Design Point')
        ax2.set_xlabel('Flow Rate (m³/h)')
        ax2.set_ylabel('Power (kW)')
        ax2.set_title('Power vs Flow Rate')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        ax3 = fig.add_subplot(2, 2, 3)
        ax3.plot(Q_range*3600, efficiencies, 'm-', linewidth=2, label='Efficiency')
        ax3.axvline(Q_design*3600, color='r', linestyle='--', alpha=0.7, label='Design Point')
        ax3.set_xlabel('Flow Rate (m³/h)')
        ax3.set_ylabel('Efficiency (%)')
        ax3.set_title('Efficiency vs Flow Rate')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        ax4 = fig.add_subplot(2, 2, 4)
        ax4.plot(Q_range*3600, npsh_req, 'c-', linewidth=2, label='NPSH Required')
        ax4.axvline(Q_design*3600, color='r', linestyle='--', alpha=0.7, label='Design Point')
        ax4.set_xlabel('Flow Rate (m³/h)')
        ax4.set_ylabel('NPSH Required (m)')
        ax4.set_title('NPSH vs Flow Rate')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        fig.tight_layout()
        self.plot_widget.canvas.draw()

    def generate_performance_maps(self, rho, mu, D_imp, N_design, eta):
        self.maps_widget.clear_plots()
        N_range = np.linspace(0.7*N_design, 1.3*N_design, 5)
        Q_range = np.linspace(0.01, 0.2, 30)
        fig = self.maps_widget.figure
        fig.suptitle('Pump Performance Maps', fontsize=14, fontweight='bold')
        ax1 = fig.add_subplot(1, 2, 1)
        for N in N_range:
            heads = []
            for Q in Q_range:
                H = 100 * (N/N_design)**2 * (1.2 - 0.8*(Q/0.1)**2)
                heads.append(H)
            ax1.plot(Q_range*3600, heads, label=f'{N*60/(2*np.pi):.0f} rpm')
        ax1.set_xlabel('Flow Rate (m³/h)')
        ax1.set_ylabel('Head (m)')
        ax1.set_title('Head Map')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        ax2 = fig.add_subplot(1, 2, 2)
        for N in N_range:
            powers = []
            for Q in Q_range:
                H = 100 * (N/N_design)**2 * (1.2 - 0.8*(Q/0.1)**2)
                P = rho * 9.81 * Q * H / eta / 1000
                powers.append(P)
            ax2.plot(Q_range*3600, powers, label=f'{N*60/(2*np.pi):.0f} rpm')
        ax2.set_xlabel('Flow Rate (m³/h)')
        ax2.set_ylabel('Power (kW)')
        ax2.set_title('Power Map')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        fig.tight_layout()
        self.maps_widget.canvas.draw() 