import streamlit as st
import requests
import libtorrent as lt
import os
import time
from urllib.parse import urlparse
import sys

API_URL = 'http://localhost:8000/api/torrents/'

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
    progress_bar = st.progress(0)
    while not handle.has_metadata():
        time.sleep(1)

    st.write("Starting download...")
    while handle.status().state != lt.torrent_status.seeding:
        progress = handle.status().progress * 100
        progress_bar.progress(int(progress))
        sys.stdout.write("\r%d%% downloaded" % int(progress))
        sys.stdout.flush()
        time.sleep(1)

    st.success("Download complete!")

    # Simpan link torrent ke dalam daftar torrent
    try:
        response = requests.post(API_URL, data={'torrent_link': torrent_link})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to save torrent link: {e}")

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

def delete_torrent(torrent_id):
    try:
        response = requests.delete(f"{API_URL}{torrent_id}/")
        response.raise_for_status()
        return True, "Torrent deleted successfully!"
    except requests.exceptions.RequestException as e:
        return False, f"Failed to delete torrent: {e}"

def stream_page():
    st.title('Video Stream Application')

    st.subheader('Download Torrent')
    torrent_link = st.text_input('Torrent Link to Download')
    if st.button('Download'):
        if torrent_link:
            download_torrent(torrent_link)
        else:
            st.error('Please enter a torrent link to download.')

def torrent_list_page():
    st.title("Torrent List")

    def get_torrents():
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch data: {e}")
        return []

    torrents = get_torrents()

    if torrents:
        for torrent in torrents:
            with st.expander(f"Torrent {torrent['id']}"):
                st.write(f"Link: {torrent['torrent_link']}")
                st.write(f"Created At: {torrent['created_at']}")
                if st.button(f"Delete Torrent {torrent['id']}", key=f"delete_{torrent['id']}"):
                    success, message = delete_torrent(torrent['id'])
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
    else:
        st.warning("No torrents found.")

def main():
    st.set_page_config(page_title="Video Stream Application", page_icon=":movie_camera:")
    pages = {
        "Stream": stream_page,
        "Torrent List": torrent_list_page
    }

    selection = st.sidebar.radio("Go to", list(pages.keys()))

    pages[selection]()

if __name__ == "__main__":
    main()