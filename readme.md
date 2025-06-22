# DCGE Simulation Project

This repository provides a minimal dynamic computable general equilibrium (DCGE) simulation using a simple Cobb–Douglas production framework and social accounting table (SAM) calibration. It generates time-series outputs and Sankey diagrams for visualizing economic flows. The project can be run in under a day and produces publication-ready graphs for presentations or GitHub.

## Directory Structure

```
dcge_minimal/
├── data/
│   └── sam_base.csv       # Baseline Social Accounting Table (SAM)
├── results/              # Output files (graphs, CSV)
├── run_dcge.py           # Main simulation script
├── sam_base_new.csv      # Example SAM with investment values
├── README.md             # This file
└── requirements.txt      # Python dependencies
```

## Prerequisites

- Python 3.8+
- pandas
- matplotlib
- (Optional) plotly for interactive Sankey diagrams

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dcge_minimal.git
   cd dcge_minimal
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Data

- ``: Simplified social accounting table. Rows and columns correspond to sectors and institutional accounts (e.g., Agriculture, Manufacturing, Household, Investment, ValueAdded, etc.).
- You can update `sam_base.csv` or create your own SAM. Use `sam_base_new.csv` as an example including non-zero investment values.

## Running the Simulation

Execute the main script to run calibration, simulation, and visualization:

```bash
python run_dcge.py
```

This will:

- Calibrate consumption shares and investment share from your SAM.
- Simulate 20 periods of growth with Cobb–Douglas production.
- Generate the following in `results/`:
  - `dcge_simulation.csv`: Time-series data for Year, Output, Consumption, Investment, Capital.
  - `capital_path.png`: Capital stock path graph.
  - `dynamics.png`: Output, Consumption, Investment dynamics graph.

## Adding Technology Growth & Shock

The function `simulate_dcge_with_tech_shock` in `run_dcge.py` allows:

- **Technology growth**: Annual increase in productivity.
- **External shock**: Sudden drop in capital in a specified year. Example usage is included in the script; results saved as `capital_path_tech_shock.png` and `dynamics_tech_shock.png`.

## Sankey Diagram (Optional)

To visualize SAM flows:

```python
# In a Jupyter notebook or script
import pandas as pd
import plotly.graph_objects as go
# Load SAM and construct Sankey as shown in the notebook examples.
```

Adjust `x_positions` and `y_positions` to fine-tune node layout.

## Customization

- **Modify parameters** in `run_dcge.py`:
  - `delta`: capital depreciation rate
  - `alpha`: capital share in production
  - `inv_share`: proportion of output invested
  - `tech`: technology growth rate
  - `shock_year`, `shock_factor`
- **Change simulation horizon** by adjusting `T`.

## License

This project is released under the MIT License.

