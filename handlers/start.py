from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from keyboards import get_main_menu
from database import get_pets_by_owner

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Здарствуйте, я - бот ветеринарной клиники \nвыберите действие:",
        reply_markup=get_main_menu()
    )


#пациенты на старте
@router.message(Command("pets"))
async def cmd_patients(message: Message):
    pets = get_pets_by_owner(message.from_user.id)

    if not pets:
        text = "нету питомцев"
    else:
        text = "ваши питомцы:\n\n"
        for i, (name, species, birth_date) in enumerate(pets, 1):
            if birth_date:
                text += f"{i}. {name} ({species}, {birth_date})\n"
            else:
                text += f"{i}. {name} ({species})\n"

    await message.answer(text)