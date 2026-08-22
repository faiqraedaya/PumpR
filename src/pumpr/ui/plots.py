"""Rendering of pump performance figures.

These functions render pre-computed data (from ``src.core.performance``) onto a
matplotlib Figure. They contain no calculation logic.
"""

def plot_performance_curves(figure, data):
    """Draw head / power / efficiency / NPSH curves onto ``figure``."""
    Q = data['Q_m3h']
    Q_design = data['Q_design_m3h']
    figure.suptitle('Pump Performance Curves', fontsize=14, fontweight='bold')
    panels = [
        (1, data['head'], 'b-', 'Head (m)', 'Head vs Flow Rate', 'Head'),
        (2, data['power_kw'], 'g-', 'Power (kW)', 'Power vs Flow Rate', 'Power'),
        (3, data['eff_pct'], 'm-', 'Efficiency (%)', 'Efficiency vs Flow Rate', 'Efficiency'),
        (4, data['npsh_req'], 'c-', 'NPSH Required (m)', 'NPSH vs Flow Rate', 'NPSH Required'),
    ]
    for pos, y, style, ylabel, title, label in panels:
        ax = figure.add_subplot(2, 2, pos)
        ax.plot(Q, y, style, linewidth=2, label=label)
        ax.axvline(Q_design, color='r', linestyle='--', alpha=0.7, label='Design Point')
        ax.set_xlabel('Flow Rate (m³/h)')
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        ax.legend()
    figure.tight_layout()


def plot_performance_maps(figure, series):
    """Draw head and power curve families (one curve per speed) onto ``figure``."""
    figure.suptitle('Pump Performance Maps', fontsize=14, fontweight='bold')
    ax1 = figure.add_subplot(1, 2, 1)
    ax2 = figure.add_subplot(1, 2, 2)
    for s in series:
        label = f"{s['rpm']:.0f} rpm"
        ax1.plot(s['Q_m3h'], s['head'], label=label)
        ax2.plot(s['Q_m3h'], s['power_kw'], label=label)
    ax1.set_xlabel('Flow Rate (m³/h)')
    ax1.set_ylabel('Head (m)')
    ax1.set_title('Head Map')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax2.set_xlabel('Flow Rate (m³/h)')
    ax2.set_ylabel('Power (kW)')
    ax2.set_title('Power Map')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    figure.tight_layout()
