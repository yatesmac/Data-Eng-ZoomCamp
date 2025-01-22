import argparse

from time import time
from sqlalchemy import create_engine

import pandas as pd


def get_args():
	'''Get arguments from arg file.'''
	parser = argparse.ArgumentParser(fromfile_prefix_chars='@', description='Load CSV data to Local Volume using Postgres')
	parser.add_argument('--user', help='user name for postgres')
	parser.add_argument('--password', help='password for postgres')
	parser.add_argument('--host', help='host for postgres')
	parser.add_argument('--port', help='port for postgres')
	parser.add_argument('--db', help='database name for postgres')
	parser.add_argument('--table_name', help='name of the table where we will write the results to')
	parser.add_argument('--url', action='append', help='A list of CSV URLs')
	parser.parse_args('--url 1 --url 2'.split())

	return parser.parse_args()


def convert_datetime_columns(df):
	'''Convert to DateTime Format'''
	df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
	df['lpep_dropoff_datetime'] = pd.to_datetime(df['ltpep_dropoff_datetime'])

	return df


def main(args):
	user = args.user
	password = args.password
	host = args.host
	port = args.port
	db = args.db
	table_name = args.table_name
	url_taxi, url_zones = args.url

	# Create PG connector
	engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

	# Process the Taxi CSV
	# csv_name = 'taxi.csv'
	# os.system(f'wget {url_taxi} -O {csv_name}') # os.system runs commands from within python.
	df_iter = pd.read_csv(url_taxi, iterator=True, chunksize=100000)
	
	# Adding the first batch of rows
	df = next(df_iter)
	df = convert_datetime_columns(df)
	df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace') # Adding the column names
	df.to_sql(name=table_name, con=engine, if_exists='append')

	for df in df_iter:
		t_start = time()
		df = convert_datetime_columns(df)
		df.to_sql(name=table_name, con=engine, if_exists='append')
		t_end = time()

		print(f'Inserted another chunk... took {t_end - t_start:.3f} second(s)')

	# Process the Zones CSV
	df_zones=pd.read_csv(url_zones)
	table_name = 'zones'
	df_zones.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
	df_zones.to_sql(name=table_name, con=engine, if_exists='append')


if __name__ == '__main__':
	args = get_args()
	main(args)
