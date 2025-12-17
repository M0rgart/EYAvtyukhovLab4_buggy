import pytest
import random
from unittest.mock import Mock, patch, call
from src.simulation import run_sim


class TestSimulation:
    def test_run_sim_default_parameters(self, capsys):
        """Тестирование запуска симуляции с параметрами по умолчанию"""
        with patch('random.seed') as mock_seed:
            run_sim()

            # Проверяем, что seed не устанавливался
            mock_seed.assert_not_called()

        captured = capsys.readouterr()
        assert "Начало симуляции" in captured.out
        assert "шагов: 20" in captured.out

    def test_run_sim_with_steps(self, capsys):
        """Тестирование запуска симуляции с указанным количеством шагов"""
        run_sim(steps=5)

        captured = capsys.readouterr()
        assert "шагов: 5" in captured.out
        assert "Шаг 5:" in captured.out
        assert "Шаг 6:" not in captured.out

    def test_run_sim_with_seed(self, capsys):
        """Тестирование запуска симуляции с seed"""
        run_sim(seed=42)

        captured = capsys.readouterr()
        assert "seed: 42" in captured.out

    def test_run_sim_with_steps_and_seed(self, capsys):
        """Тестирование запуска симуляции с шагами и seed"""
        run_sim(steps=3, seed=123)

        captured = capsys.readouterr()
        assert "шагов: 3" in captured.out
        assert "seed: 123" in captured.out

    def test_run_sim_registration(self, capsys):
        """Тестирование регистрации игроков и гусей"""
        run_sim(steps=0)  # Без шагов, только инициализация

        captured = capsys.readouterr()
        # Проверяем, что игроки зарегистрированы
        assert "Алексей" in captured.out
        assert "Мария" in captured.out
        assert "Иван" in captured.out
        assert "Ольга" in captured.out
        # Проверяем, что гуси зарегистрированы
        assert "Боевой Геннадий" in captured.out
        assert "Крикун Василий" in captured.out
        assert "Обычный Петр" in captured.out
        assert "Атакующий Максим" in captured.out

    def test_run_sim_statistics(self, capsys):
        """Тестирование вывода статистики"""
        run_sim(steps=1)

        captured = capsys.readouterr()
        assert "Итоги симуляции" in captured.out
        assert "Статистика" in captured.out
        assert "Игроков с деньгами:" in captured.out

    @patch('random.seed')
    @patch('random.random')
    @patch('random.randint')
    @patch('random.choice')
    def test_run_sim_deterministic(self, mock_choice, mock_randint, mock_random, mock_seed, capsys):
        """Тестирование детерминированной симуляции с моками"""
        mock_random.return_value = 0.5
        mock_randint.return_value = 50

        mock_casino = Mock()
        mock_casino.step.return_value = "Тестовое событие"

        mock_players = Mock()
        mock_players.get_players_with_balance.return_value = [Mock(name="Тест", balance=100)]

        type(mock_players).__len__ = Mock(return_value=1)
        mock_casino.players = mock_players
        mock_casino.geese = Mock()
        type(mock_casino.geese).__len__ = Mock(return_value=4)
        mock_casino.balance = Mock()
        mock_casino.goose_income = {}

        with patch('src.simulation.Casino', return_value=mock_casino):
            run_sim(steps=2, seed=999)

            mock_seed.assert_called_once_with(999)
            assert mock_casino.step.call_count == 2

    def test_run_sim_output_structure(self, capsys):
        """Тестирование структуры вывода"""
        run_sim(steps=2)

        captured = capsys.readouterr()
        output = captured.out

        # Проверяем структуру вывода
        assert "=== Начало симуляции" in output
        assert "Игроки:" in output
        assert "Гуси:" in output
        assert "Балансы:" in output
        assert "Доходы гусей:" in output
        assert "=== Ход симуляции ===" in output
        assert "Шаг 1:" in output
        assert "Шаг 2:" in output
        assert "=== Итоги симуляции ===" in output
        assert "=== Статистика ===" in output