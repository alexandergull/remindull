from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import methods
import json
from common import format_text_to_pre as pre
from common import ip_is_valid, replace_tags, translate_api_response, api_key_is_valid

# test data collections
test_ip_addresses = ["10.10.10.10", "188.122.82.146"]
test_email_addresses = ["ericjoneszmail@gmail.com", "regmeon@ya.ru"]
test_api_keys = ["hypy7uzarese", "w4pvofhy03br"]
test_cms_keys = ["u7yvanapu3uj"]
test_bl_api_keys = ["aa8njo6rtvrm"]


# States available
class StatesMachine(StatesGroup):
    waiting_for_method = State()
    waiting_for_apikey = State()
    waiting_for_ip = State()
    waiting_for_email = State()
    result_message = State()
    confirm_translate = State()
    # remindull
    register_wait_for_timezone = State()
    register_wait_for_forcing_period = State()


# Keyboard create method based on collection of buttons
def create_keyboard(button_list, is_resizeable, is_one_time):
    iKeyboard = types.ReplyKeyboardMarkup(is_resizeable, is_one_time)
    for iButton in button_list:
        iKeyboard.add(iButton)
    return iKeyboard


# keyboard list
keyboard_methods = create_keyboard(methods.METHOD_NAMES_AVAILABLE, True, True)
keyboard_ips = create_keyboard(test_ip_addresses, True, True)
keyboard_emails = create_keyboard(test_email_addresses, True, True)
keyboard_cms_keys = create_keyboard(test_cms_keys, True, True)
keyboard_bl_api_keys = create_keyboard(test_bl_api_keys, True, True)
keyboard_yn = create_keyboard(['Да', 'Нет'], True, True)
# remindull
keyboard_hidden = types.ReplyKeyboardRemove()
keyboard_timezones = create_keyboard('+5GMT', True, True)
keyboard_forcing_periods = create_keyboard(["30 min", "Default"], True, True)
keyboard_yes_no = create_keyboard(["Yes", "No"], True, True)


# api_key keyboard select
def select_type_of_api_key_keyboard(method_name):
    if method_name in methods.METHOD_TYPES['cms']:
        return keyboard_cms_keys
    else:
        return keyboard_bl_api_keys


# RESULT MESSAGE
async def result_message(message: types.Message, state: FSMContext):
    # read memory
    incoming_data = await state.get_data()

    # show result
    await message.answer(pre('Method URL: ') +
                         incoming_data['api_response']['url'] +
                         "\n",
                         reply_markup=keyboard_hidden)

    print(json.dumps(incoming_data['api_response']['api_response']))
    await message.answer(pre(f"API response: ") +
                         replace_tags(json.dumps(incoming_data['api_response']['api_response'])) +
                         "\n",
                         reply_markup=keyboard_hidden)

    # return to start
    await StatesMachine.confirm_translate.set()
    await message.answer(pre("Перевести с клинтолкского на русский?"), reply_markup=keyboard_yn)


# Translation confirmation
async def state_translation(message: types.Message, state: FSMContext):
    answer = message.text.lower()

    # if confirmed
    if answer == 'да':
        # read memory
        incoming_data = await state.get_data()
        translated_response = translate_api_response(
            incoming_data['selected_method'],
            incoming_data['api_response']
        )

        # throw translated response
        await message.answer(pre("Перевожу.."), reply_markup=keyboard_hidden)
        await message.answer(pre("*** начало отчёта ***"))
        for msg in translated_response.values():
            await message.answer(pre(msg))
        await message.answer(pre("*** конец отчёта ***"))

        # return to method state (new request)
        await message.answer(pre("Выберите метод:"), reply_markup=keyboard_methods)
        await StatesMachine.waiting_for_method.set()

    # if rejected
    else:
        # return to method state (new request)
        await message.answer(pre("Ну, на нет и суда нет."), reply_markup=keyboard_hidden)
        await message.answer(pre("Выберите метод:"), reply_markup=keyboard_methods)
        await StatesMachine.waiting_for_method.set()


# Start conversation there

# first state init
async def state_call_init(message: types.Message):
    # welcome and method select message
    await message.answer(pre("Приветствую вас. Выберите метод из доступных на клавиатуре ниже:"),
                         reply_markup=keyboard_methods)
    await StatesMachine.waiting_for_method.set()


