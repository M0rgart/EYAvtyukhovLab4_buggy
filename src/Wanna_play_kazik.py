import src.Players, src.We_need_one_more_goose
import random
from typing import MutableMapping, List, Dict, Iterator


class Chip:
    """
    Класс игровой фишки с определенным номиналом.

    Атрибуты:
    value - значение фишки

    Методы:
    __add__ - складывает две фишки, возвращая новую фишку с суммой номиналов
    """

    def __init__(self, value: int):
        """
        инициализация фишки с заданным номиналом

        Аргументы:
        value - номинал фишки (положительное число)
        """
        self.value = value

    def __add__(self, other: 'Chip') -> 'Chip':
        """
        Складывает две фишки

        Аргументы:
        other - вторая фишка для сложения

        Возвращает:
        Chip - новая фишка с суммой номиналов
        """
        return Chip(self.value + other.value)

    def __repr__(self):
        """
        Возвращает строковое представление фишки

        Возвращает:
        строку в формате Chip(value={value})
        """
        return f'Chip(value={self.value})'


class CasinoBalance(MutableMapping):
    """
    Управляет балансами гусей и игроков в казино (с логами)

    Атрибуты:
    _balances - словарь с балансами
    _change_log - история изменения балансов

    Методы:
    get_log - возвращает историю изменения балансов
    """

    def __init__(self):
        """
        Инициализация пустых балансов и логов
        """
        self._balances: Dict[str, int] = {}
        self._change_log: List[str] = []

    def __getitem__(self, key: str) -> int:
        """
        Возвращает баланс по ключу

        Аргументы:
        key - имя игрока или гуся

        Возвращает - текущий баланс
        """
        return self._balances[key]

    def __setitem__(self, key: str, value: int) -> None:
        """
        Устанавливает баланс для имени (запись в логах)

        Аргументы:
        key - имя игрока или гуся
        value - новое значение баланса
        """
        old_value = self._balances.get(key, 0)
        self._balances[key] = value
        change = value - old_value
        log = f'Баланс {key}: {old_value} -> {value} (Изменение: {'+' if change >= 0 else ''}{change})'
        self._change_log.append(log)
        print(f"[LOG] {log}")

    def __delitem__(self, key: str) -> None:
        """
        Удаляет запись о балансе

        Аргументы:
        key - имя игрока или гуся для удаления
        """
        del self._balances[key]

    def __iter__(self) -> Iterator[str]:
        """
        Возвращает:
        итератор по ключам словаря
        """
        return iter(self._balances)

    def __len__(self) -> int:
        """
        Возвращает:
        количество игроков и гусей с балансами
        """
        return len(self._balances)

    def __contains__(self, key: str) -> bool:
        """
        Проверяет наличие имени в словаре балансов

        Аргументы:
        key - имя игрока или гуся

        Возвращает:
        True - если пользователь есть словаре, иначе False
        """
        return key in self._balances

    def get_log(self) -> List[str]:
        """
        Возвращает:
        список строк с изменениями балансов
        """
        return self._change_log

    def __repr__(self) -> str:
        """
        Возвращает:
        строку в формате 'Casino_balance({_balances})'
        """
        return f'Casino_balance({self._balances})'


