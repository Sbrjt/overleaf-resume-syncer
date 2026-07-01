from __future__ import annotations

import json
import os
import re
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Retrieve environment variables
gdrive_link = os.environ.get("GDRIVE_LINK")
sa_key = os.environ.get("GDRIVE_SERVICE_ACCOUNT_KEY")


if not gdrive_link or not sa_key:
    raise ValueError("GDRIVE_LINK or GDRIVE_SERVICE_ACCOUNT_KEY is missing.")

sa_info = json.loads(sa_key)

credentials = service_account.Credentials.from_service_account_info(
    sa_info,
    scopes=['https://www.googleapis.com/auth/drive'],
)

drive = build('drive', 'v3', credentials=credentials)


def findId(link: str):
    match = re.search(r"/file/d/([^/]+)", link)

    if not match:
        raise ValueError("Invalid Google Drive shared URL\nExpected format: https://drive.google.com/file/d/<FILE_ID>/view")

    return match.group(1)


def updateFile(id: str, file: str):
    new_file = (
        drive.files()
        .update(
            fileId=id,
            media_body=MediaFileUpload(
                file,
                mimetype="application/pdf",
            ),
        )
        .execute()
    )
    return new_file


file_id = findId(gdrive_link)

try:
    new_file = updateFile(file_id, 'resume.pdf')
    print("Upload to google drive successful 🎉")
    # print(new_file)
except Exception as e:
    raise RuntimeError(f"Failed to upload :(") from e
