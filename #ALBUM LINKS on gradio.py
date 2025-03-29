#ALBUM LINKS on gradio

import requests
import re
import time
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from ytmusicapi import YTMusic

# ========== CONFIG ==========
SPOTIFY_CLIENT_ID = "c018d665a8804e83860098b3521abe79"
SPOTIFY_CLIENT_SECRET = "ade3af263f0a4d3994113f19ab0e9bfa"
GOOGLE_SHEET_NAME = "Album Links By UPC"
TIDAL_CLIENT_ID = "rVtNwxzekndYwQas"
TIDAL_CLIENT_SECRET = "iqpBJ228SwYwO1znZjml0nP8tqjVjDfBtPKgvgb5cCs="

# ========== GOOGLE SHEETS ==========
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
import json

credentials_content = {
  "type": "service_account",
  "project_id": "metadata-tool-455008",
  "private_key_id": "d3ba1378dd3327edbe2e5e1a9306feaed1c41b4d",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDLZBY7KqFSESxG\ntxnMC0i3EnC0ffq7rmfb8U1wyPuwVZuYZ4l1TMxvIQABD7QkSNVM6uCulLzZoMVt\nHbKhhYCA6NdE0qToZbilfiJqbuwz0K+uC+SG1Ppaqhqhh/lY66IDKrJg7XHf9VMX\nbCoycWK+k02hRC3J/i5VLdfvMFFtyXfFTaXZlFyrLlBnrr4p6gzg76lk489/WD05\nBrkv74D0zXZg9aoa7itCn1izTsLCt5ADbLZYZW4qTVPSuWKlAv2sFZhv8ZgXtKF8\nH1Qd49CeXW7SdxHaD4R9kfAqF+wykoh8J0i1kQY0Fn3D6WKf59FnglB8jFLh1+Gq\n6cgkXxbFAgMBAAECggEACBEuZ8BdthFj55YhmgJxXhmHV0SPHY/IVmS9K2Kjx2KB\nEZihtU5YTKjknoyOtGKGW07bN75C7OemJpkz8zLskUn3wXOqNZfueY0fZ+6B93go\n6Ubwrhkw3BTwVqtu/2p9+l3G+RAFIUEfJftIHS7g7MNcI+MkmDHSiQkqQTY+zizk\nAL8dJNNr8sLjB1GHLZk5Om6KuNJ4ip5UqePOnRZxCVJw37WBa/Xb6ZIcUkL8BYbi\nY6KobooR1vfDFnx+4lyS8P1+Np8tLbRteDbyuO27jMUf5JcGVAuHaf/Ewh0CZlHl\ncM13irGy8jf99UOskG3kgVlDPq3ZUpg+JJSvs8swDQKBgQDqOCTePcJgdgNkMQe9\ns9dHV5/0dfMNaYVuh9KxoESa0dNmmEl5zkI5wkS876S253cpNzc+7slyqIWvuznf\nOtjV1WEJ/3GLbFJuYqb6H+w3IX37+N7s1VE4Or0TcCWSlouC/iJBSAbt7O5MWljO\nhYytfayzTRqgn3IqakWTVC4WXwKBgQDeTgoBHBbtPWC3P4UsPCABWaroYpTWJcVT\nn83P96RO2UN45CbZCTO05CfXMURNymFxAjF7J7uoNIxeH7GQ4bgFm+0vO7awQ3Zf\nKD2zVFUcy+2+CpGdAUBZs47sQlS0emAxaBEWxoulnGk7++jCLvQNq+4tNuZmZwlx\nNUsM1ye9WwKBgCgWffDv3yIFcOUoIywL6O/UBpOf0H7eLbFSW/R8+uEIwscPj5vi\neqFKJ9uypJ2Nlm6efb0uv5n5UBBY2jnj55MJ13cPmo6DdsRf7DZpWlPBTr/ew8ED\nbchS/WOjUTr6u1wrRQ+pVU5JvCujVwnZ/8798J4rt0AAqliqIchqowy/AoGAIuJE\nF6B8yIWVI6xIDYTx0MRtWUH+8QvERzcQaM4HbogRWmsS3YPgJUaYKeCFQ1+6oq0h\nbp3xiJeWXz7B8mY5Jkgtk/fe1xH/BTefVwCoyngFuoiWCPklS+4tQ021VQzPA3G9\nHMHTMA23Rb5l6/LKQUr1eQrgZLlOdgFS4ZTxm3kCgYEAx1q0qpW9/qmRKqbhPMtz\nZMzdODujYVOqyo/16ccgvlVcH4opjl8XZ5kTGeGDS70v3dndINo485eOk2131rZF\nB1ool8+4oBAhJrxjbesChyzaJdT8gnmhq7uV+PjeheyK1lfKDo6jGJN/nGsvU5BE\nNdd0srRVfu1Gu5ocPenFl5w=\n-----END PRIVATE KEY-----\n",
  "client_email": "spotify-sheet-bot@metadata-tool-455008.iam.gserviceaccount.com",
  "client_id": "107215067029056244285",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/spotify-sheet-bot%40metadata-tool-455008.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_content, scope)
