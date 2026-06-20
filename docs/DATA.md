# Data

## Source

**Edmonton Open Data — Bylaw Complaint Details**

- Dataset ID: `ypje-j649`
- URL: `https://data.edmonton.ca/resource/ypje-j649.json`
- Coverage: January 1, 2011 to present
- Auth: basic auth (`SOCRATA_API_KEY_ID:SOCRATA_API_KEY_SECRET` from `.env`) — the app token header (`X-App-Token`) does not work with these credentials

## Noise Complaint Filter

All pipeline queries must filter on:

```
complaint_category = 'Noise'
```

~14,656 noise records as of project start.

## Fields

| Column | Socrata Field Name | Type | Notes |
|---|---|---|---|
| Row ID | `row_id` | Number | |
| Year | `year` | Number | |
| Month | `month` | Text | |
| Date Created | `date_created` | Calendar Date | Use to derive day of week |
| Complaint Category | `complaint_category` | Text | Filter: `= 'Noise'` |
| Type of Complaint | `type_of_complaint` | Text | Subcategory |
| Was Cannabis Involved | `was_cannabis_involved` | Text | |
| Officer Initiated | `officer_initiated` | Text | |
| Infraction Status | `infraction_status` | Text | |
| Neighbourhood ID | `neighbourhood_id` | Text | |
| Neighbourhood | `neighbourhood` | Text | |
| Full Name of Street | `full_name_of_street` | Text | |
| Count | `count` | Number | |
| Latitude | `latitude` | Number | Per-complaint lat/lon available |
| Longitude | `longitude` | Number | |
| Location | `location` | Location | Combined geo field |

## Update Frequency

Dataset is updated **daily** (confirmed via Socrata metadata). Pipeline cron should run once per day, overnight.

## Notes (from live test query)

- All field names above confirmed via `$limit=5` test query
- `type_of_complaint` is always `"Noise"` for noise complaints — no useful subcategory data
- `neighbourhood` and `neighbourhood_id` can be missing (some records have no neighbourhood)
- `count` is always `"1.0"` — one row per complaint, not pre-aggregated
