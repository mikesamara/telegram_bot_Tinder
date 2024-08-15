from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *


# тут будем писать наш код :)

async def start(update, context):
    dialog.mode = 'main'
    text = load_message('main')
    await send_photo(update, context, 'main')
    await send_text(update, context, text)
    await show_main_menu(update, context, {
        'start': 'главное меню бота',
        'profile': 'генерация Tinder-профля 😎',
        'opener': 'сообщение для знакомства 🥰',
        'message': 'переписка от вашего имени 😈',
        'date': 'переписка со звездами 🔥',
        'gpt': 'задать вопрос чату GPT 🧠'
    })



async def gpt(update, context):
    dialog.mode = 'gpt'
    text = load_message('gpt')
    await send_photo(update, context, 'gpt')
    await send_text(update, context, text)



async def dialog_gpt(update, context):
    text = update.message.text
    promtt = load_prompt('gpt')
    me_message = await send_text(update, context, 'Чат 🧠 думает, что ответить... ')
    answer = await chat_gpt.send_question(promtt, text)
    await me_message.edit_text(answer)


async def message(update, context):
    dialog.mode = 'message'
    text = load_message('message')
    await send_photo(update, context, 'message')
    await send_text_buttons(update, context, text, {
      'message_next': 'следующее сообщение',
      'message_date': 'Пригласить на свидание'
            
    })
    dialog.list.clear()

async def message_buttom(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()
    
    prompt = load_prompt(query)
    user_chat_history = '\n\n'.join(dialog.list)
    me_message = await send_text(update, context, 'Чат 🧠 думает, что ответить ')
    answer = await chat_gpt.send_question(prompt, user_chat_history)
    
    await me_message.edit_text(answer)
    

async def message_dialog(update, context):
    text = update.message.text
    dialog.list.append(text)


async def date(update, context):
    dialog.mode = 'date'
    text = load_message('date')
    await send_photo(update, context, 'date')
    await send_text_buttons(update, context, text, {
        'date_grande': 'Ариана Гранде 🔥',
        'date_robbie': 'Марго Робби 🔥🔥',
        'date_zendaya': 'Зендея     🔥🔥🔥',
        'date_gosling': 'Райан Гослинг 😎',
        'date_hardy': 'Том Харди   😎😎'
        
    })


async def date_dialog(update, context):
    text = update.message.text
    my_message = await send_text(update, context, 'Девушка набирает текст...')
    answer = await chat_gpt.add_message(text)
    await my_message.edit_text(answer)


async def date_buttoms(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()
    
    await send_photo(update, context, query)
    await send_text(update, context, 'Отличный выбр! Пригласите девушку (парня) на свидание за 5 сообщений')
    
    prompt= load_prompt(query)
    chat_gpt.set_prompt(prompt)

async def profile(update, context):
    dialog.mode = 'profile'
    text = load_message('profile')
    await send_photo(update, context, 'profile')
    await send_text(update, context, text)
    
    dialog.user.clear()
    dialog.count = 0
    await send_text(update, context, 'сколько Вам лет')

async def profile_dialog(update, context):
    text = update.message.text
    dialog.count += 1
    if dialog.count == 1:
        dialog.user['age'] = text
        await send_text(update, context, 'Кем вы работаете?')
    elif dialog.count == 2:
        dialog.user['occupation'] = text
        await send_text(update, context, 'У Вас есть хобби?')
    elif dialog.count == 3:
        dialog.user['hobbi'] = text
        await send_text(update, context, 'Что Вам не нравится в людях')
    elif dialog.count == 4:
        dialog.user['annoys'] = text
        await send_text(update, context, 'Цели знакомства?')
    elif dialog.count == 5:
        dialog.user['goals'] = text
        
        prompt =  load_prompt('profile')
        user_info = dialog_user_info_to_str(dialog.user)
        my_message = await send_text(update, context, 'Чат Gpt 🧠 генерирует Ваш профиль Tinder...')
        answer = await chat_gpt.send_question(prompt, user_info)
        await my_message.edit_text(answer)
    
 
async def opener(update, context):
    dialog.mode = 'opener'
    text = load_message('opener')
    await send_photo(update, context, 'opener')
    await send_text(update, context, text)
    
    dialog.user.clear()
    dialog.count = 0
    await send_text(update, context, 'Имя партнера?')

async def opener_dialog(update, context):
    text = update.message.text
    dialog.count += 1   
    
    if dialog.count == 1:
        dialog.user['name'] = text
        await send_text(update, context, 'Сколько партнеру лет?')
        
    elif dialog.count == 2:
        dialog.user['age'] = text
        await send_text(update, context, 'Оцени внешность партнера: 1 - 10 баллов')
    elif dialog.count == 3:
        dialog.user['handsome'] = text
        await send_text(update, context, 'Где работает партнер?')
    elif dialog.count == 4:
        dialog.user['work'] = text
        await send_text(update, context, 'Цель знакомства?')
    elif dialog.count == 5:
        dialog.user['goals'] = text
        promt = load_prompt('opener')
        user_info = dialog_user_info_to_str(dialog.user)
        
        my_message = await send_text(update, context, 'Чат Gpt 🧠 генерирует Ваше сообщение для знакомства...')
        answer = await chat_gpt.send_question(promt, user_info)
        
        await my_message.edit_text(answer)
        
    
    
    
    
async def hello(update, context):
    if dialog.mode == 'gpt':
        await dialog_gpt(update, context)
    elif dialog.mode == 'date':
        await date_dialog(update, context)
    elif dialog.mode == 'message':
        await message_dialog(update, context)
    elif dialog.mode == 'profile':
        await profile_dialog(update, context)
    elif dialog.mode == 'opener':
        await opener_dialog(update, context)
    else:
        await send_text(update, context, '*Привет*')
        await send_text(update, context, '_Чем я могу быть полезен тебе?_')
        await send_text(update, context, 'Вы хотели бы это? ' + update.message.text)
        await send_photo(update, context, "avatar_main")
        await send_text_buttons(update, context, 'Запустить процесс', {
            'start': 'запустить',
            'stop': 'остановить'
        })


async def hello_buttoms(update, context):
    query = update.callback_query.data
    if query == "start":
        await send_text(update, context, 'Процесс запущен')
    else:
        await send_text(update, context, 'Процесс остановлен')


dialog = Dialog()
dialog.mode = None
dialog.list =[]
dialog.count = 0
dialog.user = {}

chat_gpt = ChatGptService(token='gpt:HAQxPYQ23osmtp1E1FJuJFkblB3Tb5yvKv2J80LW8Ue2Hitv')

app = ApplicationBuilder().token("7447438390:AAFwMWQRvlWN0Ai0Al_Veg_EtWw-rf3Ad7o").build()

app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('gpt', gpt))
app.add_handler(CommandHandler('date', date))
app.add_handler(CommandHandler('message', message))
app.add_handler(CommandHandler('profile', profile))
app.add_handler(CommandHandler('opener', opener))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(date_buttoms, pattern='^date_.*'))
app.add_handler(CallbackQueryHandler(message_buttom, pattern='^message_.*'))
app.add_handler(CallbackQueryHandler(hello_buttoms))
app.run_polling()
