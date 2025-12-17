import pytest
import random
from unittest.mock import Mock, patch
from src.Wanna_play_kazik import Chip, CasinoBalance, Casino
from src.Players import Player, PlayerCollection
from src.We_need_one_more_goose import Goose, WarGoose, HonkGoose


class TestChip:
    def test_chip_initialization(self):
        """Тестирование создания фишки"""
        chip = Chip(50)
        assert chip.value == 50

    def test_chip_addition(self):
        """Тестирование сложения фишек"""
        chip1 = Chip(30)
        chip2 = Chip(20)
        result = chip1 + chip2

        assert isinstance(result, Chip)
        assert result.value == 50

    def test_chip_repr(self):
        """Тестирование строкового представления фишки"""
        chip = Chip(100)
        assert repr(chip) == "Chip(value=100)"


class TestCasinoBalance:
    def test_balance_initialization(self):
        """Тестирование инициализации баланса"""
        balance = CasinoBalance()
        assert len(balance) == 0
        assert len(balance._change_log) == 0

    def test_balance_setitem_new_key(self):
        """Тестирование установки нового баланса"""
        balance = CasinoBalance()
        balance["Иван"] = 100

        assert balance["Иван"] == 100
        assert len(balance) == 1
        assert len(balance.get_log()) == 1

    def test_balance_setitem_existing_key(self):
        """Тестирование изменения существующего баланса"""
        balance = CasinoBalance()
        balance["Иван"] = 100
        balance["Иван"] = 150

        assert balance["Иван"] == 150
        assert len(balance) == 1
        assert len(balance.get_log()) == 2

    def test_balance_setitem_negative_change(self):
        """Тестирование уменьшения баланса"""
        balance = CasinoBalance()
        balance["Иван"] = 100
        balance["Иван"] = 50

        log = balance.get_log()[-1]
        assert "Изменение: -50" in log

    def test_balance_delitem(self):
        """Тестирование удаления баланса"""
        balance = CasinoBalance()
        balance["Иван"] = 100

        del balance["Иван"]
        assert "Иван" not in balance
        assert len(balance) == 0

    def test_balance_iteration(self):
        """Тестирование итерации по балансам"""
        balance = CasinoBalance()
        balance["Иван"] = 100
        balance["Мария"] = 150

        keys = list(balance)
        assert "Иван" in keys
        assert "Мария" in keys
        assert len(keys) == 2

    def test_balance_len(self):
        """Тестирование подсчета количества записей"""
        balance = CasinoBalance()
        balance["Иван"] = 100
        balance["Мария"] = 150

        assert len(balance) == 2

    def test_balance_contains(self):
        """Тестирование проверки наличия ключа"""
        balance = CasinoBalance()
        balance["Иван"] = 100

        assert "Иван" in balance
        assert "Мария" not in balance

    def test_balance_get_log(self):
        """Тестирование получения логов"""
        balance = CasinoBalance()
        balance["Иван"] = 100
        balance["Мария"] = 150

        logs = balance.get_log()
        assert len(logs) == 2
        assert isinstance(logs, list)
        assert all(isinstance(log, str) for log in logs)

    def test_balance_repr(self):
        """Тестирование строкового представления"""
        balance = CasinoBalance()
        balance["Иван"] = 100

        assert repr(balance) == "Casino_balance({'Иван': 100})"


