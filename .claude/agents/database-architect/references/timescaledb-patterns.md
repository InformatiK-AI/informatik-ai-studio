# TimescaleDB Patterns Reference

This document provides comprehensive patterns and best practices for TimescaleDB time-series database design.

## Hypertables and Chunking

### Creating Hypertables
```sql
-- Create regular PostgreSQL table
CREATE TABLE metrics (
  time        TIMESTAMPTZ NOT NULL,
  device_id   TEXT NOT NULL,
  temperature DOUBLE PRECISION,
  humidity    DOUBLE PRECISION,
  pressure    DOUBLE PRECISION
);

-- Convert to hypertable (automatic chunking by time)
SELECT create_hypertable('metrics', 'time');

-- With custom chunk interval (7 days)
SELECT create_hypertable(
  'metrics',
  'time',
  chunk_time_interval => INTERVAL '7 days'
);

-- With space partitioning (for high-cardinality data)
SELECT create_hypertable(
  'metrics',
  'time',
  partitioning_column => 'device_id',
  number_partitions => 4
);
```

### Chunk Management
```sql
-- View chunks
SELECT * FROM timescaledb_information.chunks
WHERE hypertable_name = 'metrics'
ORDER BY range_start DESC;

-- Drop old chunks
SELECT drop_chunks('metrics', INTERVAL '90 days');

-- Move chunks to different tablespace
SELECT move_chunk(
  chunk => '_timescaledb_internal._hyper_1_1_chunk',
  destination_tablespace => 'archive_tablespace'
);

-- Reorder chunk for better performance
SELECT reorder_chunk('_timescaledb_internal._hyper_1_1_chunk', 'metrics_device_time_idx');
```

## Continuous Aggregates

### Creating Continuous Aggregates
```sql
-- Hourly aggregates
CREATE MATERIALIZED VIEW metrics_hourly
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 hour', time) AS bucket,
  device_id,
  AVG(temperature) AS avg_temp,
  MIN(temperature) AS min_temp,
  MAX(temperature) AS max_temp,
  AVG(humidity) AS avg_humidity,
  COUNT(*) AS sample_count
FROM metrics
GROUP BY bucket, device_id
WITH NO DATA;

-- Daily aggregates
CREATE MATERIALIZED VIEW metrics_daily
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 day', time) AS bucket,
  device_id,
  AVG(temperature) AS avg_temp,
  MIN(temperature) AS min_temp,
  MAX(temperature) AS max_temp,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY temperature) AS median_temp
FROM metrics
GROUP BY bucket, device_id
WITH NO DATA;
```

### Refresh Policies
```sql
-- Add automatic refresh policy
SELECT add_continuous_aggregate_policy(
  'metrics_hourly',
  start_offset => INTERVAL '3 hours',
  end_offset => INTERVAL '1 hour',
  schedule_interval => INTERVAL '1 hour'
);

-- Manual refresh
CALL refresh_continuous_aggregate('metrics_hourly', '2024-01-01', '2024-01-31');

-- View refresh policies
SELECT * FROM timescaledb_information.continuous_aggregate_stats;
```

### Hierarchical Aggregates
```sql
-- Monthly aggregates from hourly (faster than raw data)
CREATE MATERIALIZED VIEW metrics_monthly
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 month', bucket) AS bucket,
  device_id,
  AVG(avg_temp) AS avg_temp,
  MIN(min_temp) AS min_temp,
  MAX(max_temp) AS max_temp
FROM metrics_hourly
GROUP BY time_bucket('1 month', bucket), device_id
WITH NO DATA;
```

## Compression Policies

### Enable Compression
```sql
-- Enable compression on hypertable
ALTER TABLE metrics SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'device_id',
  timescaledb.compress_orderby = 'time DESC'
);

-- Add automatic compression policy
SELECT add_compression_policy('metrics', INTERVAL '7 days');

-- Manual compression
SELECT compress_chunk('_timescaledb_internal._hyper_1_1_chunk');

-- Compress all chunks older than 7 days
SELECT compress_chunk(i) FROM show_chunks('metrics', older_than => INTERVAL '7 days') i;
```

### Compression Stats
```sql
-- View compression stats
SELECT
  hypertable_name,
  chunk_name,
  before_compression_total_bytes,
  after_compression_total_bytes,
  (1 - after_compression_total_bytes::float / before_compression_total_bytes) * 100 AS compression_ratio
FROM timescaledb_information.compressed_chunk_stats
WHERE hypertable_name = 'metrics';

-- Total compression savings
SELECT
  pg_size_pretty(before_compression_total_bytes) AS before,
  pg_size_pretty(after_compression_total_bytes) AS after
FROM hypertable_compression_stats('metrics');
```

## Retention Policies

### Automatic Data Retention
```sql
-- Drop chunks older than 90 days automatically
SELECT add_retention_policy('metrics', INTERVAL '90 days');

-- Different retention for different tables
SELECT add_retention_policy('metrics_raw', INTERVAL '30 days');
SELECT add_retention_policy('metrics_hourly', INTERVAL '1 year');
SELECT add_retention_policy('metrics_daily', INTERVAL '5 years');

-- View retention policies
SELECT * FROM timescaledb_information.jobs
WHERE proc_name = 'policy_retention';
```

### Tiered Storage
```sql
-- Move old data to cheaper storage
SELECT add_tiering_policy(
  'metrics',
  INTERVAL '30 days',
  tablespace => 'slow_storage'
);
```

## Query Patterns for Time-Series

