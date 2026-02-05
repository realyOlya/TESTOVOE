from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="новый питомец", callback_data="new_pet")
    builder.button(text="мои питомцы", callback_data="my_pets")
    builder.adjust(1)  # вертикальное расположение
    return builder.as_markup()

def get_cancel_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="Отмена", callback_data="cancel_form")
    builder.adjust(1)
    return builder.as_markup()