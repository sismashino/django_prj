# chatapp/views.py
from django.shortcuts import render
import google.cloud
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 初期化: 会話履歴をリストで管理
conversation_history = []

def generate_response(prompt):
    global conversation_history
        
    genai.configure(api_key=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

    model = genai.GenerativeModel('gemini-1.5-flash')
        
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
    if request.method == 'POST':
        text = request.POST.get('message')
        res = generate_response(text)
    else:
        conversation_history = []
    return render(request, 'chatapp/chat.html', {'messages': res})



model = genai.GenerativeModel('gemini-1.5-flash')
