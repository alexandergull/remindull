def replace_tags(string):
    string = string.replace('<', '*').replace('>', '*')
    return string


def format_text_to_pre(string):
    string = string \
        .replace('<b>', '</code><b>') \
        .replace('</b>', '</b><code>') \
        .replace('<u>', '</code><u>') \
        .replace('</u>', '</u><code>') \
        .replace('<i>', '</code><i>') \
        .replace('</i>', '</i><code>') \
        .replace('<s>', '</code><s>') \
        .replace('</s>', '</s><code>')
    string = '<code>' + string + '</code>'
    return string


def ip_is_valid(ip_string: str):
    import ipaddress
    try:
        ipaddress.ip_address(ip_string)
        return True
    except ValueError:
        return False


def api_key_is_valid(api_key_string: str):
    import re
    if len(api_key_string) == 12:
        if re.search(r'[^a-z0-9]', api_key_string):
            return False
        return True
    else:
        return False


def translate_api_response(method_name, response):
    print('Translating API response..')

    def spam_check_extract_key_names(iterator):
        keys = []
        for ikey in iterator:
            keys.append(ikey)
        return keys

    def mx_response_handler(mxr_list):
        result = {'mx_string': '', 'mx_result': ''}
        for mxr in mxr_list:
            result['mx_string'] += mxr.lower()
            if mxr.find('ok') != -1:
                result['mx_result'] = 'Адрес <i>существует</i>.'
            else:
                result['mx_result'] = 'Адрес <i>не существует</i>.'
        return result

    if method_name == 'notice_paid_till':

        data = response['api_response']['data']
        translate = {'msg': ''}
        npt_logic = {'key_validation': '', 'is_trial': '', 'product': '', 'banners': ''}

        # logic start
        if data['valid'] == 0:
            npt_logic['key_validation'] = 'некорректный'
            translate['msg'] = f"Информация о ключе:\n" \
                               f" - ключ <b>{npt_logic['key_validation']}</b>\n"
        else:
            npt_logic['key_validation'] = 'корректный'

            if data['trial'] == 1:
                npt_logic['is_trial'] = 'триальная'
            else:
                npt_logic['is_trial'] = 'оплаченная'

            if data['product_id'] == 1:
                npt_logic['product'] = 'Anti-Spam'
            elif data['product_id'] == 4:
                npt_logic['product'] = 'Security'

            if data['show_notice'] == 1:
                npt_logic['banners'] += ' - <b>о продлении</b> в админке сайта\n'
            elif data['show_review'] == 1:
                npt_logic['banners'] += ' - с просьбой <b>об отзыве</b> в ПУ CleanTalk\n'
            else:
                npt_logic['banners'] += ' - <b>не обнаружено</b> в ответе API\n'

            translate['msg'] = f"Информация о ключе:\n" \
                               f" - ключ <i>{npt_logic['key_validation']}</i>\n" \
                               f" - предназначен для продукта <b>{npt_logic['product']}</b>\n" \
                               f" - статус подписки: <b>{npt_logic['is_trial']}</b>\n" \
                               f"Дополнительная информация:\n" \
                               f"  ID сервиса: <b>{data['service_id']}</b>\n" \
                               f" - спам атак зарегистрировано на этом сервисе: <b>{data['spam_count']}</b>\n" \
                               f" - ссылка-токен в ПУ клиента:\n" \
                               f"<i>https://cleantalk.org/my?user_token={data['user_token']}</i>\n" \
                               f"Информация об отображаемых баннерах:\n" \
                               f"{npt_logic['banners']}"

        return translate

    if method_name == 'spam_check':
        print('Translating spam_check response..')
        data = response['api_response']['data']
        ip = spam_check_extract_key_names(dict.keys(data))[0]
        email = spam_check_extract_key_names(dict.keys(data))[1]
        ip_dict = data[ip]
        email_dict = data[email]

        translate = {'intro_msg': '', 'ip_msg': '', 'email_msg': ''}

        if ip_dict['appears'] == 0 and email_dict['appears'] == 0:
            translate['intro_msg'] += 'Это <b>не спам</b>. И вот почему:'
        else:
            translate['intro_msg'] += 'Это <b>спам</b>. И вот почему:'

        # IP translation
        ip_logic = {'in_antispam': '', 'in_security': ''}

        if ip_dict['in_antispam'] == 0:
            ip_logic['in_antispam'] = \
                ' - Адрес <i>отсутствует</i> в чёрных списках Anti-Spam\n'
        elif ip_dict['in_antispam'] == 1:
            ip_logic['in_antispam'] = \
                ' - Адрес <i>занесён</i> в чёрные списки Anti-Spam, статус **Suspicious**\n'
        elif ip_dict['in_antispam'] == 2:
            ip_logic['in_antispam'] = \
                ' - Адрес <i>занесён</i> в чёрные списки  Anti-Spam, статус **Blacklisted**\n'
        else:
            ip_logic['in_antispam'] += f"Присутствие в ЧС Anti-Spam - неизвестный ответ от API:  " \
                                       f"[{ip_dict['in_antispam']}]\n"

        if ip_dict['in_security'] == 0:
            ip_logic['in_security'] = " - Адрес <i>отсутствует</i> в чёрных списках Security\n"
        elif ip_dict['in_security'] == 1:
            ip_logic['in_security'] = " - Адрес <i>занесён</i> в чёрные списки Security (Suspicious)\n"
        elif ip_dict['in_security'] == 2:
            ip_logic['in_security'] = " - Адрес <i>занесён</i> в чёрные списки  Security (Blacklisted)\n"
        else:
            ip_logic['in_security'] = f"Присутствие в ЧС Security - неизвестный ответ от API: " \
                                      f"[{ip_dict['in_security']}]\n"

        translate['ip_msg'] += f"Отчёт по IP адресу </code>{ip}<code>\n" \
                               f"{ip_logic['in_antispam']}" \
                               f"{ip_logic['in_security']}\n" \
                               f"Статистика обнаружения:\n" \
                               f" - Дата начала отслеживания: <i>{ip_dict['submitted']}</i>\n" \
                               f" - В последний раз обнаружен: <i>{ip_dict['updated']}</i>\n" \
                               f" - Частота обнаружения: <i>{ip_dict['frequency']}</i>\n" \
                               f" - Из них:\n" \
                               f"  - Появлений за последние 10 минут: <i>{ip_dict['frequency_time_10m']}</i>\n" \
                               f"  - Появлений за последний час: <i>{ip_dict['frequency_time_1h']}</i>\n" \
                               f"  - Появлений за последние сутки: <i>{ip_dict['frequency_time_24h']}</i>\n\n" \
                               f"Дополнительные сведения\n" \
                               f" - предполагаемое назначение подсети <i>{ip_dict['network_type']}</i>\n" \
                               f" - географическое положение адреса <i>{ip_dict['country']}</i>\n"

        # EMAIL translation
        email_logic = {'is_blacklisted': '', 'is_disposable': '', 'exists': '', 'mx_response': []}

        if email_dict['appears'] == 0:
            email_logic['is_blacklisted'] = f" - адрес <i>отсутствует</i> в чёрных списках"
        else:
            email_logic['is_blacklisted'] = f" - адрес <i>занесён</i> в чёрные списки"

        if email_dict['disposable_email'] == 1:
            email_logic['is_disposable'] = " - почтовый домен используется в качестве <i>одноразового</i> домена"
        else:
            email_logic['is_disposable'] = " - почтовый домен <i>не одноразовый</i>"

        if email_dict['exists'] == 1:
            email_logic['exists'] = " - адрес присутствует в базах как <i>реальный</i>"
        elif email_dict['exists'] == 0:

            email_logic['exists'] = " - адрес присутствует в базах как <i>несуществующий</i>"
        else:
            email_logic['exists'] = " - адрес ранее не проверялся на существование"

        mx_response = mx_response_handler(email_dict['email_existance_mx_response'])

        translate['email_msg'] += f"Отчёт по email адресу: {email}\n" \
                                  f"{email_logic['is_blacklisted']}\n\n" \
                                  f"Статистика обнаружения:\n" \
                                  f" - Дата начала отслеживания: <i>{email_dict['submitted']}</i>\n" \
                                  f" - В последний раз обнаружен: <i>{email_dict['updated']}</i>\n" \
                                  f" - Частота обнаружения: <i>{email_dict['frequency']}</i>\n" \
                                  f" - Из них:\n" \
                                  f"  - появлений за последние 10 минут: <i>{email_dict['frequency_time_10m']}</i>\n" \
                                  f"  - появлений за последний час: <i>{email_dict['frequency_time_1h']}</i>\n" \
                                  f"  - появлений за последние сутки: <i>{email_dict['frequency_time_24h']}</i>\n\n" \
                                  f"Дополнительные сведения:\n" \
                                  f"{email_logic['is_disposable']}\n" \
                                  f"{email_logic['exists']}\n\n" \
                                  f"Результат принудительной проверки адреса на существование:\n" \
                                  f"{mx_response['mx_result']}\n\n" \
                                  f"От MX-серверов получены следующие ответы:\n" \
                                  f"{replace_tags(mx_response['mx_string'])}"

        print(translate['intro_msg'])
        print(translate['ip_msg'])
        print(translate['email_msg'])
        return translate

    return {'msg': 'Для этого метода пока нет перевода'}
