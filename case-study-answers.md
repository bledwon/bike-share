# Case Study Questions: Explicit Answers

## Ask
Q: What is the problem you are trying to solve?
A: Determine how annual members and casual riders use Cyclistic bikes differently to support a member‑conversion marketing strategy.

Q: How can your insights drive business decisions?
A: Behavioral differences (trip duration, day/time patterns, station usage) guide targeted campaigns, pricing, and messaging that improve conversion and retention.

## Prepare
Q: Where is your data located?
A: Raw CSVs are stored in `data/raw/` and processed outputs in `data/processed/`.

Q: How is the data organized?
A: Four quarterly CSVs (Q1–Q4 2019) with consistent trip‑level fields; Q2 uses different column names and was normalized.

Q: Are there issues with bias or credibility in this data? Does your data ROCCC?
A: The data is first‑party operational data, which is generally reliable. It is **Current (2019), Original, and Credible**, but not fully comprehensive for rider identity or motives due to privacy limitations.

Q: How are you addressing licensing, privacy, security, and accessibility?
A: The dataset is public and licensed for analysis; no personally identifiable information is used. Findings are reported in aggregate only.

Q: How did you verify the data’s integrity?
A: Checked for missing timestamps, non‑positive durations, and schema inconsistencies across quarters. Invalid rows were removed.

Q: How does it help you answer your question?
A: It provides trip‑level behavior across user types, enabling comparisons in time, duration, and station usage.

Q: Are there any problems with the data?
A: Q2 uses different column names and duration formatting; it required normalization. Some records have missing or invalid values that were filtered.

## Process
Q: What tools are you choosing and why?
A: SQL (BigQuery‑style) for scalable analysis and Excel for fast pivots and charts.

Q: Have you ensured your data’s integrity?
A: Yes. Rows with missing timestamps or invalid durations were removed, and column names were standardized.

Q: What steps have you taken to ensure that your data is clean?
A: Normalized Q2 schema, parsed timestamps, converted duration to seconds, and filtered invalid rows.

Q: How can you verify that your data is clean and ready to analyze?
A: Summary counts and sanity checks confirm reasonable totals, duration ranges, and consistent user‑type values.

Q: Have you documented your cleaning process so you can review and share those results?
A: Yes. See `process.md` and the reproducible `scripts/analyze_2019.py` and `sql/analysis.sql`.

## Analyze
Q: How should you organize your data to perform analysis on it?
A: Standardize columns and union quarterly files into a single year‑long table with derived fields (day, hour, month, user type).

Q: Has your data been properly formatted?
A: Yes. Dates are parsed to datetime and duration is numeric (seconds).

Q: What surprises did you discover in the data?
A: Casual riders have dramatically longer trips and a much higher round‑trip rate than members.

Q: What trends or relationships did you find in the data?
A: Members ride mostly on weekdays and during commute windows; casual riders peak on weekends and in long leisure rides.

Q: How will these insights help answer your business questions?
A: They show where and when to target casual riders with membership offers and which behaviors to emphasize in marketing.

## Share
Q: Were you able to answer the question of how annual members and casual riders use Cyclistic bikes differently?
A: Yes. Members show shorter, commute‑oriented weekday rides; casuals show longer, weekend‑heavy leisure rides.

Q: What story does your data tell?
A: Cyclistic has a strong commuter base among members and a leisure base among casual riders; the latter is the best conversion opportunity.

Q: How do your findings relate to your original question?
A: Findings quantify the behavioral differences that define member vs casual usage.

Q: Who is your audience? What is the best way to communicate with them?
A: The executive and marketing teams; concise dashboards and executive‑summary slides are most effective.

Q: Can data visualization help you share your findings?
A: Yes. Charts by day, hour, month, and duration reveal the most actionable differences.

Q: Is your presentation accessible to your audience?
A: Yes. Visuals use clear labels, color contrast, and short explanatory notes.

## Act
Q: What is your final conclusion based on your analysis?
A: Casual riders are leisure‑oriented and longer‑ride users; targeted weekend and station‑specific campaigns can convert them into members.

Q: How could your team and business apply your insights?
A: Launch weekend trials, station‑based promotions, and messaging that emphasizes value for longer rides.

Q: What next steps would you or your stakeholders take based on your findings?
A: Pilot conversion campaigns at top casual stations and evaluate conversion lift over 4–8 weeks.

Q: Is there additional data you could use to expand on your findings?
A: Weather, event schedules, and pricing experiments could clarify why casual riders convert and when they are most receptive.
