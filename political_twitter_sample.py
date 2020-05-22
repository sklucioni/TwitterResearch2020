import tweepy
import json
import time
import os
import threading
import traceback

tweets = []
total_tweets = 0
start_time = ""
done_sampling = False
write_lock = threading.Lock()

def stream_writer():
    global tweets
    global done_sampling
    global total_tweets
    global start_time
    global write_lock

    while True:
        if len(tweets) >= 10000 or done_sampling:

            # make output file string
            datestr = time.strftime("%Y_%m_%d")
            if not os.path.isdir(datestr):
                os.mkdir(datestr)
            timestr = time.strftime("%Y_%m_%d-%H_%M_%S")
            outstr = datestr + "/" + 'political_' + timestr + ".json"

            with open(outstr, 'w') as f:
                # write tweets to file
                write_lock.acquire()
                total_tweets += len(tweets)
                json.dump(tweets, f)
                print("wrote " + timestr + " to file with " + str(len(tweets)) + " tweets.")
                print(str(total_tweets) + " total tweets downloaded since " + start_time + ".")
                tweets = []
                write_lock.release()

            if done_sampling:
                return
        else:
            time.sleep(1)

#override tweepy.StreamListener to add logic to on_status
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # handle incoming tweet
        global tweets
        global write_lock
        write_lock.acquire()
        tweets.append(status._json)
        write_lock.release()

def load_credentials():
    # load credentials
    with open(os.path.join(os.getcwd(), '..', 'credentials.json'), 'rb') as f:
        credentials = json.load(f)
    return credentials

def initialize_api(creds):
    # initialize the api
    auth = tweepy.OAuthHandler(creds['consumer_key'], creds['consumer_secret'])
    auth.set_access_token(creds['access_token'], creds['access_token_secret'])
    api = tweepy.API(auth)
    return api

def get_political_user_ids():
    with open('political_user_ids.json', 'r') as f:
        political_user_ids = json.load(f)
    return map(str, political_user_ids)

def main():
    global done_sampling
    global start_time

    # load credentials and api
    start_time = time.strftime("%Y_%m_%d-%H_%M_%S")
    credentials = load_credentials()
    api = initialize_api(credentials)
    political_user_ids = get_political_user_ids()

    # create listener and writer
    streamListener = StreamListener()
    stream = tweepy.Stream(auth = api.auth, listener=streamListener)
    writer_thread = threading.Thread(target=stream_writer)
    writer_thread.start()

    while True:
        try:
            # get filtered tweets by user id (blocking)
            stream.filter(follow=political_user_ids)
        except KeyboardInterrupt:
            print("Quitting due to keyboard interrupt")
            # cause writer to write out to file, and wait for it to finish
            done_sampling = True
            writer_thread.join()
            exit()
        except Exception as e:
            print("Error occurred")
            print(e)
            traceback.print_exc()

if __name__ == "__main__":
    main()
