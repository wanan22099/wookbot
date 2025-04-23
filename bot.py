import os
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# 初始化固定菜单按钮
def get_main_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("🤖 小程序"), 
                KeyboardButton("👥 群组")
            ],
            [
                KeyboardButton("📢 频道"), 
                KeyboardButton("👤 联系人")
            ]
        ],
        resize_keyboard=True,
        persistent=True  # 保持键盘持久显示
    )

# 处理 /start 命令
def start(update: Update, context: CallbackContext):
    welcome_text = "欢迎使用！请选择下方功能："
    update.message.reply_text(welcome_text, reply_markup=get_main_keyboard())

# 处理菜单点击
def handle_menu(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "🤖 小程序":
        update.message.reply_text(
            "点击打开小程序：",
            reply_markup=get_main_keyboard(),
            disable_web_page_preview=True
        )
    elif text == "👥 群组":
        update.message.reply_text(
            "立即加入讨论群组：\nhttps://t.me/your_group",
            reply_markup=get_main_keyboard()
        )
    elif text == "📢 频道":
        update.message.reply_text(
            "订阅我们的频道：\nhttps://t.me/your_channel",
            reply_markup=get_main_keyboard()
        )
    elif text == "👤 联系人":
        update.message.reply_text(
            "联系管理员：\nhttps://t.me/your_contact",
            reply_markup=get_main_keyboard()
        )

def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    PORT = int(os.environ.get("PORT", 8443))
    
    updater = Updater(TOKEN)
    
    # 注册处理器
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_menu))

    # 设置 Webhook
    webhook_url = f"https://{os.environ.get('RAILWAY_STATIC_URL')}.railway.app/{TOKEN}"
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=webhook_url
    )
    updater.idle()

if __name__ == "__main__":
    main()
