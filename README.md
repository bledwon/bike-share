# Cyclistic Bike-Share Case Study (2019)

## Overview
This project analyzes 2019 Cyclistic bike-share trips to understand how **annual members** and **casual riders** behave differently, with the goal of proposing marketing strategies that convert casual riders into members.

## Business Task
Identify behavioral differences between members and casual riders to support a conversion-focused marketing strategy.

## Tools
- SQL (BigQuery-style)
- Excel (pivot tables and charts)
- Python (standard library) for reproducible summaries

## Data Sources
- 2019 quarterly trip datasets (Q1–Q4) provided for the Cyclistic case study (Motivate International Inc.).
- Each file includes: trip_id, start/end time, duration, station info, user type, gender, and birth year.

## Analysis Highlights (2019)
- **Total rides:** 3,818,004
- **Member vs casual share:** 76.9% member (2,937,367) vs 23.1% casual (880,637)
- **Average ride length:** 14.3 min (member) vs 57.0 min (casual)
- **Weekend share:** 18.5% member vs 43.0% casual
- **Commute-window share of weekday rides (7–9am & 4–6pm):** 58.5% member vs 37.4% casual
- **Round-trip rate (same start/end station):** 1.62% member vs 11.88% casual
- **Long-ride share (>30 min):** 5.7% member vs 41.0% casual
- **Long-ride share (>60 min):** 0.42% member vs 16.5% casual
- **Peak day:** Tuesday (members) vs Saturday (casual)
- **Peak hour:** 5pm for both groups
- **Peak month:** August for both groups; lowest is February
- **Top start station:** Canal St & Adams St (members) vs Streeter Dr & Grand Ave (casual)

## Key Findings
- Members ride more frequently but for shorter durations, suggesting utilitarian/commute behavior.
- Casual riders are more weekend‑oriented and have significantly longer trips, indicating leisure use.
- Casual riders are much more likely to take round trips and long rides, reinforcing a recreational pattern.
- Both groups peak around 5pm, but member usage is concentrated on weekdays, while casual usage peaks on weekends.

## Recommendations (Top 3)
1. **Weekend conversion offers:** Market a “Weekend Explorer” membership trial to casual riders, since casual usage spikes on Saturdays and includes long rides.
2. **Commute‑focused messaging:** Promote member benefits (predictable costs, faster checkout) during weekday commute windows where member usage dominates.
3. **Station‑targeted campaigns:** Run geo‑targeted promotions at top casual stations like Streeter Dr & Grand Ave to capture high‑intent leisure riders.

## Repository Structure
- `data/raw/` — original 2019 quarterly CSVs
- `data/processed/` — Excel‑friendly summary tables
- `sql/analysis.sql` — BigQuery‑style SQL used to reproduce metrics
- `scripts/analyze_2019.py` — reproducible analysis script
- `process.md` — data cleaning and preparation steps
- `analysis.md` — deeper analysis narrative and chart ideas
- `case-study-answers.md` — explicit answers to the case study questions

## How to Reproduce
1. Load the four CSVs into BigQuery as `trips_2019_q1` … `trips_2019_q4`.
2. Run `sql/analysis.sql` to build a clean view and generate analysis tables.
3. Or run:
   ```bash
   python3 /Users/benledwon/Desktop/Github_connection/bike_share/scripts/analyze_2019.py
   ```
   to regenerate `data/processed/` outputs for Excel.

## Notes
- Analysis removes rows with missing timestamps or invalid/negative durations.
- All metrics reflect **2019 only**.
