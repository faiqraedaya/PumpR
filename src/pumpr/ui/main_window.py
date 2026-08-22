"""Main window: assembly of panels and orchestration of a calculation run."""
import traceback

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QTabWidget, QTextEdit, QMessageBox,
                               QFileDialog)
from PySide6.QtGui import QFont

from pumpr.core.units import rpm_to_rad_s
from pumpr.core.properties import PropertyCache
from pumpr.core.performance import PumpPerformance, compute_curve_data, compute_map_data
from pumpr.ui.plot_canvas import PlotCanvas
from pumpr.ui.plots import plot_performance_curves, plot_performance_maps
from pumpr.ui.inputs import MixturePanel, OperatingConditionsPanel, PumpParametersPanel
from pumpr.ui.report import build_results_text, write_curves_csv


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Single shared property cache injected into the mixture model.
        self.props = PropertyCache()
        self.last_curve_data = None  # cached for CSV export
        self.init_ui()
        self.mixture_panel.add_component()  # seed a default component

    def init_ui(self):
        self.setWindowTitle("PumpR")
        self.setGeometry(100, 100, 1600, 1200)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        left_panel = QWidget()
        left_panel.setMaximumWidth(400)
        left_layout = QVBoxLayout(left_panel)
        self.mixture_panel = MixturePanel(self.props)
        self.conditions_panel = OperatingConditionsPanel()
        self.pump_panel = PumpParametersPanel()
        left_layout.addWidget(self.mixture_panel)
        left_layout.addWidget(self.conditions_panel)
        left_layout.addWidget(self.pump_panel)
        calculate_btn = QPushButton("Calculate Performance")
        calculate_btn.clicked.connect(self.calculate_performance)
        calculate_btn.setMinimumHeight(40)
        left_layout.addWidget(calculate_btn)
        self.export_btn = QPushButton("Export Performance Curves (CSV)")
        self.export_btn.clicked.connect(self.export_curves)
        self.export_btn.setEnabled(False)
        left_layout.addWidget(self.export_btn)
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
        self.plot_widget = PlotCanvas()
        plots_layout.addWidget(self.plot_widget)
        right_panel.addTab(plots_tab, "Performance Curves")
        maps_tab = QWidget()
        maps_layout = QVBoxLayout(maps_tab)
        self.maps_widget = PlotCanvas()
        maps_layout.addWidget(self.maps_widget)
        right_panel.addTab(maps_tab, "Performance Maps")

        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 2)

    def calculate_performance(self):
        try:
            mixture = self.mixture_panel.mixture
            if len(mixture.components) == 0:
                QMessageBox.warning(self, "Warning", "Please add at least one component")
                return
            mixture.normalize_fractions()
            T, P, Q, H = self.conditions_panel.values()
            D_imp, N_rpm, eta = self.pump_panel.values()
            N = rpm_to_rad_s(N_rpm)
            rho, mu, cp, k = mixture.calculate_properties(T, P)
            P_vapor = mixture.vapor_pressure(T)
            performance = PumpPerformance.calculate_pump_performance(
                Q, H, rho, mu, D_imp, N, eta, P_inlet=P, P_vapor=P_vapor
            )
            pump = {'D_imp': D_imp, 'N_rpm': N_rpm, 'eta': eta}
            self.results_text.setText(build_results_text(
                mixture.components, mixture.mole_fractions, T, P, Q, H,
                rho, mu, cp, k, pump, performance))

            self.last_curve_data = compute_curve_data(Q, H, rho, mu, D_imp, N, eta)
            self.plot_widget.clear_plots()
            plot_performance_curves(self.plot_widget.figure, self.last_curve_data)
            self.plot_widget.canvas.draw()

            self.maps_widget.clear_plots()
            plot_performance_maps(self.maps_widget.figure,
                                  compute_map_data(Q, H, rho, N, eta))
            self.maps_widget.canvas.draw()

            self.export_btn.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Calculation failed:\n{str(e)}")
            traceback.print_exc()

    def export_curves(self):
        if not self.last_curve_data:
            QMessageBox.warning(self, "Warning", "Calculate performance first")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Export Performance Curves", "pump_curves.csv", "CSV Files (*.csv)"
        )
        if not path:
            return
        try:
            rows = write_curves_csv(path, self.last_curve_data)
            QMessageBox.information(self, "Export", f"Saved {rows} rows to:\n{path}")
        except OSError as e:
            QMessageBox.critical(self, "Error", f"Could not write file:\n{str(e)}")
