# Data Findings

Exploratory analysis run against the full dataset (14,656 records, `ypje-j649`, as of 2026-06-20).

---

## Coverage

- **Total records:** 14,656
- **Missing lat/lon:** 0 (0%) — every complaint can be mapped
- **Missing neighbourhood:** 1,953 (13.3%) — not a problem since we bin by lat/lon, not neighbourhood

---

## Volume by Year

| Year | Complaints |
|------|-----------|
| 2011 | 503 |
| 2012 | 716 |
| 2013 | 804 |
| 2014 | 881 |
| 2015 | 1,086 |
| 2016 | 1,022 |
| 2017 | 1,191 |
| 2018 | 981 |
| 2019 | 1,001 |
| 2020 | 791 |
| 2021 | 877 |
| 2022 | 1,244 |
| 2023 | 1,077 |
| 2024 | 908 |
| 2025 | 1,091 |
| 2026 | 483 (partial — mid-year) |

**Notes:**
- Steady growth 2011–2017
- Clear COVID dip in 2020
- 2022 is the all-time peak
- 2026 is on track to be similar to recent years

---

## Distribution by Day of Week

| Day | Complaints |
|-----|-----------|
| Mon | 2,159 |
| Tue | 2,392 |
| Wed | 2,429 |
| Thu | 2,303 |
| Fri | 2,283 |
| Sat | 1,448 |
| Sun | 1,642 |

**Notable:** Weekdays are noisier than weekends — Tuesday/Wednesday peak, Saturday lowest. Counterintuitive given the expectation of Friday/Saturday night noise. Worth surfacing prominently in the visualization.

---

## To Explore

- [ ] Time of day distribution (morning / afternoon / evening / night)
- [ ] Geographic clustering — which neighbourhoods or hex cells concentrate complaints
- [ ] Whether the weekday spike is driven by specific complaint types or times of day