client = gspread.authorize(creds)
sheet = client.open(GOOGLE_SHEET_NAME).sheet1

# Lấy danh sách UPC từ cột A
upc_list = sheet.col_values(1)[1:]  # bỏ dòng tiêu đề
print("Danh sách UPC để kiểm tra:")
for upc in upc_list:
    print(upc)

# ========== SPOTIFY ==========
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# ========== YOUTUBE MUSIC ==========
yt = YTMusic()

# ========== TIDAL ACCESS TOKEN ==========
def get_tidal_access_token():
    url = "https://auth.tidal.com/v1/oauth2/token"
    data = {
        "client_id": TIDAL_CLIENT_ID,
        "client_secret": TIDAL_CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "r_basicprofile"  # Không cần r_search cho /searchresults/{id}/relationships/albums
    }
    try:
        res = requests.post(url, data=data, timeout=10)
        if res.status_code != 200:
            print(f"Error getting Tidal access token: HTTP {res.status_code}, Response: {res.text}")
            raise Exception(f"HTTP {res.status_code}: {res.text}")
        result = res.json()
        access_token = result.get("access_token")
        if not access_token:
            raise Exception("No access token in response")
        return access_token
    except Exception as e:
        print(f"Error getting Tidal access token: {str(e)}")
        return None

# Lấy access token khi khởi động script
TIDAL_ACCESS_TOKEN = get_tidal_access_token()
if not TIDAL_ACCESS_TOKEN:
    print("Failed to get Tidal access token. Tidal search will use Google fallback.")
else:
    print(f"Tidal access token obtained: {TIDAL_ACCESS_TOKEN}")

# ========== HELPER FUNCTIONS ==========
def clean_query(text):
    return re.sub(r'[^\w\s]', '', text).strip()

def is_error_cell(value):
    val = value.strip().lower()
    return val == "" or val == "not found" or val.startswith("error")

def is_valid_album_link(link, domain):
    patterns = {
        "music.amazon.com": r"music\\.amazon\\.com\\/albums\\/",
        "tidal.com": r"tidal\\.com\\/(browse\\/)?album\\/",
        "boomplay.com": r"boomplay\\.com\\/albums\\/",
        "anghami.com": r"(play\\.|open\\.)?anghami\\.com\\/(album|song)\\/",
        "melon.com": r"melon\\.com\\/album\/detail\\.htm\\?albumId=",
        "zingmp3.vn": r"zingmp3\\.vn\\/album\/"
    }
    if domain not in patterns:
        return domain in link
    return re.search(patterns[domain], link) is not None

# ========== TIDAL API FUNCTIONS ==========
def get_tidal_search_result_id(album_name, artist):
    """Tạo search result ID từ album_name và artist"""
    # Nối album_name và artist, loại bỏ ký tự đặc biệt
    search_id = f"{clean_query(album_name)} {clean_query(artist)}"
    return search_id

