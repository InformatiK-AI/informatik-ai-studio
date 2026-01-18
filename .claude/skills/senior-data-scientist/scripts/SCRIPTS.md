# Scripts Documentation

This directory contains executable scripts for the **senior-data-scientist** skill.

## Scripts Overview

| Script | Purpose | Status |
|--------|---------|--------|
| `experiment_designer.py` | Design A/B tests and experiments | Production |
| `feature_engineering_pipeline.py` | Create feature engineering pipelines | Production |
| `model_evaluation_suite.py` | Evaluate ML model performance | Production |

---

## experiment_designer.py

**Purpose:** Designs statistically rigorous A/B tests and experiments including sample size calculation and power analysis.

### Usage

```bash
python3 experiment_designer.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Experiment config or metrics |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Capabilities

- Sample size calculation
- Power analysis
- Minimum detectable effect
- Test duration estimation
- Segmentation strategy

---

## feature_engineering_pipeline.py

**Purpose:** Creates and manages feature engineering pipelines with transformation, encoding, and validation.

### Usage

```bash
python3 feature_engineering_pipeline.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Data source or pipeline config |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Transformations

- Numerical encoding
- Categorical encoding
- Text vectorization
- Time-based features
- Aggregations
- Feature crosses

---

## model_evaluation_suite.py

**Purpose:** Comprehensive ML model evaluation including metrics, calibration, and fairness analysis.

### Usage

```bash
python3 model_evaluation_suite.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Model predictions or config |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Evaluation Includes

- Classification metrics (precision, recall, F1, AUC)
- Regression metrics (RMSE, MAE, R²)
- Calibration curves
- Confusion matrices
- Fairness metrics
- Feature importance

### Dependencies

All scripts require Python 3.8+ (stdlib only)
