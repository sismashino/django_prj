# chatapp/views.py
from django.shortcuts import render
import google.generativeai as genai

import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel

import chatapp.get_location as get_location

# 初期化: 会話履歴をリストで管理
conversation_history = []

def generate_response(prompt):
    global conversation_history
    
    # サービスアカウントキーのパス
    credentials_path = 'gen-lang-client-0746535071-b4820369d744.json'

    # サービスアカウントキーを用いて認証情報オブジェクトを作成
    credentials = service_account.Credentials.from_service_account_file(credentials_path)

    # Vertex AI APIの初期化
    vertexai.init(project='gen-lang-client-0746535071', location='asia-northeast1', credentials=credentials)

    model = GenerativeModel('gemini-1.5-flash')
        
    conversation_history.append(prompt)  # 今回のプロンプトを履歴に追加


    context = "\n".join(conversation_history)

    # システムメッセージを作成
    system_message = f"これまでの会話:\n{context}\n\n次の質問:"+ prompt
    
    response = model.generate_content(system_message)
    conversation_history.append(response.text)  # レスポンスを履歴に追加
    return conversation_history

def chat(request):
    global conversation_history
    res = ''
    maps = []
    floods = []
    if request.method == 'POST':
        text = request.POST.get('message')
        
        coordinates = get_location.get_lat_lon(text)
        if coordinates:
            lat = coordinates[0]
            lon = coordinates[1]
            
            for i in [13, 15, 17]:
                z, x, y = get_location.lat_lon_to_tile_coords(i, lat, lon)
                maps.append(f"https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png")
                floods.append(f"https://disaportaldata.gsi.go.jp/raster/01_flood_l2_shinsuishin_data/{z}/{x}/{y}.png")
        #res = generate_response(text)
    else:
        conversation_history = []
    return render(request, 'chatapp/chat.html', {
        'maps': maps,
        'floods': floods
        }) 