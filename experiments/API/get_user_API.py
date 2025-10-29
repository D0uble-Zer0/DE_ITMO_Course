def get_user_input() -> int:
    """
    Получаем от пользователя количество пивоварен
    """

    while True:
        try:
            user_input = int(input("\nСколько пивоварен вы хотите найти? : "))

            if user_input <= 0:
                print("ERROR! Число должно быть больше 0!")
                continue
            elif user_input > 10000:
                print("ERROR! Число не может быть больше 10000!")
                continue
            return user_input
        except ValueError:
            print("ERROR! Вы ввели не число, либо ввели не целое число!")
