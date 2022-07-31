# 11.01 Введение в микросервисы — Алексей Храпов

## Задача 1: Интернет Магазин

Руководство крупного интернет магазина у которого постоянно растёт пользовательская база и количество заказов рассматривает возможность переделки своей внутренней ИТ системы на основе микросервисов. 

Вас пригласили в качестве консультанта для оценки целесообразности перехода на микросервисную архитектуру. 

Опишите какие выгоды может получить компания от перехода на микросервисную архитектуру и какие проблемы необходимо будет решить в первую очередь.

---
### **Ответ:**

- Выгоды при переходе на микросервисную архитектуру:

    - Высокая отказоустойчивость (сбой микросервиса не ведет к выходу из строя всей системы);
    - Упрощение масштабируемости;
    - Возможность замены части сервиса на другую, не затрагивая остальные компоненты;
    - Ускорение внесения изменений в функционал;
    - Возможность использования наболее подходящих ресурсов для выполнения конкретных задач (например, разных языков прогромирования или разных фреймфорков);
    - Возможность более детального мониторинга, что поможет ускорить решение возникающих проблем;
    - Возможность разработки разных сервисов разными разработчиками, ускоряя процесс разработки и внедрения.

- Проблемы при переходе на микросервисную архитектуру:

    - Проектирование инфраструктуры с применением микросервисов требует достаточно высокой квалификации;
    - Необходимость настройки каждого отдельного микросервиса;
    - Необходимость в мониторинге и логировании большего количества сервисов;
    - Необходимость строго контроля доступа к сервисам из вне;
    - Необходиомть обеспечения совместимости API микросервисов;
    - Нобходимость дополнительного ПО для автоматизации сборки и тестирования кода.