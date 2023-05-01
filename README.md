# Tai5-gi2-siann
這是一个 Discord bot ，會共你輸入的台語文變成一个台語音檔，予福佬話的青盲牛聽有。

## 邀請到 Discord server
https://discord.com/api/oauth2/authorize?client_id=1051050407088111616&permissions=3072&scope=bot

## 家己走的方式
```
echo DISCORD_TOKEN=[your Discord bot's token] > .env
pip3 install -r requirements.txt
python3 main.py
```

## 原理
這个 Bot 會檢查一句話內底敢有臺羅聲調（譬如 ô），佮句尾敢有「臺語」兩字
若有，伊就會生音檔

## 來源
我是使用意傳科技的產品：鬥拍字的 API https://suisiann.ithuan.tw/
