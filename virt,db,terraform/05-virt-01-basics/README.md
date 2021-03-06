# 5.1. Введение в виртуализацию. Типы и функции гипервизоров. Обзор рынка вендоров и областей применения — Алексей Храпов

## Задача 1

Опишите кратко, как вы поняли: в чем основное отличие полной (аппаратной) виртуализации, паравиртуализации и виртуализации на основе ОС.

### Ответ:
| Виртуализация на основе ОС                                                                                                            | Паравиртуализация                                                                                                                                            | Полная виртуализация                                                                                                                                                                                                                                    |
|:--------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Выделение ресурсов осуществляется на уровне ОС, используются общие динамические библиотеки, общие страницы  памяти на хостовой машине | ОС взаимодействует с программой гипервизора, который предоставляет ей гостевой API, вместо использования напрямую таких ресурсов, как таблица страниц памяти | Управление виртуальными гостевыми ОС осуществляет напрямую небольшой промежуточный слой программного обеспечения. Каждая из виртуальных машин может работать независимо, в своем пространстве аппаратных ресурсов, полностью изолированно друг от друга |
| Гостевые ОС и хостовая машина должны быть на одинаковом ядре                                                                          | Гостевые ОС подготавливаются для исполнения в виртуализированной среде, для чего их ядро незначительно модифицируется                                        | Гостевая ОС становится не привязана к архитектуре хостовой платформы и к реализации платформы виртуализации                                                                                                                                                                                                                                                        |

---
## Задача 2

Выберите один из вариантов использования организации физических серверов, в зависимости от условий использования.

Организация серверов:
- физические сервера,
- паравиртуализация,
- виртуализация уровня ОС.

Условия использования:
- Высоконагруженная база данных, чувствительная к отказу.
- Различные web-приложения.
- Windows системы для использования бухгалтерским отделом.
- Системы, выполняющие высокопроизводительные расчеты на GPU.

Опишите, почему вы выбрали к каждому целевому использованию такую организацию.

### Ответ:
 - Высоконагруженная база данных, чувствительная к отказу
   - Физический сервер

    Требуется более высокая производительность, аппаратное размещение дает более быстрый 
    отклик и сокращает точки отказа в виде гипервизора хостовой машны. Однако, если бы 
     предлагалась полная аппаратная виртуализация, то, при условии организации кластера, 
     такой вариант, как мне кажется, подходил бы больше.


 - Различные web-приложения
   - Виртуализация уровня ОС

    Требуется меньше ресурсов, выше скорость масштабирования при необходимости расширения. 
    нет жестких требований к аппаратнымм ресурсам, требует меньше ресурсов на администрирование


 - Windows системы для использования Бухгалтерским отделом
   - Паравиртуализация 
   
    Эффективнее делать бэкаприрование - клонирование всей ВМ, 
    возможность расширения ресурсов на уровне ВМ 
    нет критичных требований к доступу к аппаратной составляющей сервера.

        
 - Системы, выполняющие высокопроизводительные расчеты на GPU
   - Физические сервера 

    Мне кажется, для аппаратных расчетов требуется максимальный доступ к аппаратным 
    ресурсам, который физический сервер дает более эффективно. В других предложенных вариантах,
    доступ осуществляется через хостовую ОС
---
## Задача 3

Выберите подходящую систему управления виртуализацией для предложенного сценария. Детально опишите ваш выбор.

Сценарии:

1. 100 виртуальных машин на базе Linux и Windows, общие задачи, нет особых требований. Преимущественно Windows based инфраструктура, требуется реализация программных балансировщиков нагрузки, репликации данных и автоматизированного механизма создания резервных копий.
2. Требуется наиболее производительное бесплатное open source решение для виртуализации небольшой (20-30 серверов) инфраструктуры на базе Linux и Windows виртуальных машин.
3. Необходимо бесплатное, максимально совместимое и производительное решение для виртуализации Windows инфраструктуры.
4. Необходимо рабочее окружение для тестирования программного продукта на нескольких дистрибутивах Linux.
### Ответ:

1. Hyper-V
   - наиболее совместим с инфраструктурой с использованием ОС Windows,
   - меньше затрат на обучение персонала (имея инфраструктуру на MS кадры уже имеются),
   - имеет широкий функционал, позволяющий реализовать все описанные требования,
   - скорее всего используется Active Directory, соответственно, совместимость Hyper-V будет приоритетнее,
   - меньше ограничений по совместимости с аппаратной частью сервера по сравнению с VMware, который также подходит.
2. KVM
   - гостевые ОС могут быть любыми, бесплатен и вполне производителен,
   - нативен для большинства современных ядер Linux.
   
3. Hyper-V
   - максимальная совместимое решение для виртуализации Windows инфраструктуры,
   - хорошая производительность.
4. XEN, либо KVM
   - бесплатные,
   - хорошая производительность,
   - нетребовательны к аппаратным ресурсам сервера.
---
## Задача 4

Опишите возможные проблемы и недостатки гетерогенной среды виртуализации (использования нескольких систем управления виртуализацией одновременно) и что необходимо сделать для минимизации этих рисков и проблем. Если бы у вас был выбор, то создавали бы вы гетерогенную среду или нет? Мотивируйте ваш ответ примерами.

### Ответ:
Проблемы гетерогенной среды:
 - необходимо содержать несколько команд администрирования/сопровождения для разных систем,
 - гораздо ниже масштабируемость (придется масштабировать 2 или более систем), 
 - сложность при выделении ресурсов и их управлением,
 - финансовые затраты, так как необходимо содержать несколько систем одновременно (если считать платные версии),
 - проблемы миграции между разными системами, + полное дублирование всей инфраструктуры под 2 (или более) системы виртуализации,
 - если продуктовая и тестовая среда в разных системах, то отлавливать "баги" сложнее.
      
Без опыта довольно сложно сказать, как минимизировать риски этих проблем, но я бы предложил:
 - распределить системы по совместимости (Hyper-V для Windows инфраструктуры, для остальных ВМ иные),
 - обучить команду сопровождения работе с обеими системами, для взаимозаменяемости,
 - шаблонизировать типовые задачи и конфигурации для простоты выполнения, автоматизации действий и упрощению миграции.

Затрудняюсь что-то предложить дополнительно без практического опыта.
 
Исходя из имеющихся навыков, я выбрал бы одну систему, т.к. инфраструктурно, кадрово и финансово её содержать практичнее, 
но есть нюансы в используемых задачах. Для использования нескольких систем на данный момент у меня не хватает опыта и практических
навыков.