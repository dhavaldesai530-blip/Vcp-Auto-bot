import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

# Telegram Credentials
TELEGRAM_BOT_TOKEN = "8868194866:AAHUmnjNV_dKKvzPtI_RrxnOZ3AeflB7kxM
TELEGRAM_CHAT_ID = "vcpkrishnabot"

def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram Alert Error: {str(e)}")

PAPER_CAPITAL = 100000
MAX_RISK_PER_TRADE = 1500

@app.route('/vcp_webhook', methods=['POST'])
def process_vcp_webhook():
    try:
        data = request.json
        symbol = data.get("symbol", "UNKNOWN")
        entry_price = float(data.get("price", 0))
        stop_loss = float(data.get("stop_loss", 0))
        
        risk_per_share = entry_price - stop_loss
        if risk_per_share <= 0:
            return json.dumps({"status": "INVALID_SL"}), 400
            
        qty = max(int(MAX_RISK_PER_TRADE / risk_per_share), 1)
        trade_value = round(qty * entry_price, 2)
        
        telegram_msg = (
            f"📝 *VCP PAPER TRADE EXECUTED*\n\n"
            f"📌 *Stock:* {symbol}\n"
            f"🟢 *Action:* BUY (Simulated)\n"
            f"🔢 *Quantity:* {qty}\n"
            f"💰 *Entry Price:* ₹{entry_price}\n"
            f"🛑 *Stop Loss:* ₹{stop_loss}\n"
            f"💵 *Trade Value:* ₹{trade_value}\n\n"
            f"⚡ _Executed 24/7 on Cloud Engine_"
        )
        
        send_telegram_alert(telegram_msg)
        return json.dumps({"status": "SUCCESS", "symbol": symbol}), 200

    except Exception as e:
        error_msg = f"❌ *Trade Failed:* {str(e)}"
        send_telegram_alert(error_msg)
        return json.dumps({"status": "ERROR", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
