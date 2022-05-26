from telegram import InlineKeyboardMarkup, InlineKeyboardButton


main_menu = InlineKeyboardMarkup([[InlineKeyboardButton('foo_cmd', callback_data='foo'),
                                   InlineKeyboardButton('bar_cmd', callback_data='bar'),
                                   # Sub menu not activated
                                   # InlineKeyboardButton('More', callback_data='more'),
                                   ]])

# From here: Completely functional sub-keyboard but not used
back_button = InlineKeyboardButton(u'\u2B05', callback_data='back')

more_menu = InlineKeyboardMarkup([[
    back_button,
    InlineKeyboardButton('sub_foo', callback_data='foo_2')
]])
