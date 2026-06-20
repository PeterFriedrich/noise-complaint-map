# Data

## Source

**Edmonton Open Data — Bylaw Complaint Details**

- Dataset ID: `ypje-j649`
- URL: `https://data.edmonton.ca/resource/ypje-j649.json`
- Coverage: January 1, 2011 to present
- Auth: Socrata API key (see `.env`)

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

## Open Questions

- How frequently does Edmonton refresh this dataset? (Determines cron cadence)
- Are Socrata field names above confirmed, or inferred from display names? (Verify with a small test query before building pipeline)
