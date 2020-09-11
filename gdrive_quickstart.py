"""
Edited on Mon September 7 11:50:33 2020

@author: sklucioni

Google Drive API setup.
"""
from __future__ import print_function
import pickle
import os.path, io
import general_utilities
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload

# Google Drive API Docs: https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/index%2Ehtml

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate_drive_api():
    """
    Builds the drive api service and stores it in DRIVE.
    :return the drive api service.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    DRIVE = build('drive', 'v3', credentials=creds)
    return DRIVE


def get_file_objs_list(DRIVE, query):
    '''
    Use the drive api service to get a list of files according to the `query`
    string.
    :param DRIVE: the drive api service.
    :param query: string, A query for filtering the file results. See
    https://developers.google.com/drive/api/v3/search-files for supported
    syntax.

    :return A list of file objects.
    '''
    results = DRIVE.files().list(q=query).execute()
    items = results.get('files', [])
    return items


def download_file(DRIVE, file_obj, print_status=True):
    '''
    Use the drive api service to download a file from your personal gdrive. Does
    NOT remove the locally downloaded file. Prints a status report of the
    print_statusdownload (if `print_status == True`).
    :param DRIVE: the drive api service.
    :param file_obj: a file object, must have keys `id` and `name`.
    :param print_status: bool, Whether or not to print the file download status.

    :return None.
    '''
    if 'id' not in file_obj or 'name' not in file_obj:
        print('`file_obj` needs `id` and `name`.')
        return None

    request = DRIVE.files().get_media(fileId=file_obj['id'])
    fh = io.FileIO(file_obj['name'], mode='w')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        if print_status: print("Download %d%%." % int(status.progress() * 100))

    return None


def download_pkl_file(DRIVE, file_obj, print_status=True):
    '''
    Use the drive api service to download and return the data from a pkl file
    from your personal gdrive. Removes the locally downloaded file. Prints a
    status report of the download (if `print_status == True`).
    :param DRIVE: the drive api service.
    :param file_obj: a file object, must have keys `id` and `name`.
    :param print_status: bool, Whether or not to print the file download status.

    :return pkl_data: the pkl data, most likely a list of `thinned_tweet_obj`s.
    '''
    download_file(DRIVE, file_obj, print_status)
    pkl_data = general_utilities.read_pkl(file_obj['name'])
    os.remove(file_obj['name'])
    return pkl_data


'''
Base code to download all combined_tweets-2020 files, grab pkl data, remove files

DRIVE = authenticate_drive_api()
file_objs_lst = get_file_objs_list('name contains "combined_tweets-2020"')
for file_obj in file_objs_lst:
    thinned_obj_tweets = download_pkl_file(DRIVE, file_obj, print_status=True):
    # Do something with the `thinned_obj_tweets` or store them to use later
'''
