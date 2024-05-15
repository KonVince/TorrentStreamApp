# stream.py
import streamlit as st
import requests
import libtorrent as lt
import os
import time
from urllib.parse import urlparse

API_URL = 'http://localhost:8000/api/torrents/'

def upload_torrent(torrent_link):
    if not is_valid_magnet_uri(torrent_link):
        st.error("Please enter a valid magnet URI.")
        return

    try:
        response = requests.post(API_URL, data={'torrent_link': torrent_link})
        response.raise_for_status()
        return True, "Torrent uploaded successfully!"
    except requests.exceptions.RequestException as e:
        return False, f"Failed to upload torrent: {e}"

def is_valid_magnet_uri(uri):
    try:
        parsed = urlparse(uri)
        if parsed.scheme != 'magnet':
            return False
        if not parsed.query:
            return False
        params = dict(map(lambda x: x.split('='), parsed.query.split('&')))
        if 'xt' not in params or not params['xt'].startswith('urn:btih:'):
            return False
        return True
    except ValueError:
        return False

def download_torrent(torrent_link):
    if not is_valid_magnet_uri(torrent_link):
        st.error(f"Invalid magnet URI: {torrent_link}")
        return

    ses = lt.session()
    ses.listen_on(6881, 6891)

    params = {
        'save_path': os.path.join(os.getcwd(), 'downloads'),
        'storage_mode': lt.storage_mode_t(2),
    }

    handle = lt.add_magnet_uri(ses, torrent_link, params)

    st.write(f"Downloading metadata from {torrent_link}")
    while not handle.has_metadata():
        time.sleep(1)

    st.write("Starting download...")
    progress_bar = st.progress(0)
    while handle.status().state != lt.torrent_status.seeding:
        progress = handle.status().progress * 100
        progress_bar.progress(int(progress))
        time.sleep(1)

    st.success("Download complete!")

st.set_page_config(page_title="Video Stream Application", page_icon=":movie_camera:")
st.sidebar.title("Navigation")
nav_option = st.sidebar.radio("Go to", ["Home", "Torrent List"])

if nav_option == "Home":
    st.title('Video Stream Application')

    st.subheader('Upload New Torrent')
    torrent_link = st.text_input('Torrent Link')
    if st.button('Upload'):
        if torrent_link:
            success, message = upload_torrent(torrent_link)
            if success:
                st.success(message)
            else:
                st.error(message)
        else:
            st.error('Please enter a torrent link.')

elif nav_option == "Torrent List":
    st.markdown("### Go to [Torrent List](%s)" % st.get_option("browser.serverAddress") + "/torrent_list")