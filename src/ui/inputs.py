"""Encapsulated input panels for the left-hand control column."""
from PySide6.QtWidgets import (QGroupBox, QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLabel, QPushButton, QComboBox, QDoubleSpinBox,
                               QTableWidget, QTableWidgetItem)

from src.core.properties import Mixture

# CoolProp fluid names keyed by the labels shown in the component selector.
COOLPROP_NAMES = {
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


class MixturePanel(QGroupBox):
    """Mixture composition editor; owns the underlying ``Mixture`` model.

    The shared ``PropertyCache`` is injected so every ``Mixture`` this panel
    creates reuses the same cache.
    """

    def __init__(self, props, parent=None):
        super().__init__("Mixture Composition", parent)
        self.props = props
        self.mixture = Mixture(props)
        layout = QVBoxLayout(self)
        comp_layout = QHBoxLayout()
        self.component_combo = QComboBox()
        self.component_combo.addItems(list(COOLPROP_NAMES.keys()))
        self.mole_fraction_input = QDoubleSpinBox()
        self.mole_fraction_input.setRange(0, 1)
        self.mole_fraction_input.setSingleStep(0.01)
        self.mole_fraction_input.setValue(1.0)
        self.mole_fraction_input.setDecimals(4)
        add_btn = QPushButton("Add Component")
        add_btn.clicked.connect(self.add_component)
        comp_layout.addWidget(QLabel("Fluid:"))
        comp_layout.addWidget(self.component_combo)
        comp_layout.addWidget(QLabel("Mole Fraction:"))
        comp_layout.addWidget(self.mole_fraction_input)
        comp_layout.addWidget(add_btn)
        layout.addLayout(comp_layout)
        self.component_table = QTableWidget(0, 2)
        self.component_table.setHorizontalHeaderLabels(["Component", "Mole Fraction"])
        self.component_table.setMaximumHeight(150)
        layout.addWidget(self.component_table)
        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.clear_components)
        layout.addWidget(clear_btn)

    def add_component(self):
        label = self.component_combo.currentText()
        mole_fraction = self.mole_fraction_input.value()
        self.mixture.add_component(COOLPROP_NAMES.get(label, label), mole_fraction)
        row = self.component_table.rowCount()
        self.component_table.insertRow(row)
        self.component_table.setItem(row, 0, QTableWidgetItem(label))
        self.component_table.setItem(row, 1, QTableWidgetItem(f"{mole_fraction:.4f}"))

    def clear_components(self):
        self.mixture = Mixture(self.props)
        self.component_table.setRowCount(0)


class OperatingConditionsPanel(QGroupBox):
    """Temperature / pressure / flow / head inputs."""

    def __init__(self, parent=None):
        super().__init__("Operating Conditions", parent)
        layout = QGridLayout(self)
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
        layout.addWidget(QLabel("Temperature:"), 0, 0)
        layout.addWidget(self.temp_input, 0, 1)
        layout.addWidget(QLabel("Pressure:"), 1, 0)
        layout.addWidget(self.pressure_input, 1, 1)
        layout.addWidget(QLabel("Flow Rate:"), 2, 0)
        layout.addWidget(self.flow_rate_input, 2, 1)
        layout.addWidget(QLabel("Head:"), 3, 0)
        layout.addWidget(self.head_input, 3, 1)

    def values(self):
        """Return (T [K], P [Pa], Q [m^3/s], H [m])."""
        return (self.temp_input.value(), self.pressure_input.value(),
                self.flow_rate_input.value(), self.head_input.value())


class PumpParametersPanel(QGroupBox):
    """Impeller diameter / rotation speed / efficiency inputs."""

    def __init__(self, parent=None):
        super().__init__("Pump Parameters", parent)
        layout = QGridLayout(self)
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
        layout.addWidget(QLabel("Impeller Diameter:"), 0, 0)
        layout.addWidget(self.impeller_diameter, 0, 1)
        layout.addWidget(QLabel("Rotation Speed:"), 1, 0)
        layout.addWidget(self.rotation_speed, 1, 1)
        layout.addWidget(QLabel("Efficiency:"), 2, 0)
        layout.addWidget(self.efficiency, 2, 1)

    def values(self):
        """Return (D_imp [m], N_rpm [rpm], eta [-])."""
        return (self.impeller_diameter.value(), self.rotation_speed.value(),
                self.efficiency.value())
