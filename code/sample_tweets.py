import pickle
import numpy as np
import pandas as pd
import random
import graph_tool.all as gt

random.seed(0)
np.random.seed(10)
np.set_printoptions(suppress=True)

with open('../data/user_list.pkl', 'rb') as fp:
	user_list = pickle.load(fp)
with open('../data/parts_before_leiden.pkl', 'rb') as fp:
	parts_dict = pickle.load(fp)

main_users = set()
blue_users = set()
red_users = set()
for u in parts_dict:
	if parts_dict[u] == 0:
		main_users.add(u)
	elif parts_dict[u] == 1:
		blue_users.add(u)
	else:
		red_users.add(u)

"""
Count retweets and active users
"""
with open('../data/reference_records.pkl', 'rb') as fp:
	records = pickle.load(fp)
with open('../data/tweet_to_author.pkl', 'rb') as fp:
	tweet_to_author = pickle.load(fp)

periods = ['before', 'during', 'after', 'longafter']
date_range = [d.strftime('%Y-%m-%d') for d in pd.date_range('2021-10-01', '2022-03-31')]
start_idxs = [146 - 14, 146, 153, 174]
end_idxs = [146, 146 + 7, 153 + 7, 174 + 7]

sampled_tweets = {'before':{'main':[], 'blue':[], 'red':[]}, 'during':{'main':[], 'blue':[], 'red':[]}, 'after':{'main':[], 'blue':[], 'red':[]}, 'longafter':{'main':[], 'blue':[], 'red':[]}}

for period, start_idx, end_idx in zip(periods, start_idxs, end_idxs):
	rt_cnt_main = {}
	rt_cnt_blue = {}
	rt_cnt_red = {}
	cnt_blue_blue = 0
	cnt_blue_main = 0
	cnt_red_red = 0
	cnt_red_main = 0
	blue_active = set()
	red_active = set()
	main_active = set()
	for d in range(start_idx, end_idx):
		for (tweet_id, orig_tweet_id, rt_type) in records[date_range[d]]:
			if rt_type == 'retweeted':
				if int(tweet_to_author[tweet_id]) in main_users:
					main_active.add(int(tweet_to_author[tweet_id]))
					if orig_tweet_id not in rt_cnt_main:
						rt_cnt_main[orig_tweet_id] = 0
					rt_cnt_main[orig_tweet_id] += 1

				if int(tweet_to_author[tweet_id]) in blue_users:
					blue_active.add(int(tweet_to_author[tweet_id]))
					if int(tweet_to_author[orig_tweet_id]) in blue_users:
						cnt_blue_blue += 1
					if int(tweet_to_author[orig_tweet_id]) in main_users:
						cnt_blue_main += 1
					if orig_tweet_id not in rt_cnt_blue:
						rt_cnt_blue[orig_tweet_id] = 0
					rt_cnt_blue[orig_tweet_id] += 1

				if int(tweet_to_author[tweet_id]) in red_users:
					red_active.add(int(tweet_to_author[tweet_id]))
					if int(tweet_to_author[orig_tweet_id]) in red_users:
						cnt_red_red += 1
					if int(tweet_to_author[orig_tweet_id]) in main_users:
						cnt_red_main += 1
					if orig_tweet_id not in rt_cnt_red:
						rt_cnt_red[orig_tweet_id] = 0
					rt_cnt_red[orig_tweet_id] += 1

				orig_author = int(tweet_to_author[orig_tweet_id])
				if orig_author in main_users:
					main_active.add(orig_author)
				if orig_author in red_users:
					red_active.add(orig_author)
				if orig_author in blue_users:
					blue_active.add(orig_author)

	print('Active users in period %s: main-%.4f, red-%.4f, blue-%.4f' % (period, len(main_active) / len(main_users), len(red_active) / len(red_users), len(blue_active) / len(blue_users)))

	"""
	Sample tweets by number of retweets
	"""
	sample_size = 42
	tweets_main = list(rt_cnt_main.keys())
	rts_main = np.array(list(rt_cnt_main.values()))
	samples_main = np.random.choice(tweets_main, size=sample_size, replace=False, p=rts_main/sum(rts_main))
	sampled_tweets[period]['main'] = samples_main

	for tweet in samples_main:
		print('https://twitter.com/yanxxia/status/%s, %d retweets by the main bubble' % (tweet, rt_cnt_main[tweet]))

	tweets_blue = list(rt_cnt_blue.keys())
	rts_blue = np.array(list(rt_cnt_blue.values()))
	samples_blue = np.random.choice(tweets_blue, size=sample_size, replace=False, p=rts_blue/sum(rts_blue))
	sampled_tweets[period]['blue'] = samples_blue

	for tweet in samples_blue:
		print('https://twitter.com/yanxxia/status/%s, %d retweets by the blue bubble' % (tweet, rt_cnt_blue[tweet]))

	tweets_red = list(rt_cnt_red.keys())
	rts_red = np.array(list(rt_cnt_red.values()))
	samples_red = np.random.choice(tweets_red, size=sample_size, replace=False, p=rts_red/sum(rts_red))
	sampled_tweets[period]['red'] = samples_red

	for tweet in samples_red:
		print('https://twitter.com/yanxxia/status/%s, %d retweets by the red bubble' % (tweet, rt_cnt_red[tweet]))

with open('../data/sampled_tweets.pkl', 'wb') as fp:
	pickle.dump(sampled_tweets, fp)