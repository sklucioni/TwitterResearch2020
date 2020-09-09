**Memo lucioni-200907.md**

This memo corresponds with `gdrive_quickstart.py`.

# Google Drive API Quickstart

We can use the Google Drive API to easily download and read our data files. The code to authenticate the gdrive should be pretty similar between people, so I wanted to create a tool for it. I noticed that `gdrive_quickstart.py` already existed, but it was a little out of date. Therefore, I updated the file for our current use.

At the bottom of the file, I also added a comment with some helper code for downloading the `combined_tweets-2020` pkl files (these are our main data files of thineed tweet objects). We can probably turn this into a tool within this file, but I'm hesitant because the user should probably do what they want with the data within this download portion so that we don't store massive amounts of data.

## Individual GDrive API Setup

In order to access the gdrive API, you need to set up an API credentials through the [Google Developers Console](https://console.developers.google.com/apis/credentials). I followed [this tutorial](https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/index%2Ehtml). Once you set up the credentials, download the client secrets and rename the file to be `credentials.json` (the `authenticate_drive_api` function assumes your credentials are stored as such).

Now, when you want to use the gdrive API, first import the `gdrive_quickstart.py`, then call the `authenticate_drive_api()` method and save the returned value as `DRIVE` (or something that lets you know that it stores the gdrive service). For example:

```python
import gdrive_quickstart
DRIVE = gdrive_quickstart.authenticate_drive_api()
```

To understand the functionality available with the `DRIVE` service, take a look at the gdrive API [guides](https://developers.google.com/drive/api/v3/quickstart/python). A common functionality that we will re-use is getting a list of file objects (including filename and file id). Therefore, I wrote the `get_file_objs_list(query, DRIVE)` function to get this list of files based on a `query` string and the stored `DRIVE` service. The `query` string can take on a variety of forms. Visit [these docs](https://developers.google.com/drive/api/v3/search-files) to learn more about the supported syntax.

Putting the above two functions together and showing a common use case, we can now download all the `combined_tweets-2020` pkl files, grab their data, and remove the locally downloaded copies:

```python
import gdrive_quickstart

DRIVE = gdrive_quickstart.authenticate_drive_api()
file_objs_lst = gdrive_quickstart.get_file_objs_list('name contains "combined_tweets-2020"')
for file_obj in file_objs_lst:
    thinned_obj_tweets = gdrive_quickstart.download_pkl_file(DRIVE, file_obj, print_status=True):
    # Do something with the `thinned_obj_tweets` or store them to use later
```

On my machine and my WiFi, it takes ~ 2 minutes to download one pkl file.

# Random Other Notes

- I found that `.__dict__` prints out the contents of an object as a dictionary representation. This is super helpful when looking at the list of thinned objects (`thinned_obj.__dict__` lets us look at the tweet).
- I've been thinking a lot about the statistical analysis, and I've come up with two "solid" methods to compare the statistical similarity of our data. I'm planning on writing a memo about what I've referenced, what I've thought about, and what I've come up with for the statistical analysis later this week. I'm also going to transfer the statistical analysis tools from my ipynb to py tools so that others can use them.
- To work with `.py` tools within an ipynb (e.g. `module.py`):
  - Import the module: `import module`
  - Use the module's functions: `module.function()`
