'''
    Телеграм бот на основе telebot. Написан @TrofimAl
    Ссылка на бота: @trofem_bot
'''
from dotenv import dotenv_values
import telebot as tb
import random, requests

TOKEN:str = '' # Ключ был убран ради безопасности. И кста, старый уже не активен, так что ):
bot = tb.TeleBot(TOKEN)

class TrofimBot:
    # Keyboard Markups (TG)
    markup_main = None
    markup_rps = None
    mark_combined = None

    bot_commands = {
        # обычные доступные комманды
        "start": {"label":"Начало бота", "content": "Привет! Выбери действие:"}, 
        "help": {"label": "Помощь"}, # контент генерируется внутри функции
        "info": {"label": "Информация о боте", "content": "Данный бот был создан челом: @TrofimAl, Алёшин Трофим ПКС-12."}, 
        'api': {"label": "Тест api📧", "content": "Был сгенерирован, используя запрос с моего API:"},
        # скрытые псевдо комманды
        "back": {"label":"Назад"},
        "rpc": {"label":"🪨✂️🧻"},
        "rock": {"label":"Камень🪨"}, "paper": {"label":"Бумага🧻"}, "scissors": {"label":"Ножницы✂️"}
    }
    bot_commands_length = 4 #сколько из комманд на самом деле будет видно [0:число]

    telegram_api_url = 'https://bunker-generator-trofim.vercel.app/api/character?json'

    def __init__(self):
        
        self.create_markup()
        self.register_handlers()
        bot.polling()

    
    def create_markup(self):
        ''' Создание базиса меню'''
        #   [Помощь]  [Инфо]
        #   [🪨✂️🧻] [api]
        self.markup_main = tb.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

        self.markup_main.row( 
            tb.types.KeyboardButton(self.bot_commands["help"]['label']),
            tb.types.KeyboardButton(self.bot_commands["info"]['label']) 
        )

        self.markup_main.row(
            tb.types.KeyboardButton( self.bot_commands["rpc"]['label']),
            tb.types.KeyboardButton( self.bot_commands["api"]['label']) 
        )

        # [Камень🪨] [Ножницы✂️] [Бумага🧻]
        self.markup_rps = tb.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        self.markup_rps.row( 
            tb.types.KeyboardButton(self.bot_commands["rock"]['label']), 
            tb.types.KeyboardButton(self.bot_commands["scissors"]['label']),
            tb.types.KeyboardButton(self.bot_commands["paper"]['label'])
        )

        self.mark_combined = self.markup_rps
        self.mark_combined.add(self.bot_commands["back"]['label'])

    def register_handlers(self):

        @bot.message_handler(commands=['start'])
        def send_start(message): 
            ''' Начало бота '''
            bot.reply_to(message, self.bot_commands["start"]["content"], reply_markup=self.markup_main)

        @bot.message_handler(commands=['help'])
        def send_help(message):
            ''' Все комманды '''
            bot.reply_to(
                message, 
                '\n'.join( 
                    [f"/{act} - {info['label']}" for act, info in list(self.bot_commands.items())[ 0:(self.bot_commands_length) ]] 
                ), 
                reply_markup=self.markup_main
            )

        @bot.message_handler(commands=['info'])
        def send_info(message):
            ''' Информация о боте '''
            bot.reply_to(message, self.bot_commands["info"]["content"], reply_markup=self.markup_main)
        
        @bot.message_handler(commands=['api'])
        def send_api_request(message):
            ''' Информация о боте '''
            api_request = requests.get(self.telegram_api_url).json()
            res = f"  - {'\n - '.join([ f"{fact}: {content}" for fact, content in api_request.items()])}\n - {self.bot_commands['api']['content']}\n - {self.telegram_api_url}"
            
            bot.reply_to(message, res, reply_markup=self.markup_main)


        @bot.message_handler(commands=['rpc_start'])
        def send_rock_paper_scissors_start(message):
            '''НАЧАЛО Камень ножницы бумажка'''

            bot.reply_to(message, "Выберите предмет:", reply_markup=self.markup_rps)

        @bot.message_handler(commands=['rpc_end'])
        def send_rock_paper_scissors_end(message, item):
            ''' КОНЕЦ Камень ножницы бумажка'''
            enemy_item = random.choice(["rock", "paper", "scissors"])
            result = None if (item == enemy_item) else True if (
                (item == "rock" and enemy_item == "scissors") or (item == "paper" and enemy_item == "rock") or (item == "scissors" and enemy_item == "paper")
            ) else False
            result_text = f"- Игрок: {self.bot_commands[item]['label']}\n- против\n- Бот: {self.bot_commands[enemy_item]['label']}.\n- {
                ('Выйграл '+ ('игрок' if result else 'бот')  if result != None else 'Ничья')
            }"
            
            bot.reply_to(message, result_text, reply_markup=self.mark_combined)
            print(item, enemy_item, result, "Равны?" + item == enemy_item )

        @bot.message_handler(func=lambda message: True)
        def message_comparator(message):
            ''' Каждое сообщение сравнивается с названиями комманд, а также обрабатывает кнопки, и неправильные комманды '''
            actions_dict = {
                "Назад": send_start, "Информация о боте": send_info, "Помощь": send_help, "🪨✂️🧻": send_rock_paper_scissors_start,
                self.bot_commands["api"]['label']: send_api_request,
                self.bot_commands['rock']['label']: lambda m: send_rock_paper_scissors_end(m, "rock"),
                self.bot_commands['paper']['label']: lambda m: send_rock_paper_scissors_end(m, "paper"),
                self.bot_commands['scissors']['label']: lambda m: send_rock_paper_scissors_end(m, "scissors")
            } 

            _text = message.text.strip().capitalize()
            print("Пользователь написал: " + _text)


            if _text in actions_dict:
                actions_dict[_text](message)
                return

            match _text:
                case _ if _text[0] == "/":
                    bot.reply_to(message, "Данной комманды нету. Напишите /help для полного списка.")
                case _:
                    #эхо!
                    bot.reply_to(message, f"Эхо: {_text}")

        

trofimBot = TrofimBot()