class Casino:
    """
    Основной класс для управления казино с игроками и гусями.
    Обрабатывает различные игровые события

    Атрибуты:
    players - коллекция игроков
    geese - коллекция гусей
    balance - балансы игроков
    goose_income - доходы гусей
    chips - созданные фишки

    Методы:
    register_player - регистрирует игрока
    register_geese - регистрирует гуся
    players_bet - игрок делает ставку
    geese_attack - гусь атакует
    goose_honk - гусиный honk)
    goose_steal - гусь крадет у игрока деньги
    player_panic - игрок паникует
    create_chip - создается фишка
    goose_gang - гуси объединяются в группу
    step - выполнение случайной функции
    """

    def __init__(self):
        """
        инициализация казино с коллекциями игроков и гусей, а также их балансов
        """
        self.players = src.Players.PlayerCollection()
        self.geese = src.Players.PlayerCollection()
        self.balance = CasinoBalance()
        self.goose_income = CasinoBalance()
        self.chips: List[Chip] = []

    def register_player(self, player: src.Players.Player) -> None:
        """
        Регистрирует игрока в системе казино

        Аргументы:
        player - объект для регистрации
        """
        self.players.append(player)
        self.balance[player.name] = player.balance

    def register_geese(self, goose: src.We_need_one_more_goose.Goose) -> None:
        """
        Регистрирует гуся в системе казино

        Аргументы:
        goose - гусиный объект для регистрации
        """
        self.geese.append(goose)
        self.goose_income[goose.name] = 0

    def players_bet(self) -> str:
        """
        Случайный игрок делает ставку и с шансом 33 процента утраивает ставку

        Возвращает:
        описание результатов ставки
        """
        rich_players = self.players.get_players_with_balance()
        if not rich_players:
            return 'Никто не может сделать ставку'
        player = random.choice(rich_players)
        bet = random.randint(1, min(100, player.balance))

        if player.bet(bet):
            self.balance[player.name] = player.balance
            if random.random() > 0.67:
                win = bet * 3
                player.win(win)
                self.balance[player.name] = player.balance
                return f'{player.name} ставит {bet} и выигрывает {win}!'
            return f'{player.name} ставит {bet} и проигрывает.'
        return f"{player.name} не может поставить {bet} (баланс = {player.balance})"

    def geese_attack(self) -> str:
        """
        случайный боевой гусь атакует случайного игрока в казино

        Возвращает:
        описание результатов атаки
        """
        if not self.geese or not self.players:
            return 'Нет гусей или игроков. Атака не удалась.'
        war_geese = [goose for goose in self.geese if isinstance(goose, src.We_need_one_more_goose.WarGoose)]
        if not war_geese:
            return 'Нет военных гусей. Атака не удалась.'

        goose = random.choice(war_geese)
        player = random.choice(self.players)
        old_balance = player.balance
        res = goose.attack(player)
        self.balance[player.name] = player.balance

        return res + f'(было: {old_balance}, стало: {player.balance})'

    def goose_honk(self) -> str:
        """
        Гуси гудят. А супер-гуси используют свою способность (SuperHonk)

        Возвращает:
        результат гусиного пения
        """
        if not self.geese or not self.players:
            return 'Нет гусей или игроков. Атака не удалась.'
        goose = random.choice(self.geese)
        if isinstance(goose, src.We_need_one_more_goose.HonkGoose):
            return goose.super_honk(self)
        return goose.honk()

    def goose_steal(self) -> str:
        """
        гусиный ниндзя ворует у случайного игрока деньги

        Возвращает:
        описание кражи
        """
        if not self.geese or not self.players:
            return 'Нет гусей или игроков. Атака не удалась.'

        goose = random.choice(self.geese)
        rich_players = self.players.get_players_with_balance()

        if not rich_players:
            return f"{goose.name} пытался украсть, но все игроки бомжуют."

        player = random.choice(rich_players)
        steal = random.randint(1, min(10, player.balance))
        player.balance -= steal
        self.balance[player.name] = player.balance

        current_income = self.goose_income.get(goose.name, 0)
        self.goose_income[goose.name] = current_income + steal

        return f"{goose.name} украл {steal} у {player.name} (баланс {player.balance})."

    def player_panic(self) -> str:
        """
        Случайный игрок паникует и теряет все деньги

        Возвращает:
        описание паники
        """
        if not self.players:
            return 'Нет игроков для паники.'

        rich_players = self.players.get_players_with_balance()
        if not rich_players:
            return 'Все игроки приняли антидепрессанты после проигрыша всех своих денег. Паники не будет :('
        player = random.choice(rich_players)
        lost = player.balance
        player.balance = 0
        self.balance[player.name] = 0

        return f'{player.name} паникует и теряет все {lost}!'

    def create_chip(self) -> str:
        """
        Создается новая фишка. Если существует более 2 фишек, то 2 случайных фишки объединяются

        Возвращает:
        описание созданной фишки
        """
        value = random.randint(1, 100)
        chip = Chip(value)
        self.chips.append(chip)

        if len(self.chips) > 2:
            combination = random.choice(self.chips) + random.choice(self.chips)
            return f'Создана фишка {chip}, объединена с одной из предыдущих: {combination}'
        return f'Создана фишка {chip}'

    def goose_gang(self) -> str:
        """
        Гуси объединяются в ОПГ

        Возвращает:
        результат объединения гусей
        """
        if len(self.geese) < 2:
            return 'Гусей слишком мало, они не могут объединиться в стаю'
        goose1, goose2 = random.sample(list(self.geese), 2)
        flock = goose1 + goose2
        return f'{goose1.name} и {goose2.name} объединились в стаю: {flock}!'

    def step(self) -> str:
        """
        Выполняет одно случайное событие с заданной вероятностью

        Возвращает:
        результат выполненного события
        """
        events = [
            self.players_bet,
            self.geese_attack,
            self.goose_honk,
            self.goose_steal,
            self.player_panic,
            self.create_chip,
            self.goose_gang
        ]
        weights = [0.2, 0.15, 0.15, 0.15, 0.1, 0.15, 0.1]
        return random.choices(events, weights=weights, k=1)[0]()

if __name__ == "__main__":
    pass