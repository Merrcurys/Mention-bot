from textwrap import dedent

from .premium_emoji import get_emoji

_EMOJI = get_emoji("ru")

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
        {header_1}{header_2}{header_3}{header_4}{header_5}{header_6}{header_7}
                
        {help} /help, /command - справка по всем командам
        
        {all} /all, /here, /everyone - оповестить всех пользователей
    """).format(**_EMOJI),

    'help_text_3_many': dedent(""" 
        {access} /access_toggle - смена прав доступа к оповещениям ({lock_all})
    """).format(**_EMOJI),

    'help_text_3_only': dedent(""" 
        {access} /access_toggle - смена прав доступа к оповещениям ({lock_admin})
    """).format(**_EMOJI),

    'help_text_4_show': dedent(""" 
        {visibility} /names_visibility - смена видимости имен ({eye_visible})
    """).format(**_EMOJI),

    'help_text_4_hide': dedent(""" 
        {visibility} /names_visibility - смена видимости имен ({eye_hidden})
    """).format(**_EMOJI),

    'help_text_end': dedent("""
        автор - @merrcurys
        связь - @lisabugx  
        version: [4.3](https://t.me/merrcurys_software/100) | [faq](https://telegra.ph/FAQ-po-Mention-bot-02-05)
    """),

    # Оповещение
    'all_info': "{bolt} Важная информация".format(**_EMOJI),

    # Уведомления
    'spam_control': "Эту команду можно использовать только один раз в минуту.",
    'many_users': "Эту команду можно использовать, если в чате не больше 75 пользователей.",
    'only_admin': "Только администраторы могут использовать данную команду.",
    'no_users_found': "В этом чате кроме вас некого оповещать.",

    # Не удалось отправить сообщение в топик/чат
    'cannot_send_topic': "⚠️ Не удалось отправить сообщение: этот топик закрыт.",
    'cannot_send_chat': "⚠️ Не удалось отправить сообщение в этот чат: у бота нет доступа или прав.",

    # Права доступа к команде all
    'mention_all': "{lock_all}Упоминать участников чата теперь могут все.".format(**_EMOJI),
    'mention_admin': "{lock_admin}Упоминать участников чата теперь могут только администраторы.".format(**_EMOJI),

    # Отображение username
    'show_username': "{eye_visible}При упоминании участников чата юзернеймы теперь отображаются.".format(**_EMOJI),
    'hide_username': "{eye_hidden}При упоминании участников чата юзернеймы теперь скрыты.".format(**_EMOJI),

    # Язык
    'lang_changed': "Язык изменен.",
    'lang_already_set': "Этот язык уже установлен.",
    'only_admin_lang': "Смена языка доступна только администраторам."
}
