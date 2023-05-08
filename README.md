# finnish-nato
Data and code for the paper [The Russian invasion of Ukraine selectively depolarized the Finnish NATO discussion](https://arxiv.org/abs/2212.07861).

### Data
- Tweets: Due to Twitter's policy on data publication, we can only share the IDs of the tweets we used for the analysis, which are stored in the text file `tweets/finnish_nato_tweet_ids.txt`, with one tweet ID per line. They need to be rehydrated for replicating the analysis.
- Retweet networks: Anonymized retweet networks for each period are stored as `.xml` files under the `networks` directory.

### Code
- `code/parse_tweets.py`: Parses tweet data to create formatted data for subsequent analysis. (Note that the code might need to be tweaked for parsing rehydrated tweet data.)
- `code/cls_rt_network.py`: Partitions the retweet network in the _before_ period and assigns a cluster for each user in the _before_ network.
- `code/vis_rt_network.py`: Plots the retweet networks.
- `code/network_stats.py`: Analyzes the statistics of retweet networks, including the number of nodes (i.e., users) from each cluster that are active in each period, and the weight sum of edges (i.e., the number of retweets) that go between each pair of clusters in each period.
- `code/sample_tweets.py`: Samples tweets from each period from each cluster, with the sampling probability set proportional to its number of in-cluster retweets in the period.

### Replication Instructions
- Install `Python 3.7.6` and Python libraries `numpy`, `pandas`, `graph-tool`, `igraph`, and `leidenalg`.
- Rehydrate tweet data using tweet IDs.
- Run `code/parse_tweets.py` to parse the tweet data.
- Run `code/cls_rt_network.py` to obtain user clusters.
- Run `code/vis_rt_network.py` to visualize the retweet networks, or `code/network_stats.py` to obtain the statistics of retweet networks, or `code/sample_tweets.py` to sample tweets for manual reading.
