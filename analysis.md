# Analysis Summary (2019)

## Executive Summary
In 2019, Cyclistic members generated **76.9%** of all rides and tended to take short, commute‑oriented trips (avg **14.3 min**). Casual riders took fewer rides but much longer trips (avg **57.0 min**), with strong weekend and leisure patterns. The usage gap is most visible in ride duration, weekend share, and round‑trip behavior.

## Core Metrics
- **Total rides:** 3,818,004
- **Member vs casual:** 2,937,367 (76.9%) vs 880,637 (23.1%)
- **Average ride length:** 14.3 min (member) vs 57.0 min (casual)
- **Weekend share:** 18.5% (member) vs 43.0% (casual)
- **Commute‑window share of weekday rides:** 58.5% (member) vs 37.4% (casual)
- **Round‑trip rate:** 1.62% (member) vs 11.88% (casual)
- **Long rides >30 min:** 5.7% (member) vs 41.0% (casual)
- **Long rides >60 min:** 0.42% (member) vs 16.5% (casual)

## Time Patterns
- **Peak day:** Tuesday for members, Saturday for casuals.
- **Peak hour:** 5pm for both groups.
- **Peak month:** August for both groups; lowest month is February.

## Station Patterns
- **Top member station:** Canal St & Adams St
- **Top casual station:** Streeter Dr & Grand Ave

## Interpretation
- Members behave like commuters: short rides, heavy weekday usage, and strong commute‑window concentration.
- Casual riders behave like leisure users: longer trips, more weekends, and more round‑trip rides.

## Visualizations (Included)
Charts are included in `figures/`:
- `Rides by Day of Week.png`
- `Ride by Month.png`
- `Rides by Hour.png`
- `Avg Ride Length (sec) by Day.png`
- `Member Trips by Day.png`
- `Casual Trips by Day.png`
- `Member Trips by Length.png`
- `Casual Trips by Length.png`

## Outputs
All summary tables are in `data/processed/`:
- `summary_overall.csv`
- `rides_by_day_user.csv`
- `avg_ride_seconds_by_day_user.csv`
- `rides_by_hour_user.csv`
- `rides_by_month_user.csv`
- `commute_share_weekday.csv`
- `round_trip_share.csv`
- `long_ride_share.csv`
- `top_start_stations_member.csv`
- `top_start_stations_casual.csv`
