from deep_translator import GoogleTranslator
import requests

def draw_tarot():
    url = "https://tarotapi.dev/api/v1/cards/random?n=1"
    response = requests.get(url)
    data = response.json()

    # 檢查是否包含卡片資料
    if 'cards' in data and len(data['cards']) > 0:
        card = data['cards'][0]
        card_name = card.get('name', '未知的卡片')
        meaning = card.get('meaning_up', '無法取得正位解釋')

        # 翻譯塔羅牌解讀
        try:
            translated_meaning = GoogleTranslator(source='en', target='zh-TW').translate(meaning)
        except Exception as e:
            translated_meaning = "翻譯失敗，請參考原文：" + meaning

        return f"您抽到的是：{card_name}\n\n解讀（正位）：{translated_meaning}"
    else:
        return "抱歉，出了點錯誤！請等等星星糖！"
