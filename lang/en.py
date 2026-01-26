from textwrap import dedent

LEXICON_EN = {
    # ------------------ ENGLISH ------------------ #

    # Start
    'start_text': dedent(""" 
        Add the bot to the group for full functionality. 

        The bot can notify everyone in a group of up to 75 users, can change access rights to commands, and hide nicknames when notified.
        
        support - @merrcurys
        [github](https://github.com/Merrcurys/Mention-bot) | [news](https://t.me/merrcurys_software/41) | [faq](https://telegra.ph/FAQ-po-Mention-bot-02-05)
    """),

    # Menu
    'help_text_start': dedent(""" 
        <emoji id=5287630698776110505>😀</emoji><emoji id=5287270733272065330>😀</emoji><emoji id=5289509454910334424>😀</emoji><emoji id=5287695703106134591>😀</emoji><emoji id=5287627636464427992>😀</emoji><emoji id=5287698194187166324>😀</emoji><emoji id=5287762975178892826>😀</emoji>
        
        <emoji id=5287353089269966535>😀</emoji> /help, /command - list of all commands
        
        <emoji id=5287250783148976769>😀</emoji> /all, /here, /everyone - mention all users
    """),

    'help_text_3_many': dedent(""" 
        <emoji id=5287753603560252687>😀</emoji> /access_toggle - changing access rights for mentions (<emoji id=6037496202990194718>🔒</emoji>)
    """),

    'help_text_3_only': dedent(""" 
        <emoji id=5287753603560252687>😀</emoji> /access_toggle - changing access rights for mentions (<emoji id=6037249452824072506>🔒</emoji>)
    """),

    'help_text_4_show': dedent(""" 
        <emoji id=5287257182650247240>😀</emoji> /names_visibility - changing visibility of usernames (<emoji id=6037397706505195857>👁</emoji>)
    """),

    'help_text_4_hide': dedent(""" 
        <emoji id=5287257182650247240>😀</emoji> /names_visibility - changing visibility of usernames (<emoji id=6037243349675544634>👁</emoji>)
    """),

    'help_text_end': dedent(""" 
        support - @merrcurys
        version: [4.3](https://t.me/merrcurys_software/100) | [faq](https://telegra.ph/FAQ-po-Mention-bot-02-05)
    """),

    # Mention
    'all_info': "<emoji id=5321097148371058002>⚡️</emoji> Important information!",

    # Notifications
    'spam_control': "This command can only be used once per minute.",
    'many_users': "This command can be used only if there are no more than 75 users in the chat.",
    'only_admin': "Only administrators can use this command.",
    'no_users_found': "In this chat, there is no one to mention except you.",

    # Access rights to the all command
    'mention_all': "<emoji id=6037496202990194718>🔒</emoji>Now all chat members can be mentioned.",
    'mention_admin': "<emoji id=6037249452824072506>🔒</emoji>Now only administrators can mention chat members.",

    # Username display
    'show_username': "<emoji id=6037397706505195857>👁</emoji>Usernames are now displayed when chat members are mentioned.",
    'hide_username': "<emoji id=6037243349675544634>👁</emoji>Usernames are now hidden when chat members are mentioned.",

    # Language
    'lang_changed': "The language has been changed.",
    'lang_already_set': "This language is already installed.",
    'only_admin_lang': "Only administrators can use this command."
}
