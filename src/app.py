import logging, asyncio
import sys

from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.filters.state import StatesGroup, State
from bot import dp, bot
from utils.create_qr.create_QR import create_qr


from data import config

class QR_State(StatesGroup):
    enter_text = State()
    choosing_size_qr = State()


list_status_subscribe = ['creator', 'administrator', 'member', 'restricted']


# Отправка сообщения, если не подписан на канал
async def not_subscribe_channel(message: Message) -> None:

    builder_not_subscribe = InlineKeyboardBuilder()
    builder_not_subscribe.row(InlineKeyboardButton(text='Подписаться на канал', url='https://t.me/danila_beskrokov'))
    builder_not_subscribe.row(InlineKeyboardButton(text='Я подписался', callback_data='/menu'))

    await message.answer_photo(photo='AgACAgIAAxkBAAO9ZrkiXhTVuvCJvkt3mqB7aB4Z4rkAAjbhMRtsDslJq7x3TmCTeh4BAAMCAAN4AAM1BA', caption="Это бот, в котором вы можете сгенерировать qr-код для вашей ссылки или текста. "
                         "Для того, чтобы пользоваться ботом вам нужно всего лишь подписаться на канал по кнопке "
                         "в сообщении и нажать я подписался", reply_markup=builder_not_subscribe.as_markup())


@dp.message(Command(commands=["start"]))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    if state:
        await state.clear()
    user_channel_status = await bot.get_chat_member(chat_id=config.CHANNEL_ID, user_id=message.from_user.id)

    if user_channel_status.status in list_status_subscribe:
        builder_is_subscribe = InlineKeyboardBuilder()

        builder_is_subscribe.row(InlineKeyboardButton(text='Создать qr-код', callback_data='create_qr'))
        builder_is_subscribe.row(InlineKeyboardButton(text='Другие полезные боты', callback_data='other_bots'))
        builder_is_subscribe.row(InlineKeyboardButton(text='Поблагодарить автора бота', callback_data='gift_creator'))
        builder_is_subscribe.row(InlineKeyboardButton(text='Заказать разработку бота', callback_data='order_bot'))
        await message.answer_photo(photo='AgACAgIAAxkBAAO9ZrkiXhTVuvCJvkt3mqB7aB4Z4rkAAjbhMRtsDslJq7x3TmCTeh4BAAMCAAN4AAM1BA', caption="Добрый день! В данном боте вы можете создать и скачать qr-код для ссылки или какого-либо текста"
                             " или перейти в другие полезные боты", reply_markup=builder_is_subscribe.as_markup())

    else:
        await not_subscribe_channel(message)





@dp.callback_query(F.func(lambda c: c.data and c.data == 'create_qr'))
async def command_start_handler2(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    if state:
        await state.clear()
    user_channel_status = await bot.get_chat_member(chat_id=config.CHANNEL_ID, user_id=callback_query.from_user.id)

    if user_channel_status.status in list_status_subscribe:
        keyboards_create_qr = InlineKeyboardBuilder()
        keyboards_create_qr.button(text='Вернуться в меню', callback_data='/menu')
        keyboards_create_qr.button(text='Другие полезные боты', callback_data='other_bots')
        await callback_query.message.answer("Пришлите ссылку или текст, для которой надо создать qr-код",
                                            reply_markup=keyboards_create_qr.as_markup())
        await state.set_state(QR_State.enter_text)
    else:
        await not_subscribe_channel(callback_query.message)


@dp.message(QR_State.enter_text)
async def get_text_for_qr(message: Message, state: FSMContext):
    if len(message.text) > 4000:
        await message.answer('Длина текста или ссылки должна быть меньше 4000 символов, сократите ваш текст')
    else:
        await state.update_data(enter_text=message.text)
        await message.answer('Теперь пришлите размер qr-кода от 1 до 10')
        await state.set_state(QR_State.choosing_size_qr)


@dp.message(QR_State.choosing_size_qr)
async def get_size_qr(message: Message, state: FSMContext):
    if message.text in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
        await state.update_data(choosing_size_qr=message.text)
        user_data = await state.get_data()
        await message.answer(f'Запрос принят! 💭Уже создаю ответ!')
        name_file = create_qr(user_data['enter_text'], user_data['choosing_size_qr'], message.from_user.id)
        photo = FSInputFile(f"{name_file}")

        keyboard_qr = InlineKeyboardBuilder()

        keyboard_qr.row(InlineKeyboardButton(text='Создать ещё', callback_data='create_qr'))
        keyboard_qr.row(InlineKeyboardButton(text='Отблагодарить автора бота', callback_data='gift_creator'))
        keyboard_qr.row(InlineKeyboardButton(text='Вернуться в меню', callback_data='/menu'))


        await message.answer_photo(photo=photo, reply_markup=keyboard_qr.as_markup())

        await state.clear()
    else:
        await message.answer('Напишите размер qr-кода от 1 до 10')


# Команда другие боты
@dp.callback_query(F.func(lambda c: c.data == 'other_bots'))
async def other_bots(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()


    other_bots_buttons = InlineKeyboardBuilder()
    other_bots_buttons.row(InlineKeyboardButton(text='Вернуться в меню', callback_data='/menu'))
    await callback_query.message.answer('В будущем тут будут полезные боты, созданные мной!',
                                        reply_markup=other_bots_buttons.as_markup())



# Команда поблагодарить автора
@dp.callback_query(F.func(lambda c: c.data == 'gift_creator'))
async def gift_creator(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    gift_creator_buttons = InlineKeyboardBuilder()
    gift_creator_buttons.row(InlineKeyboardButton(text='Вернуться в меню', callback_data='/menu'))
    await callback_query.message.answer('Буду очень признателен за любую благодарность. '
                                        'Можно перевести по номеру карты `2200701026272721` '
                                        '(Просто нажмите на номер, чтобы скопировать)', parse_mode= 'markdown',
                                        reply_markup=gift_creator_buttons.as_markup())


# Команда заказать бота
@dp.callback_query(F.func(lambda c: c.data == 'order_bot'))
async def order_bot(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    order_bot_buttons = InlineKeyboardBuilder()
    order_bot_buttons.row(InlineKeyboardButton(text='Заказать бот', url='https://t.me/danila_in'))
    order_bot_buttons.row(InlineKeyboardButton(text='Вернуться в меню', callback_data='/menu'))
    await callback_query.message.answer(text='Для того, чтобы заказать бота, напишите мне в личку: "Хочу бота!" и '
                                             'я вам помогу в этом вопросе', reply_markup=order_bot_buttons.as_markup())


# Команда меню
@dp.callback_query(F.func(lambda c: c.data and c.data.startswith('/menu')))
async def request_menu(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await command_start_handler(callback_query.message, state)


#@dp.message()
async def get_id_file(message: Message):
    print(message)


@dp.message()
async def all_unexpected_messages(message: Message, state: FSMContext):
    user_channel_status = await bot.get_chat_member(chat_id=config.CHANNEL_ID, user_id=message.from_user.id)

    if user_channel_status.status in list_status_subscribe:
        await message.answer_photo(photo='AgACAgIAAxkBAAO3ZrkhabyWDSfo3tA7S-dKkm-uSS8AAjHhMRtsDslJceOHEKevqVsBAAMCAAN4AAM1BA',
                               caption='Я пока не знаю как ответить на это сообщение, я ещё только учусь, '
                                       'но в будущем я смогу ответить на этот вопрос.')


    else:
        await not_subscribe_channel(message)

async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())