### Time Buckets
```sql
-- Aggregate by time bucket
SELECT
  time_bucket('1 hour', time) AS hour,
  device_id,
  AVG(temperature) AS avg_temp
FROM metrics
WHERE time > NOW() - INTERVAL '1 day'
GROUP BY hour, device_id
ORDER BY hour DESC;

-- Time bucket with offset (for timezone alignment)
SELECT
  time_bucket('1 day', time, INTERVAL '8 hours') AS day_pst,
  COUNT(*)
FROM metrics
GROUP BY day_pst;

-- Gapfilling for continuous time series
SELECT
  time_bucket_gapfill('1 hour', time) AS hour,
  device_id,
  locf(AVG(temperature)) AS temp  -- Last observation carried forward
FROM metrics
WHERE time > NOW() - INTERVAL '1 day'
  AND time <= NOW()
GROUP BY hour, device_id
ORDER BY hour;
```

### First/Last Aggregates
```sql
-- Get first and last values efficiently
SELECT
  device_id,
  first(temperature, time) AS first_temp,
  last(temperature, time) AS last_temp,
  first(time, time) AS first_time,
  last(time, time) AS last_time
FROM metrics
WHERE time > NOW() - INTERVAL '1 day'
GROUP BY device_id;
```

### Moving Averages
```sql
-- Simple moving average
SELECT
  time,
  temperature,
  AVG(temperature) OVER (
    ORDER BY time
    ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
  ) AS moving_avg
FROM metrics
WHERE device_id = 'sensor-001'
  AND time > NOW() - INTERVAL '1 hour'
ORDER BY time;

-- Time-weighted average
SELECT
  time_bucket('1 hour', time) AS hour,
  time_weight('Linear', time, temperature) AS time_weighted_avg
FROM metrics
WHERE device_id = 'sensor-001'
GROUP BY hour;
```

### Delta and Rate Calculations
```sql
-- Calculate rate of change
SELECT
  time,
  temperature,
  temperature - LAG(temperature) OVER (ORDER BY time) AS temp_delta,
  (temperature - LAG(temperature) OVER (ORDER BY time)) /
    EXTRACT(EPOCH FROM time - LAG(time) OVER (ORDER BY time)) AS rate_per_second
FROM metrics
WHERE device_id = 'sensor-001'
ORDER BY time DESC
LIMIT 100;

-- Counter reset handling
SELECT
  time_bucket('1 minute', time) AS minute,
  counter_agg(time, bytes_sent) AS counter_state
FROM network_metrics
GROUP BY minute;
```

### Percentiles and Stats
```sql
-- Percentile calculations
SELECT
  device_id,
  PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY temperature) AS p50,
  PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY temperature) AS p95,
  PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY temperature) AS p99
FROM metrics
WHERE time > NOW() - INTERVAL '1 day'
GROUP BY device_id;

-- Approximate percentiles (faster for large datasets)
SELECT
  device_id,
  approx_percentile(0.50, percentile_agg(temperature)) AS p50,
  approx_percentile(0.95, percentile_agg(temperature)) AS p95
FROM metrics
WHERE time > NOW() - INTERVAL '1 day'
GROUP BY device_id;
```

## Indexing for Time-Series

### Optimal Indexes
```sql
-- Default hypertable index (time, device_id)
CREATE INDEX ON metrics (device_id, time DESC);

-- For range queries on specific devices
CREATE INDEX ON metrics (device_id, time DESC)
  WHERE device_id IS NOT NULL;

-- For filtering by value ranges
CREATE INDEX ON metrics (time DESC)
  WHERE temperature > 100;  -- High temperature alerts

-- BRIN index for large time ranges
CREATE INDEX ON metrics USING BRIN (time);
```

## Integration with PostgreSQL

### Views for Latest Data
```sql
-- Materialized view for latest readings
CREATE MATERIALIZED VIEW latest_metrics AS
SELECT DISTINCT ON (device_id)
  device_id,
  time,
  temperature,
  humidity
FROM metrics
ORDER BY device_id, time DESC;

-- Refresh regularly
REFRESH MATERIALIZED VIEW CONCURRENTLY latest_metrics;
```

### Combining with Regular Tables
```sql
-- Device metadata in regular table
CREATE TABLE devices (
  id TEXT PRIMARY KEY,
  name TEXT,
  location TEXT,
  installed_at TIMESTAMPTZ
);

-- Join time-series with metadata
SELECT
  d.name,
  d.location,
  time_bucket('1 hour', m.time) AS hour,
  AVG(m.temperature) AS avg_temp
FROM metrics m
JOIN devices d ON m.device_id = d.id
WHERE m.time > NOW() - INTERVAL '1 day'
GROUP BY d.name, d.location, hour
ORDER BY hour DESC;
```

## Migration Strategy

```markdown
### Migration 1: Install TimescaleDB extension
- CREATE EXTENSION IF NOT EXISTS timescaledb;

### Migration 2: Create raw metrics table
- Create table with time, dimensions, and metrics columns
- Convert to hypertable with appropriate chunk interval

### Migration 3: Add indexes
- Create composite indexes for common query patterns
- Add partial indexes for specific filters

### Migration 4: Set up continuous aggregates
- Create hourly/daily/monthly aggregates
- Add refresh policies

### Migration 5: Configure compression
- Enable compression with segmentby/orderby
- Add compression policy

### Migration 6: Add retention
- Set retention policy based on data tier
- Configure tiered storage if needed
```

## Performance Tips

```markdown
1. **Chunk Sizing**: Match chunk interval to typical query range
   - Too small: query overhead from many chunks
   - Too large: slow chunk operations

2. **Segmentby for Compression**: Choose columns used in WHERE clauses

3. **Use Continuous Aggregates**: Pre-compute common aggregations

4. **Query Latest Data**: Use descending time indexes

5. **Batch Inserts**: Insert in time-ordered batches for best performance

6. **Monitor Chunk Count**: Keep reasonable number of chunks (hundreds, not thousands)
```