class TestCasino:
    @pytest.fixture
    def casino(self):
        """Фикстура для создания казино"""
        return Casino()

    @pytest.fixture
    def sample_players(self):
        """Фикстура для создания игроков"""
        return [
            Player("Алексей", 200),
            Player("Мария", 150),
            Player("Иван", 0),  # Без денег
        ]

    @pytest.fixture
    def sample_geese(self):
        """Фикстура для создания гусей"""
        return [
            Goose("Обычный", 5),
            WarGoose("Боевой", 5, 10),
            HonkGoose("Крикун", 8, 7),
        ]

    def test_casino_initialization(self, casino):
        """Тестирование инициализации казино"""
        assert isinstance(casino.players, PlayerCollection)
        assert isinstance(casino.geese, PlayerCollection)
        assert isinstance(casino.balance, CasinoBalance)
        assert isinstance(casino.goose_income, CasinoBalance)
        assert casino.chips == []

    def test_register_player(self, casino):
        """Тестирование регистрации игрока"""
        player = Player("Алексей", 200)
        casino.register_player(player)

        assert player in casino.players
        assert casino.balance["Алексей"] == 200

    def test_register_geese(self, casino):
        """Тестирование регистрации гуся"""
        goose = Goose("Петр", 5)
        casino.register_geese(goose)

        assert goose in casino.geese
        assert casino.goose_income["Петр"] == 0

    def test_players_bet_success(self, casino, sample_players, monkeypatch):
        """Тестирование успешной ставки игрока"""
        for player in sample_players:
            casino.register_player(player)

        # Фиксируем выбор игрока и случайные числа
        monkeypatch.setattr(random, "choice", lambda lst: sample_players[0])
        monkeypatch.setattr(random, "randint", lambda a, b: 50)
        monkeypatch.setattr(random, "random", lambda: 0.8)  # Выигрыш

        result = casino.players_bet()

        assert "Алексей" in result
        assert "выигрывает" in result
        assert casino.balance["Алексей"] == 300  # 200 - 50 + 150

    def test_players_bet_no_rich_players(self, casino):
        """Тестирование ставки без богатых игроков"""
        player = Player("Иван", 0)
        casino.register_player(player)

        result = casino.players_bet()
        assert result == "Никто не может сделать ставку"

    def test_geese_attack(self, casino, sample_players, sample_geese, monkeypatch):
        """Тестирование атаки гусей"""
        for player in sample_players:
            casino.register_player(player)
        for goose in sample_geese:
            casino.register_geese(goose)
        call_count = 0
        def mock_choice(lst):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return sample_geese[1]
            else:
                return sample_players[0]

        monkeypatch.setattr(random, "choice", mock_choice)
        result = casino.geese_attack()
        assert "атакует" in result.lower()

    def test_geese_attack_no_war_geese(self, casino, sample_players):
        """Тестирование атаки без военных гусей"""
        goose = Goose("Обычный", 5)  # Не военный гусь
        casino.register_geese(goose)
        casino.register_player(sample_players[0])

        result = casino.geese_attack()
        assert "Нет военных гусей" in result

    def test_goose_honk_honkgoose(self, casino, sample_geese, sample_players, monkeypatch):
        """Тестирование гудения гуся-крикуна"""
        for player in sample_players:
            casino.register_player(player)
        casino.register_geese(sample_geese[2])  # HonkGoose

        mock_result = "Крикун издает особый крик! 2 игроков получили по 7 монет."
        with patch.object(sample_geese[2], 'super_honk', return_value=mock_result):
            result = casino.goose_honk()
            assert result == mock_result

    def test_goose_honk_regular(self, casino, sample_geese, sample_players, monkeypatch):
        """Тестирование обычного гудения"""
        for player in sample_players:
            casino.register_player(player)
        casino.register_geese(sample_geese[0])  # Обычный гусь

        def mock_choice(lst):
            for item in lst:
                if hasattr(item, 'honk'):
                    return item
            return lst[0]

        monkeypatch.setattr(random, "choice", mock_choice)

        result = casino.goose_honk()
        assert "кричит с громкостью" in result

    def test_goose_steal(self, casino, sample_players, sample_geese, monkeypatch):
        """Тестирование кражи денег"""
        for player in sample_players[:2]:
            casino.register_player(player)
        casino.register_geese(sample_geese[0])

        call_count = 0
        def mock_choice(lst):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return sample_geese[0]
            else:
                for player in lst:
                    if player.balance > 0:
                        return player
                return lst[0]

        monkeypatch.setattr(random, "choice", mock_choice)
        monkeypatch.setattr(random, "randint", lambda a, b: 20)
        result = casino.goose_steal()
        assert "украл" in result.lower() or "попытался" in result.lower()

    def test_goose_steal_no_money(self, casino, sample_players, sample_geese, monkeypatch):
        """Тестирование кражи без денег"""
        # Только игрок без денег
        casino.register_player(sample_players[2])
        casino.register_geese(sample_geese[0])

        monkeypatch.setattr(random, "choice", lambda lst: sample_geese[0])

        result = casino.goose_steal()
        assert "пытался украсть" in result

    def test_player_panic(self, casino, sample_players, monkeypatch):
        """Тестирование паники игрока"""
        casino.register_player(sample_players[0])
        monkeypatch.setattr(random, "choice", lambda lst: sample_players[0])

        result = casino.player_panic()
        assert "паникует" in result
        assert casino.balance["Алексей"] == 0

    def test_player_panic_no_rich_players(self, casino):
        """Тестирование паники без богатых игроков"""
        player = Player("Иван", 0)
        casino.register_player(player)

        result = casino.player_panic()
        assert "Все игроки приняли антидепрессанты" in result

    def test_create_chip(self, casino, monkeypatch):
        """Тестирование создания фишки"""
        monkeypatch.setattr(random, "randint", lambda a, b: 50)

        result = casino.create_chip()
        assert "Создана фишка" in result
        assert len(casino.chips) == 1
        assert casino.chips[0].value == 50

    def test_create_chip_with_combination(self, casino, monkeypatch):
        """Тестирование создания фишки с объединением"""
        # Создаем 3 фишки заранее
        casino.chips = [Chip(10), Chip(20), Chip(30)]

        monkeypatch.setattr(random, "randint", lambda a, b: 40)

        result = casino.create_chip()
        assert "объединена" in result.lower()

    def test_goose_gang(self, casino, sample_geese, monkeypatch):
        """Тестирование объединения гусей"""
        for goose in sample_geese:
            casino.register_geese(goose)

        # Фиксируем выбор
        monkeypatch.setattr(random, "sample", lambda lst, k: [sample_geese[0], sample_geese[1]])

        result = casino.goose_gang()
        assert "объединились" in result

    def test_goose_gang_not_enough(self, casino):
        """Тестирование объединения без достаточного количества гусей"""
        goose = Goose("Одинокий", 5)
        casino.register_geese(goose)

        result = casino.goose_gang()
        assert "Гусей слишком мало" in result

    def test_step(self, casino, monkeypatch):
        """Тестирование одного шага симуляции"""
        # Добавляем минимальные данные для работы
        player = Player("Тест", 100)
        goose = Goose("Тестовый", 5)
        casino.register_player(player)
        casino.register_geese(goose)

        # Фиксируем выбор события
        monkeypatch.setattr(random, "choices", lambda events, weights, k: [casino.create_chip])
        monkeypatch.setattr(random, "randint", lambda a, b: 25)

        result = casino.step()
        assert "Создана фишка" in result

    def test_step_empty_casino(self, casino, monkeypatch):
        """Тестирование шага в пустом казино"""
        # Фиксируем событие, которое не требует данных
        monkeypatch.setattr(random, "choices", lambda events, weights, k: [casino.create_chip])
        monkeypatch.setattr(random, "randint", lambda a, b: 25)

        result = casino.step()
        assert "Создана фишка" in result