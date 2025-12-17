from typing import Optional, Union, List, MutableSequence, Iterator


class Player:
    """
    Класс игрока в казино.
    Игрок имеет имя и баланс, может делать ставки
    (у меня нет на это время, мне нужно программировать) и зарабатывать бабки

    Атрибуты:
    name - имя игрока
    balance - баланс игрока
    """

    def __init__(self, name: str, start_balance: int = 100):
        """
        инициализация игрока

        Аргументы:
        name - имя игрока
        start_balance - стартовый капитал (поля чудес)(по умолчанию 100)
        """
        self.name = name
        self.balance = start_balance

    def bet(self, amount: int) -> bool:
        """
        Делает ставку указанного размера

        Аргументы:
        amount - размер ставки

        Возвращает:
        True если ставка была сделана, иначе False
        """
        if amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def win(self, amount: int) -> None:
        """
        победа в ставке => +бабки

        Аргументы:
        amount - размер выигрыша
        """
        self.balance += amount

    def __repr__(self) -> str:
        """
        возвращает строковое представление игрока

        Возвращает:
        строку в формате 'Player(name={name}, balance={balance})'
        """
        return f'Player(name={self.name}, balance={self.balance})'


class PlayerCollection(MutableSequence):
    """
    коллекция игроков с дополнительным функционалом.

    Атрибуты:
    _players - список игроков
    """

    def __init__(self, players: Optional[List[Player]] = None):
        """
        инициализация коллекции игроков

        Аргументы:
        players - список игроков. По умолчанию пустой
        """
        self._players = players if players is not None else []

    def __len__(self) -> int:
        """
        Возвращает:
        количество игроков
        """
        return len(self._players)

    def __getitem__(self, index: Union[int, slice]) -> Union[Player, 'PlayerCollection']:
        """
        Возвращает либо игрока по индексу, либо срез игроков

        Аргументы:
        index - либо номер игрока, либо срез

        Возвращает:
        либо игрока, либо список игроков
        """
        if isinstance(index, slice):
            return PlayerCollection(self._players[index])
        return self._players[index]

    def __setitem__(self, index: int, player: Player) -> None:
        """
        Заменяет игрока по индексу

        Аргументы:
        index - индекс игрока для замены
        player - новый объект игрока
        """
        self._players[index] = player

    def __delitem__(self, index: int) -> None:
        """
        Удаляет игрока по индексу

        Аргументы:
        index - индекс игрока
        """
        del self._players[index]

    def insert(self, index: int, player: Player) -> None:
        """
        Вставляет игрока по индексу

        Аргументы:
        index - индекс для внедрения игрока
        player - игрок для внедрения (в банду)
        """
        self._players.insert(index, player)

    def __iter__(self) -> Iterator[Player]:
        """
        Возвращает:
        итератор объектов (игроков)
        """
        return iter(self._players)

    def __repr__(self) -> str:
        """
        Возвращает строковое представление коллекции игроков

        Возвращает:
        строку в формате 'PlayerCollection({_players})'
        """
        return f'PlayerCollection({self._players})'

    def find_by_name(self, name: str) -> Optional[Player]:
        """
        Находит игрока по имени

        Аргументы:
        name - имя игрока, которого нужно найти

        Возвращает:
        объект Player если такой есть, иначе None
        """
        for player in self._players:
            if player.name == name:
                return player
        return None

    def get_players_with_balance(self) -> List[Player]:
        """
        Возвращает:
        список игроков с положительным балансом
        """
        return [player for player in self._players if player.balance > 0]


if __name__ == "__main__":
    pass