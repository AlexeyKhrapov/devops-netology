# 09.05 Teamcity — Алексей Храпов

## Основная часть

1. Создайте новый проект в teamcity на основе fork
2. Сделайте autodetect конфигурации<details><summary>Результат выполнения</summary>
![](./src/2.png)
</details>

3. Сохраните необходимые шаги, запустите первую сборку master'a<details><summary>Результат выполнения</summary>
![](./src/3.png)
</details>

4. Поменяйте условия сборки: если сборка по ветке `master`, то должен происходит `mvn clean deploy`, иначе `mvn clean test`<details><summary>Результат выполнения</summary>
![](./src/4.png)
</details>

5. Для deploy будет необходимо загрузить [settings.xml](./teamcity/settings.xml) в набор конфигураций maven у teamcity, предварительно записав туда креды для подключения к nexus<details><summary>Результат выполнения</summary>
![](./src/5.png)
</details>

6. В pom.xml необходимо поменять ссылки на репозиторий и nexus<details><summary>Результат выполнения</summary>
![](./src/6.png)
</details>

7. Запустите сборку по master, убедитесь что всё прошло успешно, артефакт появился в nexus<details><summary>Результат выполнения</summary>
![](./src/7.png)
</details>

8. Мигрируйте `build configuration` в репозиторий<details><summary>Результат выполнения</summary>
![](./src/8.png)
</details>

9. Создайте отдельную ветку `feature/add_reply` в репозитории
10. Напишите новый метод для класса Welcomer: метод должен возвращать произвольную реплику, содержащую слово `hunter`
11. Дополните тест для нового метода на поиск слова `hunter` в новой реплике
12. Сделайте push всех изменений в новую ветку в репозиторий
13. Убедитесь что сборка самостоятельно запустилась, тесты прошли успешно<details><summary>Результат выполнения</summary>
![](./src/13.png)
</details>

14. Внесите изменения из произвольной ветки `feature/add_reply` в `master` через `Merge`
15. Убедитесь, что нет собранного артефакта в сборке по ветке `master`
16. Настройте конфигурацию так, чтобы она собирала `.jar` в артефакты сборки<details><summary>Результат выполнения</summary>
![](./src/16.png)
</details>

17. Проведите повторную сборку мастера, убедитесь, что сбора прошла успешно и артефакты собраны<
18. Проверьте, что конфигурация в репозитории содержит все настройки конфигурации из teamcity
19. В ответ предоставьте ссылку на репозиторий

https://github.com/AlexeyKhrapov/example-teamcity