def search_tidal_by_searchresult_id(search_result_id, country_code="US"):
    """Gọi /searchresults/{id}/relationships/albums để lấy danh sách ID album"""
    if not TIDAL_ACCESS_TOKEN:
        print("Tidal API failed. Using Google fallback for Tidal.")
        return None
    
    headers = {
        "Authorization": f"Bearer {TIDAL_ACCESS_TOKEN}",
        "User-Agent": "Mozilla/5.0"
    }
    # Thêm /relationships/albums vào endpoint
    url = f"https://openapi.tidal.com/v2/searchresults/{requests.utils.quote(search_result_id)}/relationships/albums?countryCode={country_code}&include=albums"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            print(f"Tidal search error (searchresults): HTTP {res.status_code}, Response: {res.text}")
            return None
        result = res.json()
        if "data" in result:
            albums = result["data"]
            return [album["id"] for album in albums if album["type"] == "albums"]
        return None
    except Exception as e:
        print(f"Tidal search error (searchresults): {str(e)}")
        return None

def search_tidal(album_name, artist):
    """Tìm kiếm album trên Tidal bằng /searchresults/{id}/relationships/albums"""
    # Bước 1: Tạo search result ID từ album_name và artist
    search_result_id = get_tidal_search_result_id(album_name, artist)
    if not search_result_id:
        print("Could not create Tidal search result ID. Using Google fallback for Tidal.")
        q = f'"{album_name}" "{artist}"'
        return search_google_fallback(q, "tidal.com")

    # Bước 2: Gọi /searchresults/{id}/relationships/albums để lấy danh sách ID album
    album_ids = search_tidal_by_searchresult_id(search_result_id)
    if not album_ids:
        print("No album IDs found in search results. Using Google fallback for Tidal.")
        q = f'"{album_name}" "{artist}"'
        return search_google_fallback(q, "tidal.com")

    # Bước 3: Tạo URL album từ ID album đầu tiên
    album_id = album_ids[0]  # Lấy ID album đầu tiên
    album_url = f"https://listen.tidal.com/album/{album_id}"
    return album_url

# ========== API SEARCH FUNCTIONS ==========
def search_youtube_music(album_name, artist):
    try:
        results = yt.search(query=f"{album_name} {artist}", filter="albums")
        link = f"https://music.youtube.com/browse/{results[0]['browseId']}" if results else "Not found"
        return link
    except:
        return "Error"

def search_apple_music(album_name, artist):
    try:
        r = requests.get(f"https://itunes.apple.com/search?term={requests.utils.quote(album_name + ' ' + artist)}&entity=album&limit=1")
        result = r.json()
        link = result['results'][0]['collectionViewUrl'] if result['resultCount'] else "Not found"
        return link
    except:
        return "Error"

def search_deezer(album_name, artist):
    try:
        r = requests.get(f"https://api.deezer.com/search/album?q=album:\"{album_name}\" artist:\"{artist}\"")
        result = r.json()
        link = result['data'][0]['link'] if result['data'] else "Not found"
        return link
    except:
        return "Error"

def search_boomplay(album_name, artist):
    headers = {"User-Agent": "Mozilla/5.0"}
    query = f"{album_name} {artist}"
    url = f"https://www.boomplay.com/search/album/{requests.utils.quote(query)}"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        link = soup.find('a', href=re.compile(r'/albums/\d+'))
        return f"https://www.boomplay.com{link['href']}" if link else "Not found"
    except Exception as e:
        return f"Error: {str(e)}"

def search_google_fallback(query, domain):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(f"https://www.google.com/search?q={query}+site:{domain}", headers=headers, timeout=10)
        links = re.findall(r"https://[\w./%-]+", res.text)
        for link in links:
            if domain in link:
                return link
    except:
        return "Error"
    return "Not found"

