# climate-by-station-etl

## What? 
---
- This extracts, transforms, and loads climate data based upon input of station location(s) and years of data requested

## Why?
---
- To provide climate reports for rail networks in securing bids for heaters 

## How?
---
I. Extract

- Load NOAA data [NOAA's ghcn daily endpoint](https://www.ncei.noaa.gov/pub/data/ghcn/daily/by_station/)
  
II. Transform:

- Prune out missing data
- Calculate snow days from precipitation and minimum temperature
- Calculate average snow fall
- Calculate power required to melt snow by year

III. Load

- Output data locally to a pdf
- Email
- Rinse and Repeat

