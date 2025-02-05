from textwrap import dedent

LEXICON_RU = {
    # ------------------ РУССКИЙ ------------------ #

    'start_text': dedent(""" 
        Добавьте бота в группу, для полного функционала. 

        Бот может оповещать всех в группе до 75 пользователей, может изменять права доступа к командам, а также скрывать никнеймы при оповещении.     
        
        техподдержка - @merrcurys
        [github](https://github.com/Merrcurys/Mention-bot) | [news](https://t.me/merrcurys_software/41) | [faq](https://telegra.ph/FAQ-po-Mention-bot-02-05)          
    """),

    # Меню
    'help_text': dedent(""" 
        **———СПИСОК КОМАНД———**
        
        1. /help, /command - справка по всем командам.
        
        2. /all, /here, /everyone - позвать всех пользователей. 
        
        3. /access_toggle - тумблер прав доступа к оповещениям.
        
        4. /names_visibility - тумблер для видимости имен при оповещении.
        
        техподдержка - @merrcurys
        version: [4.1](https://t.me/merrcurys_software/47) | [faq](https://telegra.ph/FAQ-po-Mention-bot-02-05)
    """),

    'all_info': "Важная информация!",

    # Уведомления
    'spam_control': "Эту команду можно использовать только один раз в минуту.",
    'many_users': "Эту команду можно использовать, если в чате не больше 75 пользователей.",
    'only_admin': "Только администраторы могут использовать данную команду.",
    'no_users_found': "В этом чате кроме вас некого оповещать.",

    # Права доступа к команде all
    'mention_all': "Упоминать участников чата теперь могут все.",
    'mention_admin': "Упоминать участников чата теперь могут только администраторы.",

    # Отображение username
    'show_username': "При упоминании участников чата юзернеймы теперь отображаются.",
    'hide_username': "При упоминании участников чата юзернеймы теперь скрыты.",

    # Язык
    'lang_changed': "Язык изменен.",
    'lang_already_set': "Этот язык уже установлен.",
    'only_admin_lang': "Смена языка доступна только администраторам."
}
