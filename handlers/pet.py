from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import get_main_menu, get_cancel_menu
from database import add_pet, get_pets_by_owner
from utils import validate_date
from models import Pet

router = Router()


#FSM
class Dialog_FSM(StatesGroup):
    NAME = State()
    TYPE_ANIMAL = State()
    BIRTH_DATE = State()



@router.callback_query(F.data == "new_pet")
async def new_patient(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Dialog_FSM.NAME)
    await callback.message.edit_text(
        "введите имя питомца",
        reply_markup=get_cancel_menu()
    )
    await callback.answer()



@router.message(Dialog_FSM.NAME)
async def process_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if not name or len(name) < 2 or len(name) > 50:
        await message.answer("имя некорректно, попробуйте еще раз")
        return

    await state.update_data(name=name)
    await state.set_state(Dialog_FSM.TYPE_ANIMAL)
    await message.answer(
        f"имя питомца - {name}. теперь необходимо ввести вид животного",
        reply_markup=get_cancel_menu()
    )



@router.message(Dialog_FSM.TYPE_ANIMAL)
async def process_type_animal(message: Message, state: FSMContext):
    type_animal = message.text.strip().lower()
    if not type_animal or len(type_animal) < 2 or len(type_animal) > 50:
        await message.answer("вид некорректен, попробуйте еще раз")
        return

    await state.update_data(type_animal=type_animal)
    await state.set_state(Dialog_FSM.BIRTH_DATE)
    await message.answer(
        f"далее введите дату рождения в формате ДД.ММ.ГГГГ\n"
        "если не знаете - напишите - 'нет'",
        reply_markup=get_cancel_menu()
    )



@router.message(Dialog_FSM.BIRTH_DATE)
async def process_birth_date(message: Message, state: FSMContext):
    text = message.text.strip().lower()
    if text == "нет":
        birth_date = None
    else:
        if not validate_date(text):
            await message.answer(
                "ввод дня рождения некорректен, попробуйте еще раз"
                "введите дату рождения в формате ДД.ММ.ГГГГ"
            )
            return
        birth_date = text

    data = await state.get_data()
    try:
        pet = Pet(
            name=data["name"],
            type_animal=data["type_animal"],
            birth_date=birth_date,
            owner_id=message.from_user.id
        )
    except(ValueError, TypeError):
        await message.answer("попробуйте снова:")
        return


    add_pet(pet)

    await state.clear()


    await message.answer(
        f"питомец '{pet.get_display_name()}' сохранён",
        reply_markup=get_main_menu()
    )


@router.callback_query(F.data == "my_pets")
async def show_pets(callback: CallbackQuery):
    pets = get_pets_by_owner(callback.from_user.id)

    if not pets:
        text = "у вас пока нет питомцев(.\nнажмите «новый питомец», чтобы добавить"
    else:
        text = "ваши питомцы:\n\n"
        for i, pet in enumerate(pets, 1):
            if pet.birth_date:
                text += f"{i}. {pet.name} ({pet.type_animal}, {pet.birth_date})\n"
            else:
                text += f"{i}. {pet.name} ({pet.type_animal})\n"

    await callback.message.edit_text(text, reply_markup=get_main_menu())
    await callback.answer()


@router.callback_query(F.data == "cancel_form")
async def cancel_form(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "добавение отменено",
        reply_markup=get_main_menu()
    )
    await callback.answer()