# 臺語聲 Tâi-gí-siann
這是一个 Discord bot ，會共你輸入的台語文變成一个台語音檔，予福佬話的青盲牛聽有。

## 邀請到 Discord server
https://discord.com/api/oauth2/authorize?client_id=1051050407088111616&permissions=3072&scope=bot

## 家己走的方式
```
echo DISCORD_TOKEN=[your Discord bot's token] > .env
pip3 install -r requirements.txt
python3 main.py
```

## 指令
```
$taigi [ help | rule | set_keyword [regex] | set_detect_tone [bool] | reset ]
$taigi help # 幫助
$taigi rule # 這馬的設定
$taigi set_keyword [regex] ＃ 設定會予 bot 掠出來的 keyword ，是 regular expression 。正常是 [\[「\'"\(（][台臺]語[\)）\]」\'"]$
$taigi set_detect_tone [bool] # 設定 bot 敢會掠出來有聲調的字母，是 True 抑 False 。正常是 True
$taigi reset # 共設定復原到正常的設定
```

## 原理
這个 Bot 會檢查一句話內底敢有臺羅聲調（譬如 ô），佮句尾敢有「臺語」兩字。  
若有，伊就會生音檔。  
以下兩句就會成功。  
```
這是我 ê
這是我的（臺語）
```

## 問題
若拄著無法度發音的問題，會使佇句尾加「。」，嘛會使用「""」來共毋是臺語的詞包起來。  
譬如講：  
```
這是我 ê 。
這 sī "mine"
```

## 來源
我是使用意傳科技的產品：鬥拍字的 API https://suisiann.ithuan.tw/
