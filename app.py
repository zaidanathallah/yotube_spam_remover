import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json, os
from judol_patterns import is_judol_comment

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

st.title("YouTube Judol Comment Remover")

# Upload credentials
credentials_file = st.file_uploader("Upload credentials.json", type="json")
if credentials_file:
    with open("credentials.json", "wb") as f:
        f.write(credentials_file.read())
    st.success("File kredensial berhasil di-upload!")

# Generate token
if os.path.exists("credentials.json"):
    if st.button("Authorize via Google"):
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_console()  # GANTI INI
        with open("token.json", "w") as token:
            token.write(creds.to_json())
        st.success("Token berhasil dibuat!")

# Cek token
if os.path.exists("token.json"):
    with open("token.json") as token_file:
        creds_data = json.load(token_file)
        creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
        st.success("Token aktif.")

    video_id = st.text_input("Masukkan ID Video YouTube")

    if st.button("Deteksi dan Hapus Komentar Judol"):
        youtube = build('youtube', 'v3', credentials=creds)

        # Ambil komentar
        comments_deleted = 0
        nextPageToken = None
        while True:
            response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=20000,
                pageToken=nextPageToken
            ).execute()

            for item in response.get("items", []):
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comment_id = item["snippet"]["topLevelComment"]["id"]
                if is_judol_comment(comment):
                    youtube.comments().setModerationStatus(
                        id=comment_id,
                        moderationStatus="rejected"
                    ).execute()
                    comments_deleted += 1

            nextPageToken = response.get("nextPageToken")
            if not nextPageToken:
                break

        st.success(f"Jumlah komentar judol yang dihapus: {comments_deleted}")
