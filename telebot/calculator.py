
class Calculator:
    def __init__(self):
        self.log = []
        while True:
            
            res = self.main_loop()
            if res == 1:
                break

        print("Конец")
        print('\n'.join(self.log))

    def _is_exit(self, text):
        return text.strip().lower() == "exit"
                
    
    def main_loop(self):
        try:
            num1, num2, sym = None, None, None

            num1 = (input("Введите первое число: ")).strip()
            if self._is_exit(num1):
                return 1
                    
            num2 = (input("Введите второе число: ")).strip()
            if self._is_exit(num2):
                return 1

            sym = input("Введите символ операции: ").strip()
            if self._is_exit(sym):
                return 1
            elif (sym == '/' and num2 == '0'):
                print("Деление на ноль недопустимо!")
                return
            num1, num2 = float(num1), float(num2)
        except:
            print("Числа были неправильно введены.")
            return #не заканчивает

        result = eval(f"{num1}{sym}{num2}")
        self.log.append(f"Вычисление: {num1} {sym} {num2} = {result}")
        print(F'Результат: {result}')

Calculator()