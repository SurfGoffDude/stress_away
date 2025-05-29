from password_generation.password_generator import PasswordGenerator, PasswordSecurity
from password_generation.settings import MESSAGES, DEFAULT_LENGTH, MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH


def get_yes_no(prompt: str, default: bool = True) -> bool:
    while True:
        response = input(prompt).strip().lower()

        if not response:
            return default
        if response in ['д', 'y', 'да', 'yes']:
            return True
        if response in ['н', 'n', 'нет', 'no']:
            return False
        print("Пожалуйста, введите 'д' или 'н'.")


def get_number(prompt: str, default: int = 10) -> int:
    while True:
        try:
            count_str = input(prompt).strip()
            if not count_str:
                return default

            count = int(count_str)
            return count
        except ValueError:
            print("Подалуйста введите число.")


def get_password() -> str:
    while True:
        password = input(MESSAGES['get_password']).strip()
        if password:
            return password


def create_progressbar(progress: int) -> str:
    bar = '[' + '#' * progress + '-' * (100 - progress) + '] '
    return bar


class PasswordGeneratorService:
    def __init__(self):
        self.generator = PasswordGenerator()

    def interactive_mod(self):

        while True:
            length = self._get_length()
            use_uppercase = get_yes_no(MESSAGES['include_uppercase'], default=True)
            use_digits = get_yes_no(MESSAGES['include_digits'], default=True)
            use_special = get_yes_no(MESSAGES['include_special'], default=True)
            exclude_similar = get_yes_no(MESSAGES['exclude_similar'], default=True)

            self.generator.configure(
                length=length,
                use_uppercase=use_uppercase,
                use_digits=use_digits,
                use_special=use_special,
                exclude_similar=exclude_similar
            )

            if get_yes_no(MESSAGES['generate_many'], default=False):
                count = get_number(MESSAGES['get_count_passwords'], default=10)
                password = self.generator.generate_multiple(count)

                if get_yes_no(MESSAGES['print_as_list'], default=False):
                    print('\nВот ваши пароли:')
                    for passw in password:
                        print(passw)
                else:
                    print('\nВот ваши пароли:')
                    print(*password)
                print(f"Длина: {length} символов")

            else:
                password = self.generator.generate()

                print(f"\nСгенерированный пароль: {password}")
                print(f"Длина: {len(password)} символов")

            if not get_yes_no(MESSAGES['generate_another'], default=False):
                break

    @staticmethod
    def _get_length() -> int:
        while True:
            try:
                length_str = input(MESSAGES['length_prompt']).strip()
                if not length_str:
                    return DEFAULT_LENGTH

                lenght = int(length_str)
                if MIN_PASSWORD_LENGTH <= lenght <= MAX_PASSWORD_LENGTH:
                    return lenght
                print(MESSAGES['invalid_length'])
            except ValueError:
                print("Подалуйста введите число.")


class PasswordSecurityService:
    def __init__(self):
        self.generator = None

    def interactive_mod(self):
        while True:
            self.generator = PasswordSecurity(get_password())

            self.get_security_info()

            if not get_yes_no(MESSAGES['check_another'], default=False):
                break

    def get_security_info(self) -> None:
        strength = self.generator.strength
        print(f'\nНадежность пароля: {strength}%')
        print(create_progressbar(int(strength)))
        print(f'\nЭнтропия пароля: {self.generator.entropy} бит')
        print(f'\nВремя до взлома пароля: {self.generator.time_until_crack}')


class Service:
    @staticmethod
    def app():
        print(MESSAGES['welcome'])

        while True:
            action = get_number(MESSAGES['choose_action'], default=1)
            if not action:
                continue
            if action == 1:
                generating = PasswordGeneratorService()
                generating.interactive_mod()
            if action == 2:
                grader = PasswordSecurityService()
                grader.interactive_mod()
            if action == 3:
                exit(14)
