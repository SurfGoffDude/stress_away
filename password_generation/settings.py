DEFAULT_LENGTH = 16
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 100

DIGITS = '0123456789'  # 2
LOWERCASE = 'abcdefghijklmnopqrstyvwxyz'  # 0
UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTYVWXYZ'  # 1
SPECIAL = '!@#$%^&*_-?'  # 4
SIMILAR_CHARS = '1lI0O'

big_symb = 1
nums = 2
spec_symb = 4

MESSAGES = {
    'welcome': '=== Генератор безопасных паролей ===\n',
    'length_prompt': f'Введите длину пароля (по умолчанию {DEFAULT_LENGTH}): ',
    'invalid_length': f'Длина пароля должна быть от {MIN_PASSWORD_LENGTH} до {MAX_PASSWORD_LENGTH} символов',
    'include_uppercase': 'Включать заглавные буквы? (д/н) [д]: ',
    'include_digits': 'Включать цифры? (д/н) [д]: ',
    'include_special': 'Включать специальные символы? (д/н) [д]: ',
    'exclude_similar': 'Исключать похожие символы (1, l, I, 0, O)? (д/н) [д]: ',
    'generate_another': 'Сгенерировать еще один пароль? (д/н) [н]: ',
    'generate_many': 'Сгенерировать несколько паролей? (д/н) [н]: ',
    'get_count_passwords': 'Сколько хотите сгенерировать паролей? [10 паролей по умолчанию] ',
    'print_as_list': 'Вывести пароли списком? (д/н) [н]: ',
    'choose_action': """
    Что хотите сделать? 
    [1] - Сгенерировать пароль 
    [2] - Оценит пароль на безопасность
    [3] - Выйти
    
    """,
    'check_another': '\nПроверить еще один пароль? (д/н) [н]: ',
    'get_password': '\nПожалуйста введите пароль: ',
}