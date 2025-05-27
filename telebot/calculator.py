log = []
while True:
    num1, num2, sym = None, None, None
    try:
        num1, num2, sym = float(input("Введите первое число: ")), float(input("Введите второе число: ")), input("Введите символ операции: ")
    except:
        print("Числа были неправильно введены.")
        continue

    if ("exit" in sym): 
        break
    result = eval(f"{num1}{sym}{num2}") 
    log.append(f"Вычисление: {num1} {sym} {num2} = {result}")
    print(F'Результат: {result}')
print("Конец")
print('\n'.join(log))