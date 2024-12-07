def ru_plural(n: int) -> str:
    """
    Возвращает правильное окончание слова в зависимости от количества.
    """
    n = abs(n)
    n %= 100
    if 5 <= n <= 20:
        return 'many'
    n %= 10
    if n == 1:
        return 'one'
    if 2 <= n <= 4:
        return 'few'
    return 'many'