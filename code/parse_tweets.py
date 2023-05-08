import os
import pickle
import pandas as pd

dirpath = '../tweets/'
date_range = [d.strftime('%Y-%m-%d') for d in pd.date_range('2021-10-01', '2022-03-31')]

"""
Parse data
"""
tweet_set = set()
tweet_to_author = {}
rf_records = {day:[] for day in date_range}

for filename in os.listdir(dirpath):
	filepath = dirpath + '/' + filename
	print('Processing ' + filename)
	with open(filepath, 'rb') as fp:
		raw_data = pickle.load(fp)
		for response in raw_data:
			df = pd.json_normalize(response[0])  # Batch of 100 tweet objects
			for row in df.itertuples():
				tweet_id = row.id
				author_id = row.author_id
				day = row.created_at[:10]
				if day in date_range:
					if tweet_id not in tweet_set:
						try:
							tweet_set.add(tweet_id)
							tweet_to_author[tweet_id] = author_id
							rf_tweets = row.referenced_tweets
							if isinstance(rf_tweets, list):
								rf_tweet = rf_tweets[0]
								rf_records[day].append((tweet_id, rf_tweet['id'], rf_tweet['type']))
						except Exception as e:
							print(row)

			df_rf = pd.json_normalize(response[2])  # Batch of referenced tweet objects
			for row in df_rf.itertuples():
				rf_tweet_id = row.id
				rf_author_id = row.author_id
				tweet_to_author[rf_tweet_id] = rf_author_id

with open('../data/reference_records.pkl', 'wb') as fp:
	pickle.dump(rf_records, fp)

with open('../data/tweet_to_author.pkl', 'wb') as fp:
	pickle.dump(tweet_to_author, fp)

user_list = list(set(list(tweet_to_author.values())))
with open('../data/user_list.pkl', 'wb') as fp:
	pickle.dump(user_list, fp)