# method set state
async def state_method_is_set(message: types.Message, state: FSMContext):
    # check if method is correct
    method_name = message.text.lower()
    if method_name not in methods.METHOD_NAMES_AVAILABLE:
        await message.answer(pre("Пожалуйста, выберите метод, используя клавиатуру ниже."))
        return

    # goto api_key state
    await state.update_data(selected_method=message.text.lower())

    # use appropriate keyboard using function
    ikeyboard = select_type_of_api_key_keyboard(method_name)

    # api_key welcome message
    await message.answer(pre("Теперь введите api_key, можно взять тестовый с кнопки:"), reply_markup=ikeyboard)
    await StatesMachine.waiting_for_apikey.set()


# api_key set state
async def state_apikey_is_set(message: types.Message, state: FSMContext):

    # always requires a key
    # chek if key is correct
    api_key = message.text.lower()
    if not api_key_is_valid(api_key):
        await message.answer(pre(f"К сожалению, ключ <b>{api_key}</b> некорректный, попробуйте ещё раз."))
        return
    await state.update_data(api_key=api_key)
    incoming_data = await state.get_data()

    # if notice paid till perform fetching
    if incoming_data['selected_method'] == 'notice_paid_till':

        # info message and hide keyboard
        await message.answer(pre('Вы выбрали метод ') +
                             incoming_data['selected_method'] +
                             pre(', c ключом: ') +
                             incoming_data['api_key'],
                             reply_markup=keyboard_hidden)

        # fetching using methods.py
        await state.update_data(api_response=methods.notice_paid_till(incoming_data['api_key']))

        # call reply function
        await result_message(message, state)

    #  if spam_check or ip_info go to IP insert state
    else:
        await message.answer(pre("Введите IP, можно взять тестовый с кнопки:"),
                             reply_markup=keyboard_ips)
        # go to ip set state
        await StatesMachine.waiting_for_ip.set()


# ip set state
async def state_ip_is_set(message: types.Message, state: FSMContext):

    # chek if IP is correct
    ip = message.text.lower()
    if not ip_is_valid(ip):
        await message.answer(pre(f"К сожалению, ip адрес <b>{ip}</b> некорректный, попробуйте ещё раз."))
        return
    else:
        await message.answer(pre(f"Ip адрес <b>{ip}</b> корректный."))
    await state.update_data(ip=ip)

    # reading memory
    incoming_data = await state.get_data()

    # if spam_chek in memory
    if incoming_data['selected_method'] == 'spam_check':
        # request email message and
        await message.answer(pre("Теперь введите email, можно взять тестовый с кнопки:"),
                             reply_markup=keyboard_emails)
        # go to email set state
        await StatesMachine.waiting_for_email.set()

    # if ip_info in memory
    elif incoming_data['selected_method'] == 'ip_info':

        # set api request data
        ip_info_data = {"api_key": incoming_data['api_key'],
                        "ip": incoming_data['ip']}
        # info message and hide keyboard and
        await message.answer(pre('Вы выбрали метод ') +
                             incoming_data['selected_method'] +
                             pre(', с ключом ') +
                             incoming_data['api_key'],
                             reply_markup=keyboard_hidden)
        # fetch and
        await state.update_data(api_response=methods.ip_info(ip_info_data))
        # show result using function
        await result_message(message, state)


async def state_email_is_set(message: types.Message, state: FSMContext):
    # save email to memory
    await state.update_data(email=message.text.lower())

    # read memory
    incoming_data = await state.get_data()
    spam_check_data = {"api_key": incoming_data['api_key'],
                       "ip": incoming_data['ip'],
                       "email": incoming_data['email']}
    # info message and hide keyboard and
    await message.answer(pre(f'Проверка следующих данных:\n'
                             f'Метод: spam_check\n'
                             f'API key: ') + spam_check_data['api_key'] + '\n' +
                         pre('IP: ') + spam_check_data['ip'] + '\n' +
                         pre('Email: ') + spam_check_data['email'] + '\n',
                         reply_markup=keyboard_hidden)
    # fetching and
    await state.update_data(api_response=methods.spam_check(spam_check_data))
    # show result using function
    await result_message(message, state)


# handler registration function
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(state_call_init, commands="start", state="*")
    dp.register_message_handler(state_method_is_set, state=StatesMachine.waiting_for_method)
    dp.register_message_handler(state_apikey_is_set, state=StatesMachine.waiting_for_apikey)
    dp.register_message_handler(state_ip_is_set, state=StatesMachine.waiting_for_ip)
    dp.register_message_handler(state_email_is_set, state=StatesMachine.waiting_for_email)
    dp.register_message_handler(state_translation, state=StatesMachine.confirm_translate)
