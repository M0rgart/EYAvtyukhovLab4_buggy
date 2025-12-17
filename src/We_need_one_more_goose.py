import src.Wanna_play_kazik, src.Players
import random


class Goose:
    """
    Базовый класс гуся
    У гуся есть имя, громкость гудения и карманы для награбленного.
    Умеет объединяться в стаи

    Атрибуты:
    name - имя (кликуха) гуся
    honk_volume - громкость гудения (от 1 до 10)
    _stolen_chips - количество украденных монет
    """

    def __init__(self, name: str, honk_volume: int):
        """
        Инициализация гуся

        Аргументы:
        name - имя гуся
        honk_volume - громкость гудения гуся
        """
        self.name = name
        self.honk_volume = honk_volume
        self._stolen_chips = 0

    def honk(self) -> str:
        """
        Гусь кричит

        Возвращает:
        сообщение о крике с указанной громкостью
        """
        return f"{self.name} кричит с громкостью {self.honk_volume}!"

    def __repr__(self) -> str:
        """
        Возвращает строковое представление гуся

        Возвращает:
        строку в формате 'Goose(name={name}, honk_volume={honk_volume})'
        """
        return f"Goose(name={self.name}, honk_volume={self.honk_volume})"

    def __add__(self, other: "Goose") -> "GooseFlock":
        """
        Объединяет гусей в стаю

        Аргументы:
        other - гусь для объединения

        Возвращает:
        новую стаю (с обоими гусями)
        """
        return GooseFlock([self, other])

class WarGoose(Goose):
    """
    Твой папаша служил во Вьетнаме? вот у этого гуся да.
    Наследуется от Goose и добавляет возможность атаковать игроков

    Атрибуты:
    power - сила атаки гуся
    """

    def __init__(self, name: str, honk_volume: int, power: int = 10):
        """
        Инициализация военного гуся

        Аргументы:
        name - имя боевого гуся
        honk_volume - громкость гусиного крика
        power - сила атки гуся
        """
        super().__init__(name, honk_volume)
        self.power = power

    def attack(self, player: 'src.Players.Player') -> str:
        """
        гусь атакует игрока, уменьшая его баланс

        Аргументы:
        player - цель для атаки

        Возвращает:
        результат атаки
        """
        dmg = random.randint(1, self.power)
        player.balance = max(0, player.balance - dmg)
        return f'{self.name} атакует {player.name}! Баланс игрока уменьшен на {dmg}'

    def __repr__(self) -> str:
        """
        Возвращает строковое представление военного гуся

        Возвращает:
        строку в формате 'WarGoose(name={name}, power={power})'
        """
        return f'WarGoose(name={self.name}, power={self.power})'

class HonkGoose(Goose):
    """
    Гусь-крикун с особыми свойствами. Наследуется от Goose
    Супер гусь может использовать ульту: super_honk

    Атрибуты:
    honk_power - сила супер-гудения
    """

    def __init__(self, name: str, honk_volume: int, honk_power: int = 10):
        """
        Инициализация кричащего гуся

        Аргументы:
        name - имя гуся
        honk_volume - громкость гусиного крика
        honk_power - сила гусиного крика
        """
        super().__init__(name, honk_volume)
        self.honk_power = honk_power

    def super_honk(self, casino: 'Wanna_play_kazik.Casino') -> str:
        """
        Особый гусиный крик, который может принести игрокам деньги.
        Каждый игрок с шансом 50% получит honk_power монет

        Аргументы:
        casino - объект казино с игроками

        Возвращает:
        результат этого особого крика с указанием количества разбогатевших игроков
        """
        res = f'{self.name} издает особый крик!'
        win = 0

        for player in casino.players:
            if random.random() > 0.5:
                player.balance += self.honk_power
                casino.balance[player.name] = player.balance
                win += 1

        return res + f' {win} игроков получили по {self.honk_power} монет.'

    def __call__(self) -> str:
        """
        Позволяет вызывать гуся как функцию

        Возвращает:
        специальное гусиное сообщение
        """
        return f'Гусь {self.name} отвечает ГОГОГО с силой {self.honk_volume}!'


class GooseFlock:
    """
    Гусиная стая
    используется объединение гусей в группу

    Атрибуты:
    geese - список объектов Goose
    """

    def __init__(self, geese: list[Goose]):
        """
        Инициализация стаи

        Аргументы:
        geese - список объектов Goose
        """
        self.geese = geese

    def __repr__(self) -> str:
        """
        Возвращает строковое представление стаи

        Возвращает:
        строку в формате  'GooseFlock({goose_names})'
        """
        goose_names = ', '.join(goose.name for goose in self.geese)
        return f"GooseFlock({goose_names})"

if __name__ == "__main__":
    pass