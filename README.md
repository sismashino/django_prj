初期設定
```
python -m venv venv

. venv/bin/activate  

pip install -r requirements.txt
```

.envファイルを作成し、`GOOGLE_APPLICATION_CREDENTIALS`にGemini APIのAPIキーを設定する。

起動コマンド
```
python manage.py runserver
```