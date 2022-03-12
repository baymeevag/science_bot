from utils.auth import oauth
from utils.config import TOPIC
from generators.Markov import Markov

if __name__ == "__main__":
    api = oauth()

    follower_ids = api.get_follower_ids()
    for fid in follower_ids:
        try:
            api.create_friendship(user_id=fid)
        except:
            continue
