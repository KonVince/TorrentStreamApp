# torrent_list.py
import streamlit as st
import requests

API_URL = 'http://localhost:8000/api/torrents/'

def get_torrents():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch data: {e}")
    return []

def main():
    st.set_page_config(page_title="Torrent List", page_icon=":movie_camera:")
    st.title("Torrent List")

    torrents = get_torrents()

    if torrents:
        for torrent in torrents:
            with st.expander(f"Torrent {torrent['id']}"):
                st.write(f"Link: {torrent['torrent_link']}")
                st.write(f"Created At: {torrent['created_at']}")
    else:
        st.warning("No torrents found.")

if __name__ == "__main__":
    main()