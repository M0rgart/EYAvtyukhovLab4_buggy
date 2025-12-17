import src.simulation


def main() -> None:
    """
    основная функция. Вызывает симуляцию с различными значениями.
    """
    sep = '\n' + '=' * 50 + '\n'

    print('Симуляция №1')
    print('Вызов симуляции без указания переменных')
    src.simulation.run_sim()

    print(sep)

    print('Симуляция №2')
    print('Вызов симуляции из 10 шагов')
    src.simulation.run_sim(steps=10)

    print(sep)

    print('\nСимуляция №3')
    print('Вызов симуляции по сиду')
    src.simulation.run_sim(seed=52)

    print(sep)

    print('\nСимуляция №4')
    print('Вызов симуляции по сиду с ограниченным количеством шагов')
    src.simulation.run_sim(steps=10, seed=67)

    print(sep)

    print('\nСимуляция №5')
    print('Вызов симуляции с данными пользователя')
    steps = int(input('укажите количество шагов симуляции '))
    seed = int(input('укажите сид симуляции '))
    src.simulation.run_sim(steps=steps, seed=seed)


if __name__ == "__main__":
    main()
