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

def get_lat_lon(address, api_key):
    url = f"https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': address,
        'key': api_key
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

if __name__ == "__main__":
    api_key = MAP_API_KEY
    prefecture = '東京都'
    address = '江東区豊洲'
    prefecture_code = prefecture_code_list[prefecture]
    coordinates = get_lat_lon(prefecture + address, api_key)
    if coordinates:
        lat = coordinates[0]
        lon = coordinates[1]
        print(f"緯度: {lat}, 経度: {lon}")

        z, x, y = lat_lon_to_tile_coords(17, lat, lon)
        print(f"https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png")
        print(f"https://disaportaldata.gsi.go.jp/raster/01_flood_l2_shinsuishin_data/{z}/{x}/{y}.png")