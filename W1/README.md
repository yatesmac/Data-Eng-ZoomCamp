# 2025 Week 1 Homework - Docker

[Homework Link](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2025/01-docker-terraform/homework.md)

## Q1 Understanding docker first run

To run docker with the `python:3.12.8` image in an interactive mode, using the entrypoint `bash`:

```bash
docker run -it --entrypoint=bash python:3.12.8
```

From inside the docker bash run:

```bash
pip --version
```

## Data Ingestion

Before running the python notebook to create the tables in postgres,

Note: Docker Compose should run from the week 1 homework folder

1) Build the images

    ```bash
    docker-compose build
    ```

1) Run the images in detached mode:

    ```bash
    docker-compose up -d
    ```

1) Download the datasets:

    ```bash
    wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz -O taxi.csv
    ```
    
    ```bash
    wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv -O zones.csv
    ```

1) Install dependencies

    ``bash
    pip install pandas sqlalchemy psycopg2
    ```

To shut down the images running use:

```bash
docker-compose down
```

## Q3 Trip Segmentation Count

```sql
-- Up to 1 mile
SELECT COUNT(trip_distance) 
FROM green_taxi_trips
WHERE DATE(lpep_pickup_datetime) BETWEEN '2019-10-01' AND '2019-10-31'
AND DATE(lpep_dropoff_datetime) BETWEEN '2019-10-01' AND '2019-10-31'
AND trip_distance <= 1.0;

-- In between 1 (exclusive) and 3 miles (inclusive)
SELECT COUNT(trip_distance) 
FROM green_taxi_trips
WHERE DATE(lpep_pickup_datetime) BETWEEN '2019-10-01' AND '2019-10-31'
AND DATE(lpep_dropoff_datetime) BETWEEN '2019-10-01' AND '2019-10-31'
AND trip_distance > 1.0
AND trip_distance <= 3.0;

-- In between 3 (exclusive) and 7 miles (inclusive)
SELECT COUNT(trip_distance) 
FROM green_taxi_trips
WHERE DATE(lpep_pickup_datetime) BETWEEN '2019-10-01' AND '2019-10-31'
AND DATE(lpep_dropoff_datetime) BETWEEN '2019-10-01' AND '2019-10-31'
AND trip_distance > 3.0
AND trip_distance <= 7.0;

-- In between 7 (exclusive) and 10 miles (inclusive)
SELECT COUNT(trip_distance) 
FROM green_taxi_trips
WHERE DATE(lpep_pickup_datetime) BETWEEN '2019-10-01' AND '2019-10-31'
AND DATE(lpep_dropoff_datetime) BETWEEN '2019-10-01' AND '2019-10-31'
AND trip_distance > 7.0
AND trip_distance <= 10.0;

-- Over 10 miles
SELECT COUNT(trip_distance) 
FROM green_taxi_trips
WHERE DATE(lpep_pickup_datetime) BETWEEN '2019-10-01' AND '2019-10-31'
AND DATE(lpep_dropoff_datetime) BETWEEN '2019-10-01' AND '2019-10-31'
AND trip_distance > 10.0;
```

## Q4 Longest trip for each day

```sql
SELECT trip_day, MAX(max_trip)
FROM (
    SELECT DATE(lpep_pickup_datetime) AS trip_day, MAX(trip_distance) AS max_trip
    FROM green_taxi_data
    GROUP BY trip_day
);

```

## Q5 Three biggest pickup zones

```sql
SELECT zones."Zone", taxi.total_amount
FROM green_taxi_trips AS taxi
JOIN zones AS zones
ON taxi."PULocationID" = zones."LocationID"
WHERE DATE(lpep_pickup_datetime) = '2019-10-18'
AND taxi.total_amount > 13000
ORDER BY taxi.total_amount DESC
LIMIT 3
```

## Q6 Largest tip

```sql
SELECT zones."Borough", taxi.tip_amount
FROM green_taxi_trips AS taxi
JOIN (
    SELECT * 
    FROM zones 
    WHERE "Zone" = 'East Harlem North'
) AS zones
ON taxi."PULocationID" = zones."LocationID"
WHERE DATE(lpep_pickup_datetime) BETWEEN '2019-10-01' AND '2019-10-31'
ORDER BY taxi.tip_amount DESC
```
