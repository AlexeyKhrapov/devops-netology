# 7.5. Основы golang — Алексей Храпов

## Задача 1. Установите golang.
1. Воспользуйтесь инструкций с официального сайта: [https://golang.org/](https://golang.org/).
2. Так же для тестирования кода можно использовать песочницу: [https://play.golang.org/](https://play.golang.org/).

### Ответ:

Установка по инструкции прошла успешно.
```bash
kad@g-deb-test:~$ go version
go version go1.18.1 linux/amd64
```

---

## Задача 2. Знакомство с gotour.
У Golang есть обучающая интерактивная консоль [https://tour.golang.org/](https://tour.golang.org/). 
Рекомендуется изучить максимальное количество примеров. В консоли уже написан необходимый код, 
осталось только с ним ознакомиться и поэкспериментировать как написано в инструкции в левой части экрана.  

### Ответ:

Ознакомился.

---

## Задача 3. Написание кода. 
Цель этого задания закрепить знания о базовом синтаксисе языка. Можно использовать редактор кода 
на своем компьютере, либо использовать песочницу: [https://play.golang.org/](https://play.golang.org/).

1. Напишите программу для перевода метров в футы (1 фут = 0.3048 метр). Можно запросить исходные данные 
у пользователя, а можно статически задать в коде.
    Для взаимодействия с пользователем можно использовать функцию `Scanf`:
    ```
    package main
    
    import "fmt"
    
    func main() {
        fmt.Print("Enter a number: ")
        var input float64
        fmt.Scanf("%f", &input)
    
        output := input * 2
    
        fmt.Println(output)    
    }
    ```
 
1. Напишите программу, которая найдет наименьший элемент в любом заданном списке, например:
    ```
    x := []int{48,96,86,68,57,82,63,70,37,34,83,27,19,97,9,17,}
    ```
1. Напишите программу, которая выводит числа от 1 до 100, которые делятся на 3. То есть `(3, 6, 9, …)`.

В виде решения ссылку на код или сам код. 

### Ответ:

> 1. Напишите программу для перевода метров в футы (1 фут = 0.3048 метр). Можно запросить исходные данные 
у пользователя, а можно статически задать в коде.
```gotemplate
package main

import ("fmt")

func m_to_ft_convert(meters float64) float64 {
    return meters / 0.3048
} 
    
func main() {
    fmt.Print("Please enter a value in meters: ")
    var input float64
    fmt.Scanf("%f", &input)
    fmt.Printf("It's in feets: %.4f\n", m_to_ft_convert(input))
}
```
Результат выполнения:
```bash
ad@g-deb-test:~/golang/1$ go run task3-1.go 
Please enter a value in meters: 5
It's in feets: 16.4042
```

> 2. Напишите программу, которая найдет наименьший элемент в любом заданном списке, например:
    ```
    x := []int{48,96,86,68,57,82,63,70,37,34,83,27,19,97,9,17,}
    ```
```gotemplate
package main

import (
    "fmt"
    "strconv"
)

func MinNum (arr []int) (min int) {
    for i, value := range arr {
        if (i ==0) || (value < min) {
            min = value
        }
    }

    return
}

func main() {
    var min int
    x := []int{48,2,96,86,3,68,57,82,63,70,37,34,83,27,19,97,9,17,1}
    
    if len(x) == 0 {
        fmt.Errorf("Array is empty!")
    }
    
    min = MinNum(x)
    
    fmt.Println("List of elements:\n", x)
    fmt.Println("\nMinimal value is", strconv.Itoa(min))
    
}
```

Результат выполнения:
```bash
kad@g-deb-test:~/golang/2$ go run task3-2.go 
List of elements:
 [48 2 96 86 3 68 57 82 63 70 37 34 83 27 19 97 9 17 1]

Minimal value is 1
```

> 3. Напишите программу, которая выводит числа от 1 до 100, которые делятся на 3. То есть `(3, 6, 9, …)`.

```gotemplate
package main

import ("fmt")

func Div3Check(value int) bool {
    return value%3 == 0
}
    
func main() {
    for i := 1; i <= 100; i++ {
        if Div3Check(i) {
            fmt.Print(i," ")
            }
    }
    fmt.Println()  
}
```

Результат выполнения:
```bash
kkad@g-deb-test:~/golang/3$ go run task3-3.go 
3 6 9 12 15 18 21 24 27 30 33 36 39 42 45 48 51 54 57 60 63 66 69 72 75 78 81 84 87 90 93 96 99 
```

---

## Задача 4. Протестировать код (не обязательно).

Создайте тесты для функций из предыдущего задания. 

### Ответ:

1. Проверка функции конвертации из задания 1:
```gotemplate
package main

import "testing"

func TestM_to_ft_convert(t *testing.T) {
	value := 0.3048
	if m_to_ft_convert(value) != 1 {
		t.Error(value, "it's not equal to 1 ft")
	}
}
```
Результат тестирования:
```bash
kad@g-deb-test:~/golang/1$ go test -v
=== RUN   TestM_to_ft_convert
--- PASS: TestM_to_ft_convert (0.00s)
PASS
ok      task3-1 0.001s
```
2. Проверка функции нахождения наименьшего элемента массива:
```gotemplate
package main

import (
	"testing"
)

func TestMinNum(t *testing.T) {
	value := []int{3, 2, 1}
	min := MinNum(value)
	if min != 1 {
		t.Error("error in func MinFromArray()")
	}

}
```
Результат тестирования:
```bash
kad@g-deb-test:~/golang/2$ go test -v
=== RUN   TestMinNum
--- PASS: TestMinNum (0.00s)
PASS
ok      task3-2 0.001s
```
3. Проверка функции деления на 3:
```gotemplate
package main

import "testing"

func TestDiv3Check(t *testing.T) {
	value := 3
	if !Div3Check(value) {
		t.Error(value, "is not divisible by 3")
	}
}
```
Результат тестирования:
```bash
kad@g-deb-test:~/golang/3$ go test -v
=== RUN   TestDiv3Check
--- PASS: TestDiv3Check (0.00s)
PASS
ok      task3-3 0.001s
```