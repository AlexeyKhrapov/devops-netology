# 7.6. Написание собственных провайдеров для Terraform — Алексей Храпов

## Задача 1. 
Давайте потренируемся читать исходный код AWS провайдера, который можно склонировать от сюда: 
[https://github.com/hashicorp/terraform-provider-aws.git](https://github.com/hashicorp/terraform-provider-aws.git).
Просто найдите нужные ресурсы в исходном коде и ответы на вопросы станут понятны.  


1. Найдите, где перечислены все доступные `resource` и `data_source`, приложите ссылку на эти строки в коде на 
гитхабе.   
1. Для создания очереди сообщений SQS используется ресурс `aws_sqs_queue` у которого есть параметр `name`. 
    * С каким другим параметром конфликтует `name`? Приложите строчку кода, в которой это указано.
    * Какая максимальная длина имени? 
    * Какому регулярному выражению должно подчиняться имя? 

### Ответ:

> 1. Найдите, где перечислены все доступные `resource` и `data_source`, приложите ссылку на эти строки в коде на 
гитхабе.

- [recource](https://github.com/hashicorp/terraform-provider-aws/blob/8b5a71bcdcaa04e6d5c5c41243fd981edbdd79a5/internal/provider/provider.go#L872-L1999)
- [data_source](https://github.com/hashicorp/terraform-provider-aws/blob/8b5a71bcdcaa04e6d5c5c41243fd981edbdd79a5/internal/provider/provider.go#L412-L870)

> 2. Для создания очереди сообщений SQS используется ресурс `aws_sqs_queue` у которого есть параметр `name`.  
> * С каким другим параметром конфликтует `name`? Приложите строчку кода, в которой это указано.

`name` конфликтует с `name_prefix`:

https://github.com/hashicorp/terraform-provider-aws/blob/db1ab4cfcb7ca407398753b158037c4e94472c6b/internal/service/sqs/queue.go#L82-L94

> * Какая максимальная длина имени? 

Исходя [из кода функции](https://github.com/hashicorp/terraform-provider-aws/blob/8b5a71bcdcaa04e6d5c5c41243fd981edbdd79a5/internal/service/sqs/queue.go#L407-L433), максимальная длина имени - 80 символов:
```gotemplate
func resourceQueueCustomizeDiff(_ context.Context, diff *schema.ResourceDiff, meta interface{}) error {
	fifoQueue := diff.Get("fifo_queue").(bool)
	contentBasedDeduplication := diff.Get("content_based_deduplication").(bool)

	if diff.Id() == "" {
		// Create.

		var name string

		if fifoQueue {
			name = create.NameWithSuffix(diff.Get("name").(string), diff.Get("name_prefix").(string), FIFOQueueNameSuffix)
		} else {
			name = create.Name(diff.Get("name").(string), diff.Get("name_prefix").(string))
		}

		var re *regexp.Regexp

		if fifoQueue {
			re = regexp.MustCompile(`^[a-zA-Z0-9_-]{1,75}\.fifo$`)
		} else {
			re = regexp.MustCompile(`^[a-zA-Z0-9_-]{1,80}$`)
		}

		if !re.MatchString(name) {
			return fmt.Errorf("invalid queue name: %s", name)
		}
	}
```

> * Какому регулярному выражению должно подчиняться имя?

Как видно из выше представленного кода, имя подчиняется следующим регулярным выражениям, в зависимости от того указано расширение или нет:
```gotemplate
if fifoQueue {
			re = regexp.MustCompile(`^[a-zA-Z0-9_-]{1,75}\.fifo$`)
		} else {
			re = regexp.MustCompile(`^[a-zA-Z0-9_-]{1,80}$`)
		}
```
