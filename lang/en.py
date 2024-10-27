from textwrap import dedent

LEXICON_EN = {
    # ------------------ ENGLISH ------------------ #

    # Menu
    'help_text': dedent(""" 
        *———COMMAND LIST———*
        
        1. /help, /command - list of all commands.
        
        2. /all, /here, /everyone - mention all users. 
        
        3. /access_toggle - toggle access rights for notifications.
        
        4. /names_visibility - toggle visibility of usernames in mentions.
        
        support - @merrcurys
        version: 3.1
    """),

    'all_info': "Important information!\n",

    # Notifications
    'spam_control': "This command can only be used once per minute.",
    'many_users': "This command can be used only if there are no more than 75 users in the chat.",
    'only_admin': "Only administrators can use this command.",

    # Access rights to the all command
    'mention_all': "Now all chat members can be mentioned.",
    'mention_admin': "Now only administrators can mention chat members.",

    # Username display
    'show_username': "Usernames are now displayed when chat members are mentioned.",
    'hide_username': "Usernames are now hidden when chat members are mentioned."
}
