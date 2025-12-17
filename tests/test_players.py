import pytest
from src.Players import Player, PlayerCollection


class TestPlayer:
    def test_player_initialization(self):
        """Тестирование создания игрока"""
        player = Player("Алексей", 200)
        assert player.name == "Алексей"
        assert player.balance == 200

    def test_player_default_balance(self):
        """Тестирование игрока со стандартным балансом"""
        player = Player("Мария")
        assert player.balance == 100

    def test_player_bet_success(self):
        """Тестирование успешной ставки"""
        player = Player("Иван", 100)
        assert player.bet(50) is True
        assert player.balance == 50

    def test_player_bet_failure(self):
        """Тестирование неудачной ставки"""
        player = Player("Ольга", 30)
        assert player.bet(50) is False
        assert player.balance == 30

    def test_player_win(self):
        """Тестирование выигрыша"""
        player = Player("Петр", 100)
        player.win(50)
        assert player.balance == 150

    def test_player_repr(self):
        """Тестирование строкового представления"""
        player = Player("Алексей", 200)
        assert repr(player) == "Player(name=Алексей, balance=200)"


class TestPlayerCollection:
    def test_collection_initialization(self):
        """Тестирование создания коллекции"""
        players = [
            Player("Алексей", 200),
            Player("Мария", 150)
        ]
        collection = PlayerCollection(players)
        assert len(collection) == 2

    def test_collection_empty_initialization(self):
        """Тестирование создания пустой коллекции"""
        collection = PlayerCollection()
        assert len(collection) == 0

    def test_collection_append(self):
        """Тестирование добавления игрока"""
        collection = PlayerCollection()
        player = Player("Алексей", 200)
        collection.append(player)
        assert len(collection) == 1
        assert collection[0] == player

    def test_collection_getitem(self):
        """Тестирование доступа по индексу"""
        player1 = Player("Алексей", 200)
        player2 = Player("Мария", 150)
        collection = PlayerCollection([player1, player2])

        assert collection[0] == player1
        assert collection[1] == player2

    def test_collection_getitem_slice(self):
        """Тестирование среза коллекции"""
        players = [Player(f"Player{i}", 100) for i in range(5)]
        collection = PlayerCollection(players)

        sliced = collection[1:3]
        assert isinstance(sliced, PlayerCollection)
        assert len(sliced) == 2

    def test_collection_setitem(self):
        """Тестирование замены игрока"""
        player1 = Player("Алексей", 200)
        player2 = Player("Мария", 150)
        collection = PlayerCollection([player1])

        collection[0] = player2
        assert collection[0] == player2

    def test_collection_delitem(self):
        """Тестирование удаления игрока"""
        player1 = Player("Алексей", 200)
        player2 = Player("Мария", 150)
        collection = PlayerCollection([player1, player2])

        del collection[0]
        assert len(collection) == 1
        assert collection[0] == player2

    def test_collection_insert(self):
        """Тестирование вставки игрока"""
        player1 = Player("Алексей", 200)
        player2 = Player("Мария", 150)
        collection = PlayerCollection([player1])

        collection.insert(0, player2)
        assert len(collection) == 2
        assert collection[0] == player2
        assert collection[1] == player1

    def test_collection_iteration(self):
        """Тестирование итерации по коллекции"""
        players = [Player(f"Player{i}", 100) for i in range(3)]
        collection = PlayerCollection(players)

        for i, player in enumerate(collection):
            assert player == players[i]

    def test_find_by_name_found(self):
        """Тестирование поиска игрока по имени (найден)"""
        player1 = Player("Алексей", 200)
        player2 = Player("Мария", 150)
        collection = PlayerCollection([player1, player2])

        result = collection.find_by_name("Мария")
        assert result == player2

    def test_find_by_name_not_found(self):
        """Тестирование поиска игрока по имени (не найден)"""
        player = Player("Алексей", 200)
        collection = PlayerCollection([player])

        result = collection.find_by_name("Неизвестный")
        assert result is None

    def test_get_players_with_balance(self):
        """Тестирование получения игроков с положительным балансом"""
        players = [
            Player("Богатый", 100),
            Player("Бедный", 0),
            Player("Обычный", 50)
        ]
        collection = PlayerCollection(players)

        rich_players = collection.get_players_with_balance()
        assert len(rich_players) == 2
        assert all(p.balance > 0 for p in rich_players)

    def test_get_players_with_balance_empty(self):
        """Тестирование получения игроков с балансом (все нули)"""
        players = [
            Player("Бедный1", 0),
            Player("Бедный2", 0)
        ]
        collection = PlayerCollection(players)

        rich_players = collection.get_players_with_balance()
        assert len(rich_players) == 0

    def test_collection_repr(self):
        """Тестирование строкового представления коллекции"""
        player = Player("Алексей", 200)
        collection = PlayerCollection([player])

        assert repr(collection) == f"PlayerCollection([{repr(player)}])"