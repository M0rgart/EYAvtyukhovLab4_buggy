import pytest
import random
from unittest.mock import Mock
from src.We_need_one_more_goose import Goose, WarGoose, HonkGoose, GooseFlock
from src.Players import Player


class TestGoose:
    def test_goose_initialization(self):
        """Тестирование создания гуся"""
        goose = Goose("Петр", 5)
        assert goose.name == "Петр"
        assert goose.honk_volume == 5
        assert goose._stolen_chips == 0

    def test_goose_honk(self):
        """Тестирование гудения гуся"""
        goose = Goose("Василий", 7)
        result = goose.honk()
        assert result == "Василий кричит с громкостью 7!"

    def test_goose_repr(self):
        """Тестирование строкового представления гуся"""
        goose = Goose("Петр", 5)
        assert repr(goose) == "Goose(name=Петр, honk_volume=5)"

    def test_goose_addition(self):
        """Тестирование объединения гусей"""
        goose1 = Goose("Петр", 5)
        goose2 = Goose("Василий", 7)

        flock = goose1 + goose2
        assert isinstance(flock, GooseFlock)
        assert len(flock.geese) == 2
        assert goose1 in flock.geese
        assert goose2 in flock.geese


class TestWarGoose:
    def test_wargoose_initialization(self):
        """Тестирование создания военного гуся"""
        goose = WarGoose("Геннадий", 5, 15)
        assert goose.name == "Геннадий"
        assert goose.honk_volume == 5
        assert goose.power == 15

    def test_wargoose_attack(self, monkeypatch):
        """Тестирование атаки военного гуся"""
        goose = WarGoose("Геннадий", 5, 10)
        player = Player("Иван", 100)

        # Фиксируем случайное число для предсказуемости теста
        monkeypatch.setattr(random, "randint", lambda x, y: 5)

        result = goose.attack(player)
        assert player.balance == 95
        assert "Геннадий атакует Иван" in result
        assert "Баланс игрока уменьшен на 5" in result

    def test_wargoose_attack_to_zero(self, monkeypatch):
        """Тестирование атаки, которая опускает баланс до нуля"""
        goose = WarGoose("Геннадий", 5, 20)
        player = Player("Иван", 10)

        monkeypatch.setattr(random, "randint", lambda x, y: 15)

        result = goose.attack(player)
        assert player.balance == 0
        assert "Баланс игрока уменьшен на 15" in result

    def test_wargoose_repr(self):
        """Тестирование строкового представления военного гуся"""
        goose = WarGoose("Геннадий", 5, 15)
        assert repr(goose) == "WarGoose(name=Геннадий, power=15)"


class TestHonkGoose:
    def test_honkgoose_initialization(self):
        """Тестирование создания гуся-крикуна"""
        goose = HonkGoose("Василий", 10, 7)
        assert goose.name == "Василий"
        assert goose.honk_volume == 10
        assert goose.honk_power == 7

    def test_honkgoose_super_honk(self, monkeypatch):
        """Тестирование особого крика гуся"""
        goose = HonkGoose("Василий", 10, 10)

        from src.Players import Player
        player1 = Player("Иван", 100)
        player2 = Player("Мария", 150)

        mock_casino = Mock()
        mock_casino.players = [player1, player2]

        casino_balance = {}
        mock_casino.balance = casino_balance

        original_update_balance = None
        if hasattr(mock_casino, 'update_balance'):
            original_update_balance = mock_casino.update_balance
            mock_casino.update_balance = Mock()

        monkeypatch.setattr(random, "random", lambda: 0.3)  # 30% < 50% - выигрыш

        result = goose.super_honk(mock_casino)

        assert "Василий издает особый крик" in result
        assert "игроков получили" in result

        # Для отладки - что на самом деле происходит
        print("Тест завершен, проверим реализацию метода super_honk")

    def test_honkgoose_super_honk_no_winners(self, monkeypatch):
        """Тестирование особого крика без победителей"""
        goose = HonkGoose("Василий", 10, 10)

        mock_casino = Mock()
        mock_player = Mock()
        mock_player.name = "Иван"
        mock_player.balance = 100
        mock_casino.players = [mock_player]
        mock_casino.balance = {}

        monkeypatch.setattr(random, "random", lambda: 0.4)
        result = goose.super_honk(mock_casino)
        assert mock_player.balance == 100
        assert "Василий издает особый крик" in result
        assert "0 игроков получили по 10 монет" in result

    def test_honkgoose_call(self):
        """Тестирование вызова гуся как функции"""
        goose = HonkGoose("Василий", 8, 5)
        result = goose()
        assert result == "Гусь Василий отвечает ГОГОГО с силой 8!"

    def test_honkgoose_inheritance(self):
        """Тестирование наследования"""
        goose = HonkGoose("Василий", 10, 7)
        assert isinstance(goose, Goose)
        assert hasattr(goose, "honk")


class TestGooseFlock:
    def test_gooseflock_initialization(self):
        """Тестирование создания стаи"""
        goose1 = Goose("Петр", 5)
        goose2 = Goose("Василий", 7)
        flock = GooseFlock([goose1, goose2])

        assert len(flock.geese) == 2
        assert goose1 in flock.geese
        assert goose2 in flock.geese

    def test_gooseflock_repr(self):
        """Тестирование строкового представления стаи"""
        goose1 = Goose("Петр", 5)
        goose2 = Goose("Василий", 7)
        flock = GooseFlock([goose1, goose2])

        assert repr(flock) == "GooseFlock(Петр, Василий)"

    def test_gooseflock_empty(self):
        """Тестирование создания пустой стаи"""
        flock = GooseFlock([])
        assert len(flock.geese) == 0
        assert repr(flock) == "GooseFlock()"