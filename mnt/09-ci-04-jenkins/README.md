# 09.04 Jenkins — Алексей Храпов

## Основная часть

1. Сделать Freestyle Job, который будет запускать `molecule test` из любого вашего репозитория с ролью.

<details><summary>Результат выполнения</summary>

![](./src/screenshot/task1-1.png)
![](./src/screenshot/task1-2.png)
![](./src/screenshot/task1-3.png)
![](./src/screenshot/task1-4.png)

</details>

2. Сделать Declarative Pipeline Job, который будет запускать `molecule test` из любого вашего репозитория с ролью.

<details><summary>Результат выполнения</summary>

![](./src/screenshot/task2-1.png)
![](./src/screenshot/task2-2.png)
![](./src/screenshot/task2-3.png)

</details>

3. Перенести Declarative Pipeline в репозиторий в файл `Jenkinsfile`.

- [Jenkinsfile](https://github.com/AlexeyKhrapov/vector-role/blob/main/Jenkinsfile)

4. Создать Multibranch Pipeline на запуск `Jenkinsfile` из репозитория.

<details><summary>Результат выполнения</summary>

![](./src/screenshot/task4-1.png)
![](./src/screenshot/task4-2.png)
![](./src/screenshot/task4-3.png)
![](./src/screenshot/task4-4.png)
![](./src/screenshot/task4-5.png)

</details>

5. Создать Scripted Pipeline, наполнить его скриптом из [pipeline](./pipeline).
6. Внести необходимые изменения, чтобы Pipeline запускал `ansible-playbook` без флагов `--check --diff`, если не установлен параметр при запуске джобы (prod_run = True), по умолчанию параметр имеет значение False и запускает прогон с флагами `--check --diff`.
7. Проверить работоспособность, исправить ошибки, исправленный Pipeline вложить в репозиторий в файл `ScriptedJenkinsfile`.

<details><summary>Результат выполнения</summary>

![](./src/screenshot/task6-1.png)
![](./src/screenshot/task6-3.png)
![](./src/screenshot/task6-2.png)


</details>

8. Отправить ссылку на репозиторий с ролью и Declarative Pipeline и Scripted Pipeline.

- [Jenkinsfile](https://github.com/AlexeyKhrapov/vector-role/blob/main/Jenkinsfile)
- [ScriptedJenkinsfile](./src/files/ScriptedJenkinsfile)
