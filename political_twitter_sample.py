import tweepy
import json
import time
from datetime import date
import os, sys, pickle
import threading
import traceback
import thinned_tweet_obj as tt
import general_utilities as gt

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
    global write_dir

    while True:
        if len(tweets) >= 10000 or done_sampling:

            # make output file string
            datestr = time.strftime("%Y_%m_%d")
            datestr = '/'.join([write_dir, datestr])
            if not os.path.isdir(datestr):
                os.mkdir(datestr)
            timestr = time.strftime("%Y_%m_%d-%H_%M_%S")
            outstr = write_dir + "/" + datestr + "/" + 'political_' + timestr + ".pkl"

            with open(outstr, 'wb') as f:
                # write tweets to file
                write_lock.acquire()
                total_tweets += len(tweets)
                gt.write_pkl(outstr, tweets)
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
        print('Entered stream listener')
        # handle incoming tweet
        global tweets
        global write_lock
        write_lock.acquire()
        print ('Write lock acquired')
        tweets.append(tt.tweet(status._json))
        print ('Appended tweet')
        write_lock.release()

class MyListener(StreamListener):

    def __init__(self, out_directory, out_fname):
        super().__init__()
        self.count = 1
        self.cur_list = []
        self.directory = out_directory
        self.fname = out_fname
        self.date = date.today()
        self.outname = os.path.sep.join([out_directory, out_fname])
        self.outname = self.outname + str(self.date) + '.pkl'
        try:
            self.outfile = open(self.outname, 'a')
            self.outfile.close()
        except BaseException as e:
            print(self.outname)
            print('error on file open'+ str(e))
            exit(1)

    def on_data(self, t_data):
        try:
            self.cur_list.append(tt.tweet(t_data))
            if self.count < 1000:
                self.count += 1
            else:
                self.count = 1
                if self.check_new_date():
                    self.use_file()
                self.write_file()
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

    def write_file(self):
        out_f = open(self.use_file(), 'rb')
        cur_list = pickle.load(out_f)
        out_f.close()
        write_list = cur_list + self.cur_list
        out_f = open(self.use_file(), 'wb')
        pickle.dump(out_f, write_list)
        out_f.close()
        return

    def use_file(self):
        self.outfile.close()
        if self.date != date.today():
            self.date = date.today()
        self.outname = os.path.sep.join([self.directory, self.fname])
        self.outname = self.outname + str(self.date) + '.json'
        try:
            self.outfile = open(self.outname, 'a')
        except BaseException as e:
            print('error opening new file')
            exit(1)

    def check_new_date(self):
        if self.date != date.today():
            return True
        else:
            return False

def load_credentials(cred_fname):
    # load credentials
    with open(cred_fname, 'rb') as f:
        credentials = json.load(f)
    return credentials

def initialize_api(creds):
    # initialize the api
    auth = tweepy.OAuthHandler(creds['consumer_key'], creds['consumer_secret'])
    auth.set_access_token(creds['access_token'], creds['access_secret'])
    api = tweepy.API(auth)
    return api

def get_political_user_ids(keys_file):
    with open(keys_file, 'r') as f:
        political_user_ids = json.load(f)
    return map(str, political_user_ids)

def main():
    global done_sampling
    global start_time
    global write_dir

    #load configuration file
    config_in = open(sys.argv[1], 'r')
    config_d = json.load(config_in)
    config_in.close()

    # load credentials and api
    start_time = time.strftime("%Y_%m_%d-%H_%M_%S")
    if 'credentials' in config_d:
        credentials = load_credentials(config_d['credentials'])
    else:
        print('No credentials file specified in configuration')
        sys.exit(1)
    api = initialize_api(credentials)
    political_user_ids = get_political_user_ids(config_d['filter_by'])
    if 'data_dir' in config_d:
        write_dir = config_d['data_dir']
    else:
        write_dir = '.'

    done_sampling = False

    # create listener and writer
    writer_thread = threading.Thread(target=stream_writer)
    writer_thread.start()

    streamListener = MyListener(write_dir, 'test_output.pkl')
    stream = tweepy.Stream(auth = api.auth, listener=streamListener)

    try:
        # get filtered tweets by user id (blocking)
        stream.filter(follow=political_user_ids)
    except KeyboardInterrupt:
        print("Quitting due to keyboard interrupt")
        exit()
    except Exception as e:
        print("Error occurred")
        print(e)
        traceback.print_exc()
        stream.disconnect()

if __name__ == "__main__":
    main()
