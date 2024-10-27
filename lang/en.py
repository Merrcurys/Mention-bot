from textwrap import dedent

LEXICON_EN = {
    # ------------------ ENGLISH ------------------ #

    'start_text': dedent(""" 
        Добавьте бота в группу, для полного функционала. 

        Бот может оповещать всех в группе до 75 пользователей, может изменять права доступа к командам, а также скрывать никнеймы при оповещении.
                         
        Язык бота меняется внутри группы при вызове команды /help.

        Add the bot to the group for full functionality. 

        The bot can notify everyone in a group of up to 75 users, can change access rights to commands, and hide nicknames when notified.
        
        support - @merrcurys
        [github](https://github.com/Merrcurys/Mention-bot) | [news](https://t.me/merrcurys_software/41)
    """),

    # Menu
    'help_text': dedent(""" 
        **———COMMAND LIST———**
        
        1. /help, /command - list of all commands.
        
        2. /all, /here, /everyone - mention all users. 
        
        3. /access_toggle - toggle access rights for notifications.
        
        4. /names_visibility - toggle visibility of usernames in mentions.
        
        support - @merrcurys
        version: [4.0](https://t.me/merrcurys_software/42)
    """),

    'all_info': "Important information!",

    # Notifications
    'spam_control': "This command can only be used once per minute.",
    'many_users': "This command can be used only if there are no more than 75 users in the chat.",
    'only_admin': "Only administrators can use this command.",
    'no_users_found': "In this chat, there is no one to mention except you.",

    # Access rights to the all command
    'mention_all': "Now all chat members can be mentioned.",
    'mention_admin': "Now only administrators can mention chat members.",

    # Username display
    'show_username': "Usernames are now displayed when chat members are mentioned.",
    'hide_username': "Usernames are now hidden when chat members are mentioned.",

    # Language
    'lang_changed': "The language has been changed.",
    'lang_already_set': "This language is already installed.",
    'only_admin_lang': "Only administrators can use this command."
}
