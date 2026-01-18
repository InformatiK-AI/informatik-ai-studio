# Scripts Documentation

This directory contains executable scripts for the **senior-data-engineer** skill.

## Scripts Overview

| Script | Purpose | Status |
|--------|---------|--------|
| `pipeline_orchestrator.py` | Orchestrate data pipelines | Production |
| `data_quality_validator.py` | Validate data quality | Production |
| `etl_performance_optimizer.py` | Optimize ETL performance | Production |

---

## pipeline_orchestrator.py

**Purpose:** Orchestrates data pipeline execution, scheduling, and dependency management for ETL/ELT workflows.

### Usage

```bash
python3 pipeline_orchestrator.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Pipeline config or DAG file |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Supported Orchestrators

- Apache Airflow DAGs
- Prefect flows
- Dagster pipelines
- dbt models

---

## data_quality_validator.py

**Purpose:** Validates data quality using configurable rules, constraints, and statistical checks.

### Usage

```bash
python3 data_quality_validator.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Data source or validation config |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Validation Checks

- Schema validation
- Null checks
- Uniqueness constraints
- Range validation
- Statistical anomaly detection
- Referential integrity

---

## etl_performance_optimizer.py

**Purpose:** Analyzes and optimizes ETL pipeline performance, identifying bottlenecks and suggesting improvements.

### Usage

```bash
python3 etl_performance_optimizer.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Pipeline logs or metrics |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Analysis Includes

- Query optimization
- Partitioning recommendations
- Parallelization opportunities
- Memory/compute scaling
- Data skew detection

### Dependencies

All scripts require Python 3.8+ (stdlib only)
