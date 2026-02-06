# Process: Data Cleaning and Preparation

## Tools Chosen and Why
- **SQL (BigQuery‑style):** Handles multi‑million row datasets efficiently and enables reproducible analysis.
- **Excel:** Quick pivots and charts for communicating results.

## Data Preparation Steps
1. Downloaded 2019 quarterly trip data (Q1–Q4) CSVs.
2. Stored raw files in `data/raw/` and kept processed outputs in `data/processed/`.
3. Normalized Q2 column names to match the Q1/Q3/Q4 schema.
4. Converted trip duration to seconds (removed commas and decimals).
5. Parsed timestamps into consistent datetime format.
6. Created derived fields for analysis:
   - `day_of_week` (Mon–Sun)
   - `hour_of_day` (0–23)
   - `month`
   - `user_type` bucket (member/casual)

## Data Integrity Checks
- Dropped rows with missing `start_time` or `tripduration`.
- Excluded trips with non‑positive duration.
- Verified that user type values map cleanly to member/casual buckets.

## Cleaning Decisions (Documented)
- **Q2 schema mismatch:** renamed columns to align with other quarters.
- **Duration parsing:** handled values with commas (e.g., `1,048.0`).
- **Invalid records:** filtered out null timestamps or negative durations.

## Reproducibility
- `scripts/analyze_2019.py` recreates all summary tables.
- `sql/analysis.sql` provides BigQuery queries that match the Python outputs.
