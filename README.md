## 使い方

```bash
python3 -m venv .

source bin/activate

pip install -r requirements.txt

cp mycat-discriminator/.env.example mycat-discriminator/.env

# 学習データ作成
python mycat-discriminator/app/learn.py

# サーバ起動
python mycat-discriminator/app/server.py
# open http://localhost:8001

```
