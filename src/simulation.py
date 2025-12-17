import random
from src.Players import *
from src.Wanna_play_kazik import *
from src.We_need_one_more_goose import *


def run_sim(steps: int = 20, seed: int | None = None) -> None:
    """
    Запускает пошаговую симуляцию работы казино с игроками и гусями.
    Создаёт казино, регестрирует игроков и гусей, выполняет заданное количество шагов
    симуляции и выводит статистику

    Аргументы:
    steps - количество шагов симуляции (по умолчанию 20)
    seed - ключ генерации событий (по умолчанию случайный)

    Выводит:
    результаты тех или иных событий
    итоговую статистику
    """
    if seed is not None:
        random.seed(seed)

    print(f"=== Начало симуляции (шагов: {steps}, seed: {seed}) ===")

    casino = Casino()

    players = [
        Player("Алексей", 200),
        Player("Мария", 150),
        Player("Иван", 100),
        Player("Ольга", 80),
    ]

    for player in players:
        casino.register_player(player)

    geese = [
        WarGoose("Боевой Геннадий", 5, 15),
        HonkGoose("Крикун Василий", 10, 7),
        Goose("Обычный Петр", 3),
        WarGoose("Атакующий Максим", 7, 12),
    ]

    for goose in geese:
        casino.register_geese(goose)

    print(f"\nИгроки: {casino.players}")
    print(f"Гуси: {casino.geese}")
    print(f"Балансы: {casino.balance}")
    print(f"Доходы гусей: {casino.goose_income}")

    print(f"\n=== Ход симуляции ===")
    for i in range(steps):
        print(f"\nШаг {i + 1}:")
        result = casino.step()
        print(f"  {result}")

    print(f"\n=== Итоги симуляции ===")
    print(f"Финальные балансы: {casino.balance}")
    print(f"Доходы гусей: {casino.goose_income}")

    print(f"\n=== Статистика ===")
    rich_players = casino.players.get_players_with_balance()
    print(f"Игроков с деньгами: {len(rich_players)} из {len(casino.players)}")

    if rich_players:
        richest = max(rich_players, key=lambda p: p.balance)
        print(f"Самый богатый игрок: {richest.name} с балансом {richest.balance}")

    if casino.goose_income:
        richest_goose = max(casino.goose_income.items(), key=lambda x: x[1])
        print(f"Самый успешный гусь: {richest_goose[0]} с доходом {richest_goose[1]}")


if __name__ == "__main__":
    pass