# ========== MAIN ==========
def main():
    data = sheet.get_all_values()
    header = data[0]
    rows = data[1:]

    for idx, row in enumerate(rows):
        upc = row[0]
        album_name = row[1] if len(row) > 1 else ""
        artist = row[2] if len(row) > 2 else ""

        if not album_name or not artist:
            try:
                result = sp.search(q=f"upc:{upc}", type="album")
                album_info = result['albums']['items'][0] if result['albums']['items'] else None
                if album_info:
                    album_name = album_info['name']
                    artist = album_info['artists'][0]['name']
                    sheet.update_cell(idx + 2, 2, album_name)
                    sheet.update_cell(idx + 2, 3, artist)
                    spotify_link = album_info['external_urls']['spotify']
                    sheet.update_cell(idx + 2, 4, spotify_link)
                    print(f"→ Updated: {album_name} - {artist}")
            except:
                continue
        else:
            try:
                result = sp.search(q=f"album:{album_name} artist:{artist}", type="album")
                album_info = result['albums']['items'][0] if result['albums']['items'] else None
                if album_info:
                    spotify_link = album_info['external_urls']['spotify']
                    sheet.update_cell(idx + 2, 4, spotify_link)
                    print(f"→ Spotify: {spotify_link}")
            except:
                pass

        # Apple Music (E)
        if len(row) < 5 or is_error_cell(row[4]):
            link = search_apple_music(album_name, artist)
            sheet.update_cell(idx + 2, 5, link)
            print("→ Apple Music:", link)

        # YouTube Music (F)
        if len(row) < 6 or is_error_cell(row[5]):
            link = search_youtube_music(album_name, artist)
            sheet.update_cell(idx + 2, 6, link)
            print("→ YouTube Music:", link)

        # Amazon Music (G)
        if len(row) < 7 or is_error_cell(row[6]):
            q = f'"{album_name}" "{artist}"'
            link = search_google_fallback(q, "music.amazon.com")
            sheet.update_cell(idx + 2, 7, link)
            print("→ Amazon Music:", link)

        # Deezer (H)
        if len(row) < 8 or is_error_cell(row[7]):
            link = search_deezer(album_name, artist)
            sheet.update_cell(idx + 2, 8, link)
            print("→ Deezer:", link)

        # Tidal (I)
        if len(row) < 9 or is_error_cell(row[8]):
            link = search_tidal(album_name, artist)
            sheet.update_cell(idx + 2, 9, link)
            print("→ Tidal:", link)

        # Boomplay (J)
        if len(row) < 10 or is_error_cell(row[9]):
            link = search_boomplay(album_name, artist)
            sheet.update_cell(idx + 2, 10, link)
            print("→ Boomplay:", link)

        # Anghami (K)
        if len(row) < 11 or is_error_cell(row[10]):
            q = f'"{album_name}" "{artist}"'
            link = search_google_fallback(q, "anghami.com")
            sheet.update_cell(idx + 2, 11, link)
            print("→ Anghami:", link)

        # Melon (L)
        if len(row) < 12 or is_error_cell(row[11]):
            q = f'"{album_name}" "{artist}"'
            link = search_google_fallback(q, "melon.com")
            sheet.update_cell(idx + 2, 12, link)
            print("→ Melon:", link)

        # Zing MP3 (M)
        if len(row) < 13 or is_error_cell(row[12]):
            q = f'"{album_name}" "{artist}"'
            link = search_google_fallback(q, "zingmp3.vn")
            sheet.update_cell(idx + 2, 13, link)
            print("→ Zing MP3:", link)

        time.sleep(3)

import gradio as gr

def run_app():
    try:
        return main()
    except Exception as e:
        return f"❌ Có lỗi: {str(e)}"

gr.Interface(
    fn=main,
    inputs=[],
    outputs="text",
    title="🎧 Album Link Fetcher",
    description="Quét tất cả dòng trong Google Sheet để cập nhật link album."
).launch()

