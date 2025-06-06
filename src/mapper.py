#!/usr/bin/env python3
import sys
import pandas as pd
import pyarrow.parquet as pq


def process_parquet(file_path):
    try:
        table = pq.read_table(file_path)
        df = table.to_pandas()

        for _, row in df.iterrows():
            fare = row.get('fare_amount', 0)
            distance = row.get('trip_distance', 0)
            pickup = row.get('tpep_pickup_datetime')
            dropoff = row.get('tpep_dropoff_datetime')
            duration = 0
            if pickup and dropoff:
                duration = (
                    pd.to_datetime(dropoff) - pd.to_datetime(pickup)
                ).total_seconds() / 60
            print(f"trip\t{fare},{distance},{duration}")
    except Exception as e:
        print(f"Error reading file {file_path}: {e}", file=sys.stderr)


if __name__ == "__main__":
    for line in sys.stdin:
        parquet_file = line.strip()
        process_parquet(parquet_file)
