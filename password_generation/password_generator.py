import secrets
import string
from datetime import timedelta
from math import log2
from operator import length_hint
from random import shuffle

from settings import *


class PasswordGenerator:
    def __init__(self):
        self.length = DEFAULT_LENGTH
        self.use_uppercase = True
        self.use_digits = True
        self.use_special = True
        self.exclude_similar = True
        self._character_set = ''

    def configure(
            self,
            length: int = DEFAULT_LENGTH,
            use_uppercase: bool = True,
            use_digits: bool = True,
            use_special: bool = True,
            exclude_similar: bool = True
    ) -> None:
        self.length = max(MIN_PASSWORD_LENGTH, min(self.length, MAX_PASSWORD_LENGTH))
        self.use_uppercase = use_uppercase
        self.use_digits = use_digits
        self.use_special = use_special
        self.exclude_similar = exclude_similar
        self._update_character_set()

    def _update_character_set(self) -> None:
        chars = string.ascii_lowercase

        if self.use_uppercase:
            chars += UPPERCASE
        if self.use_digits:
            chars += DIGITS
        if self.use_special:
            chars += SPECIAL

        if self.exclude_similar:
            chars = ''.join(c for c in chars if c not in SIMILAR_CHARS)

        if len(chars) < MIN_PASSWORD_LENGTH:
            raise ValueError("Слишком мало доступных символов для генерации пароля")

        self._character_set = chars

    def generate(self) -> str:
        if not self._character_set:
            self._update_character_set()

        password_chars = [secrets.choice(string.ascii_lowercase)] + [secrets.choice(string.ascii_lowercase)]

        if self.use_uppercase:
            password_chars.append(secrets.choice(UPPERCASE))
            password_chars.append(secrets.choice(UPPERCASE))
        if self.use_digits:
            password_chars.append(secrets.choice(DIGITS))
            password_chars.append(secrets.choice(DIGITS))
        if self.use_special:
            password_chars.append(secrets.choice(SPECIAL))
            password_chars.append(secrets.choice(SPECIAL))

        remainig_lenght = self.length - len(password_chars)
        if remainig_lenght > 0:
            password_chars.extend(secrets.choice(self._character_set) for _ in range(remainig_lenght))

        shuffle(password_chars)

        return ''.join(password_chars)

    def generate_multiple(self, count: int) -> list[str]:
        return [self.generate() for _ in range(count)]


class PasswordSecurity:
    def __init__(self, password: str) -> None:
        self.password = password
        self.entropy = self._get_enthropy()
        self.strength = self._get_strength()
        self.time_until_crack = self._get_time_until_crack()

    def _get_strength(self) -> float:
        if not self.password:
            return 0.0

        entropy = self._get_enthropy()
        max_entropy = 128
        strength = min(100, (entropy / max_entropy) * 100)

        length = len(self.password)
        if length < 8:
            strength *= 0.5
        elif length < 12:
            strength *= 0.8

        return round(strength, 2)

    def _get_enthropy(self) -> float:
        charset = 0
        if any(c.islower() for c in self.password):
            charset += 26
        if any(c.isupper() for c in self.password):
            charset += 26
        if any(c.isdigit() for c in self.password):
            charset += 10
        if any(c in SPECIAL for c in self.password):
            charset += len(SPECIAL)

        length = len(self.password)
        return round(log2(charset ** length), 2) if charset > 0 else 0

    def _get_time_until_crack(self) -> str:
        speeds = {
            'Обычный компьютер': 10 ** 9,
            'Игровая видеокарта': 10 ** 11,
            'Ботнет': 10 ** 12,
            'Суперкомпьютер': 10 ** 15,
        }

        time_seconds = {}
        for key, speed in speeds.items():
            time_seconds[key] = (2 ** self.entropy) / speed

        result = []
        for key, seconds in time_seconds.items():
            if seconds < 1:
                result.append(f"    {key}: менее секунды")
                continue

            intervals = (
                ('лет', 31536000),
                ('дней', 86400),
                ('часов', 3600),
                ('минут', 60),
                ('секунд', 1)
            )

            parts = []
            for name, count in intervals:
                value = int(seconds // count)
                if value > 0:
                    seconds -= value * count
                    parts.append(f"{value} {name}")
                    if len(parts) == 2:
                        break

            result.append(f"    {key}: {', '.join(parts)}")

        return "\n" + "\n".join(result)
