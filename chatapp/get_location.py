import requests
import math
import dotenv
import os
import json


dotenv.load_dotenv()
prefecture_code_list = json.load(open('prefecture_code_list.json', 'r', encoding='utf-8'))


MAP_API_KEY = os.getenv('MAP_API_KEY')

def lat_lon_to_tile_coords(zoom, lat, lon):
    # 緯度をラジアンに変換
    lat_rad = math.radians(lat)
    
    # タイルの数を計算（2のズームレベル乗）
    n = 2.0 ** zoom
    
    # x座標を計算
    x_tile = int((lon + 180.0) / 360.0 * n)
    
    # y座標を計算
    y_tile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    
    return zoom, x_tile, y_tile

def get_lat_lon(address):
    url = f"https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': address,
        'key': MAP_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            location = results[0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            print("住所が見つかりませんでした。")
            return None
    else:
        print(f"エラーが発生しました: {response.status_code}")
        return None

def tile_to_latlon(zoom, tileX, tileY):
    # タイルの中心を取得するために x, y に 0.5 を足す
    tileX += 0.5
    tileY += 0.5
    
    # 経度の計算
    lon = tileX / (2**zoom) * 360.0 - 180.0
    
    # 緯度の計算
    n = math.pi - 2.0 * math.pi * tileY / (2**zoom)
    lat = math.degrees(math.atan(math.sinh(n)))
    
    return lat, lon


def get_key():
    return MAP_API_KEY
