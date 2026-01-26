from textwrap import dedent

LEXICON_RU = {
    # ------------------ РУССКИЙ ------------------ #

    # Старт
    'start_text': dedent(""" 
        Добавьте бота в группу, для полного функционала. 

        Бот может оповещать всех в группе до 75 пользователей, может изменять права доступа к командам, а также скрывать никнеймы при оповещении.     
        
        техподдержка - @merrcurys
        [github](https://github.com/Merrcurys/Mention-bot) | [news](https://t.me/merrcurys_software/41) | [faq](https://telegra.ph/FAQ-po-Mention-bot-02-05)          
    """),

    # Меню
    'help_text_start': dedent(""" 
        <emoji id=5287701007390746028>😀</emoji><emoji id=5287271536430948585>😀</emoji><emoji id=5287716774215689708>😀</emoji><emoji id=5289925796155106922>😀</emoji><emoji id=5287588797075170892>😀</emoji><emoji id=5289543758814127281>😀</emoji><emoji id=5287362237550307187>😀</emoji>
                
        <emoji id=5287353089269966535>😀</emoji> /help, /command - справка по всем командам
        
        <emoji id=5287250783148976769>😀</emoji> /all, /here, /everyone - оповестить всех пользователей
    """),

    'help_text_3_many': dedent(""" 
        <emoji id=5287753603560252687>😀</emoji> /access_toggle - смена прав доступа к оповещениям (<emoji id=6037496202990194718>🔒</emoji>)
    """),

    'help_text_3_only': dedent(""" 
        <emoji id=5287753603560252687>😀</emoji> /access_toggle - смена прав доступа к оповещениям (<emoji id=6037249452824072506>🔒</emoji>)
    """),

    'help_text_4_show': dedent(""" 
        <emoji id=5287257182650247240>😀</emoji> /names_visibility - смена видимости имен (<emoji id=6037397706505195857>👁</emoji>)
    """),

    'help_text_4_hide': dedent(""" 
        <emoji id=5287257182650247240>😀</emoji> /names_visibility - смена видимости имен (<emoji id=6037243349675544634>👁</emoji>)
    """),

    'help_text_end': dedent(""" 
        связь - @merrcurys
        version: [4.3](https://t.me/merrcurys_software/100) | [faq](https://telegra.ph/FAQ-po-Mention-bot-02-05)
    """),

    # Оповещение
    'all_info': "<emoji id=5321097148371058002>⚡️</emoji>Важная информация!",

    # Уведомления
    'spam_control': "Эту команду можно использовать только один раз в минуту.",
    'many_users': "Эту команду можно использовать, если в чате не больше 75 пользователей.",
    'only_admin': "Только администраторы могут использовать данную команду.",
    'no_users_found': "В этом чате кроме вас некого оповещать.",

    # Права доступа к команде all
    'mention_all': "<emoji id=6037496202990194718>🔒</emoji>Упоминать участников чата теперь могут все.",
    'mention_admin': "<emoji id=6037249452824072506>🔒</emoji>Упоминать участников чата теперь могут только администраторы.",

    # Отображение username
    'show_username': "<emoji id=6037397706505195857>👁</emoji>При упоминании участников чата юзернеймы теперь отображаются.",
    'hide_username': "<emoji id=6037243349675544634>👁</emoji>При упоминании участников чата юзернеймы теперь скрыты.",

    # Язык
    'lang_changed': "Язык изменен.",
    'lang_already_set': "Этот язык уже установлен.",
    'only_admin_lang': "Смена языка доступна только администраторам."
}
