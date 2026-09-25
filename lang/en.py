from textwrap import dedent

from .premium_emoji import get_emoji

_EMOJI = get_emoji("en")

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
        {header_1}{header_2}{header_3}{header_4}{header_5}{header_6}{header_7}
        
        {help} /help, /command - list of all commands
        
        {all} /all, /here, /everyone - mention all users
    """).format(**_EMOJI),

    'help_text_3_many': dedent(""" 
        {access} /access_toggle - changing access rights for mentions ({lock_all})
    """).format(**_EMOJI),

    'help_text_3_only': dedent(""" 
        {access} /access_toggle - changing access rights for mentions ({lock_admin})
    """).format(**_EMOJI),

    'help_text_4_show': dedent(""" 
        {visibility} /names_visibility - changing visibility of usernames ({eye_visible})
    """).format(**_EMOJI),

    'help_text_4_hide': dedent(""" 
        {visibility} /names_visibility - changing visibility of usernames ({eye_hidden})
    """).format(**_EMOJI),

    'help_text_end': dedent("""
        author - @merrcurys
        support - @lisabugx 
        version: [4.3](https://t.me/merrcurys_software/100) | [faq](https://telegra.ph/FAQ-po-Mention-bot-02-05)
    """),

    # Mention
    'all_info': "{bolt} Important information".format(**_EMOJI),

    # Notifications
    'spam_control': "This command can only be used once per minute.",
    'many_users': "This command can be used only if there are no more than 75 users in the chat.",
    'only_admin': "Only administrators can use this command.",
    'no_users_found': "In this chat, there is no one to mention except you.",

    # Failed to send a message to a topic/chat
    'cannot_send_topic': "⚠️ Couldn't send the message: this topic is closed.",
    'cannot_send_chat': "⚠️ Couldn't send the message to this chat: the bot has no access or permissions.",

    # Access rights to the all command
    'mention_all': "{lock_all}Now all chat members can be mentioned.".format(**_EMOJI),
    'mention_admin': "{lock_admin}Now only administrators can mention chat members.".format(**_EMOJI),

    # Username display
    'show_username': "{eye_visible}Usernames are now displayed when chat members are mentioned.".format(**_EMOJI),
    'hide_username': "{eye_hidden}Usernames are now hidden when chat members are mentioned.".format(**_EMOJI),

    # Language
    'lang_changed': "The language has been changed.",
    'lang_already_set': "This language is already installed.",
    'only_admin_lang': "Only administrators can use this command."
}
