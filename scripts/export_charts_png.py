#!/usr/bin/env python3
"""Export charts as PNGs from processed CSVs."""
from pathlib import Path
import csv
import matplotlib.pyplot as plt

BASE = Path('/Users/benledwon/Desktop/Github_connection/bike_share')
PROCESSED = BASE / 'data' / 'processed'
OUT = BASE / 'figures'
OUT.mkdir(parents=True, exist_ok=True)

DAY_FULL = {
    'Mon': 'Monday',
    'Tue': 'Tuesday',
    'Wed': 'Wednesday',
    'Thu': 'Thursday',
    'Fri': 'Friday',
    'Sat': 'Saturday',
    'Sun': 'Sunday',
}

plt.rcParams.update({
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'legend.fontsize': 10,
})


def read_csv(path):
    with path.open() as f:
        return list(csv.DictReader(f))


def pivot(rows, key, series, value):
    keys = []
    series_vals = []
    data = {}
    for r in rows:
        k = r[key]
        if k in DAY_FULL:
            k = DAY_FULL[k]
        s = r[series].capitalize()
        if s == 'Unknown':
            continue
        v = float(r[value])
        data.setdefault(k, {})[s] = v
        if k not in keys:
            keys.append(k)
        if s not in series_vals:
            series_vals.append(s)
    return keys, series_vals, data


def plot_bar(keys, series_vals, data, title, xlabel, ylabel, filename):
    fig, ax = plt.subplots(figsize=(10, 5.5))
    x = range(len(keys))
    width = 0.35
    for i, s in enumerate(series_vals):
        vals = [data.get(k, {}).get(s, 0) for k in keys]
        ax.bar([p + i*width for p in x], vals, width, label=s)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticks([p + width*(len(series_vals)-1)/2 for p in x])
    ax.set_xticklabels(keys, rotation=0)
    ax.grid(axis='y', alpha=0.25)
    ax.legend(loc='upper right')
    fig.tight_layout()
    fig.savefig(OUT / filename, dpi=200)
    plt.close(fig)


def plot_line(keys, series_vals, data, title, xlabel, ylabel, filename):
    fig, ax = plt.subplots(figsize=(10, 5.5))
    for s in series_vals:
        vals = [data.get(k, {}).get(s, 0) for k in keys]
        ax.plot(keys, vals, marker='o', label=s)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(axis='y', alpha=0.25)
    ax.legend(loc='upper right')
    fig.tight_layout()
    fig.savefig(OUT / filename, dpi=200)
    plt.close(fig)


def plot_share_bar(labels, series_vals, values, title, ylabel, filename):
    fig, ax = plt.subplots(figsize=(7.5, 5))
    x = range(len(labels))
    width = 0.35
    for i, s in enumerate(series_vals):
        ax.bar([p + i*width for p in x], values[s], width, label=s)
    ax.set_title(title)
    ax.set_xlabel('User Type')
    ax.set_ylabel(ylabel)
    ax.set_xticks([p + width*(len(series_vals)-1)/2 for p in x])
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1)
    ax.set_yticklabels([f'{int(t*100)}%' for t in ax.get_yticks()])
    ax.grid(axis='y', alpha=0.25)
    ax.legend(loc='upper right')
    fig.tight_layout()
    fig.savefig(OUT / filename, dpi=200)
    plt.close(fig)


# Rides by day of week
rows = read_csv(PROCESSED / 'rides_by_day_user.csv')
keys, series_vals, data = pivot(rows, 'day_of_week', 'user_type', 'ride_count')
plot_bar(keys, series_vals, data, 'Rides by Day of Week', 'Day', 'Rides', 'rides_by_day.png')

# Avg ride length by day
rows = read_csv(PROCESSED / 'avg_ride_seconds_by_day_user.csv')
keys, series_vals, data = pivot(rows, 'day_of_week', 'user_type', 'avg_ride_seconds')
plot_bar(keys, series_vals, data, 'Avg Ride Length by Day (sec)', 'Day', 'Seconds', 'avg_ride_by_day.png')

# Rides by month
rows = read_csv(PROCESSED / 'rides_by_month_user.csv')
keys, series_vals, data = pivot(rows, 'month', 'user_type', 'ride_count')
plot_line(keys, series_vals, data, 'Rides by Month', 'Month', 'Rides', 'rides_by_month.png')

# Rides by hour
rows = read_csv(PROCESSED / 'rides_by_hour_user.csv')
keys, series_vals, data = pivot(rows, 'hour_of_day', 'user_type', 'ride_count')
plot_line(keys, series_vals, data, 'Rides by Hour', 'Hour', 'Rides', 'rides_by_hour.png')

# Weekend vs weekday share
rows = read_csv(PROCESSED / 'summary_overall.csv')
labels = ['Member', 'Casual']
weekend = {}
weekday = {}
for r in rows:
    if r['user_type'] == 'unknown':
        continue
    user = r['user_type'].capitalize()
    weekend[user] = float(r['weekend_rides']) / (float(r['weekend_rides']) + float(r['weekday_rides']))
    weekday[user] = float(r['weekday_rides']) / (float(r['weekend_rides']) + float(r['weekday_rides']))
values = {
    'Weekend': [weekend['Member'], weekend['Casual']],
    'Weekday': [weekday['Member'], weekday['Casual']],
}
plot_share_bar(labels, ['Weekend', 'Weekday'], values, 'Weekend vs Weekday Share', 'Share', 'weekend_weekday_share.png')

# Long ride share
rows = read_csv(PROCESSED / 'long_ride_share.csv')
share_30 = {}
share_60 = {}
for r in rows:
    if r['user_type'] == 'unknown':
        continue
    user = r['user_type'].capitalize()
    share_30[user] = float(r['share_over_30m'])
    share_60[user] = float(r['share_over_60m'])
values = {
    '>30 min': [share_30['Member'], share_30['Casual']],
    '>60 min': [share_60['Member'], share_60['Casual']],
}
plot_share_bar(labels, ['>30 min', '>60 min'], values, 'Long Ride Share', 'Share', 'long_ride_share.png')

print('Exported PNG charts to figures/.')
