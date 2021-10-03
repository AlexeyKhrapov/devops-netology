# Домашнее задание к занятию «2.4. Инструменты Git»  — Алексей Храпов
> Найдите полный хеш и комментарий коммита, хеш которого начинается на aefea.

Для получения полного хеша коммита и его комментария воспользовался командой `git log aefea --pretty=format:'%H %s'`
хеш: `aefead2207ef7e2aa5dc81a34aedf0cad4c32545`
Комментарий: `Update CHANGELOG.md`
Также можно было воспользоваться командами `git log aefea` и `git show aefea`, но их вывод избыточен для выполнения поставленной задачи.

> Какому тегу соответствует коммит 85024d3?

Для проверки воспользовался командой `git show 85024d3 -s`
```
admin@LP-AHR:/mnt/c/Users/ahr/studing/terraform$  git show 85024d3 -s
commit 85024d3100126de36331c6982bfaac02cdab9e76 (tag: v0.12.23)
Author: tf-release-bot <terraform@hashicorp.com>
Date:   Thu Mar 5 20:56:10 2020 +0000

    v0.12.23
```
Из вывода видно, что коммит соответствует тэгу v0.12.23
	
> Сколько родителей у коммита b8d720? Напишите их хеши.

Для выполнения использовал команду `git log b8d720`
Получил вывод команды:
```
commit b8d720f8340221f2146e4e4870bf2ee0bc48f2d5
Merge: 56cd7859e 9ea88f22f
Author: Chris Griggs <cgriggs@hashicorp.com>
Date:   Tue Jan 21 17:45:48 2020 -0800

    Merge pull request #23916 from hashicorp/cgriggs01-stable

    [Cherrypick] community links
```
Из вывода видим, что у этого коммита 2 родителя.
Для получения хеша первого родителя воспользовался командой `git show b8d720^1 --pretty=format:'%H' -s`, таким образом хеш первого родителя:
`56cd7859e05c36c06b56d013b55a252d0bb7e158`
Аналогично получил хеш второго родителя путем ввода команды `git show b8d720^2 --pretty=format:'%H' -s`:
`9ea88f22fc6269854151c571162c5bcf958bee2b`	

> Перечислите хеши и комментарии всех коммитов которые были сделаны между тегами v0.12.23 и v0.12.24.

Для получения всех коммитов между вышеуказанными тегами воспользовался командой `git log v0.12.23..v0.12.24 --pretty=format:'%H %s'`
```
admin@LP-AHR:/mnt/c/Users/ahr/studing/terraform$ git log v0.12.23..v0.12.24 --pretty=format:'%H %s'
33ff1c03bb960b332be3af2e333462dde88b279e v0.12.24
b14b74c4939dcab573326f4e3ee2a62e23e12f89 [Website] vmc provider links
3f235065b9347a758efadc92295b540ee0a5e26e Update CHANGELOG.md
6ae64e247b332925b872447e9ce869657281c2bf registry: Fix panic when server is unreachable
5c619ca1baf2e21a155fcdb4c264cc9e24a2a353 website: Remove links to the getting started guide's old location
06275647e2b53d97d4f0a19a0fec11f6d69820b5 Update CHANGELOG.md
d5f9411f5108260320064349b757f55c09bc4b80 command: Fix bug when using terraform login on Windows
4b6d06cc5dcb78af637bbb19c198faff37a066ed Update CHANGELOG.md
dd01a35078f040ca984cdd349f18d0b67e486c35 Update CHANGELOG.md
225466bc3e5f35baa5d07197bbc079345b77525e Cleanup after v0.12.23 release
```

> Найдите коммит в котором была создана функция func providerSource, ее определение в коде выглядит так func providerSource(...) (вместо троеточего перечислены аргументы).

Для нахождения первого коммита с указанной функцией восользовался командой `git log -S'func providerSource' --pretty=format:'%H %aD %s'`
```
git log -S'func providerSource' --pretty=format:'%H %aD %s'
5af1e6234ab6da412fb8637393c5a17a1b293663 Tue, 21 Apr 2020 16:28:59 -0700 main: Honor explicit provider_installation CLI config when presen
t
8c928e83589d90a031f811fae52a81be7153e82f Thu, 2 Apr 2020 18:04:39 -0700 main: Consult local directories as potential mirrors of providers
```
Таким образом, коммит в котором была создана функция имеет хеш
`8c928e83589d90a031f811fae52a81be7153e82f`

Более детальную информацию можно получить путем поиска по содержимому файлов и последующим поиском с помощью `git log -L`
```
admin@LP-AHR:/mnt/c/Users/ahr/studing/terraform$ git grep -n 'func providerSource('
provider_source.go:23:func providerSource(configs []*cliconfig.ProviderInstallation, services *disco.Disco) (getproviders.Source, tfdiags.Diagnostics) {
admin@LP-AHR:/mnt/c/Users/ahr/studing/terraform$ git log -L '/func providerSource/',/^}/:provider_source.go --pretty=format:'%H %aD %s' -s
5af1e6234ab6da412fb8637393c5a17a1b293663 Tue, 21 Apr 2020 16:28:59 -0700 main: Honor explicit provider_installation CLI config when present
diff --git a/provider_source.go b/provider_source.go
--- a/provider_source.go
+++ b/provider_source.go
@@ -20,6 +23,14 @@
-func providerSource(services *disco.Disco) getproviders.Source {
-       // We're not yet using the CLI config here because we've not implemented
-       // yet the new configuration constructs to customize provider search
-       // locations. That'll come later. For now, we just always use the
-       // implicit default provider source.
-       return implicitProviderSource(services)
+func providerSource(configs []*cliconfig.ProviderInstallation, services *disco.Disco) (getproviders.Source, tfdiags.Diagnostics) {
+       if len(configs) == 0 {
+               // If there's no explicit installation configuration then we'll build
+               // up an implicit one with direct registry installation along with
+               // some automatically-selected local filesystem mirrors.
+               return implicitProviderSource(services), nil
+       }
+
+       // There should only be zero or one configurations, which is checked by
+       // the validation logic in the cliconfig package. Therefore we'll just
+       // ignore any additional configurations in here.
+       config := configs[0]
+       return explicitProviderSource(config, services)
+}

92d6a30bb4e8fbad0968a9915c6d90435a4a08f6 Wed, 15 Apr 2020 11:48:24 -0700 main: skip direct provider installation for providers available locally
diff --git a/provider_source.go b/provider_source.go
--- a/provider_source.go
+++ b/provider_source.go
@@ -19,5 +20,6 @@
 func providerSource(services *disco.Disco) getproviders.Source {
        // We're not yet using the CLI config here because we've not implemented
        // yet the new configuration constructs to customize provider search
-       // locations. That'll come later.
-       // For now, we have a fixed set of search directories:
+       // locations. That'll come later. For now, we just always use the
+       // implicit default provider source.
+       return implicitProviderSource(services)

8c928e83589d90a031f811fae52a81be7153e82f Thu, 2 Apr 2020 18:04:39 -0700 main: Consult local directories as potential mirrors of providers
diff --git a/provider_source.go b/provider_source.go
--- /dev/null
+++ b/provider_source.go
@@ -0,0 +19,5 @@
+func providerSource(services *disco.Disco) getproviders.Source {
+       // We're not yet using the CLI config here because we've not implemented
+       // yet the new configuration constructs to customize provider search
+       // locations. That'll come later.
+       // For now, we have a fixed set of search directories:
```

> Найдите все коммиты в которых была изменена функция globalPluginDirs.

Для начала установил в каких файлах была использована функция

```
 git grep --heading --break -n 'globalPluginDirs'
commands.go
88:             GlobalPluginDirs: globalPluginDirs(),
436:    helperPlugins := pluginDiscovery.FindPlugins("credentials", globalPluginDirs())

internal/command/cliconfig/config_unix.go
34:             // FIXME: homeDir gets called from globalPluginDirs during init, before

plugins.go
12:// globalPluginDirs returns directories that should be searched for
18:func globalPluginDirs() []string {
```
Далее поэтапно были проведены проверки с помощью `git log -L`
```
git log -L '/globalPluginDirs/',/^}/:commands.go | grep '^commit'
commit 65e0c448a0e38307d1a08e1af062f03c0d16a12d
commit 583859e510e44e31b4a0191d048e90cb4fbe8d0f
commit 7f783429536db18473c3299d2b516496d0b39e7e
commit 08b649b6f94928e7fb3fe729f00c21b60ec0a7c9
commit a60120477c0ebe37505e5ce00f28cb11edcf11eb
commit 83e6703bf77f60660db4465ef50d30c633f800f1
commit 5e089c2c093d8522a27004bd1ea988f48439e5d0
commit 0a596d2a12ea67ccf43ef25fe2418e92127d37b2
commit 6a44586a8f6b2a3e9298d7db076130482581732e
commit 9665901e8e247afe88b50560a2e484b6df5c5bcf
commit f44265e59e941f581859e91686b9a688bd1c876b
commit 39504ede052507574179c9e628eaf9abc51f0983
commit 30204ecded21fb52c992b0a707bb4cbb96e2c608
commit e270291f194043486bc6c46759308ffa8bdec239
commit 49e2e00231d04de4f2c3b8b21b3c6aecdac8f4f0
commit 5e2b11657e82b7a7e239ff695c68795d883a4b4e
commit 5127f1ef8b35fb9cd5f63a944d82b5d1ea800741
commit 7165d6c42955e278ad94f64aea69bb812a356816
commit 5f313a65ad5216e7d7df17e74a21b39bd41ba7c7
commit 3b0b29ef52687f36000ffdf878c54751195bfac2
commit 1b45b744c3debbbf2875feb25df81bb7390113c1
commit 081f02971dc649a6f6dc29bab127cd4f07026738
commit b75201acc23ec3d794367a2cb939d4ffeb5715fb
commit e9d0822b2a60f15653da0120607e74df1e116422
commit 131656a2372d858a061ca30fef78bdf419fe3707
commit 7ccd6204c4663014e9b2ba91dc0078ac879adfb4
commit 6bba3ceb4208c470f82b2985747329fbcabbc8f2
commit 16823f43deec42427a791f0e82b9b43e4b41fbc0
commit ffe5f7c4e60b8d759b1251ce81a2cb44c7190b8f
commit 618883596ad1ef7c9eb111b20195f0ac90bbd404
commit 179b32d426025f9cb94f57488634ee4e3d9699a3
commit 6884a07bbae0b4163a2d423249b056015086856a
commit 3da5fefdc125ae74bb707317b73a27e68999f67b
commit 865e61b4eabf1fa0d126b202d522a61484512ea0
commit cb17a9a607446da9bd62b951dc11095a4b110eca
commit 0fe43c8977a04a64c2dff43aa1c36f6ba0a39e21
commit 2e7c8ab76aafdf3e35073e46664fb86c88ff40a7
commit 9d7fce2f69123100afd43be27a110f8431fbb43b
commit 31d556894f63c630fddedad5e3a59d854d6febac
commit 3af0ecdf0131225ffccd20d2f2ea7632cf1e4b7c
commit 8364383c359a6b738a436d1b7745ccdce178df47
commit 9e9d0b1bdfafbb27e26da5f3f3f17c101200d388
commit 39a5ddd381fc5f80a798d822b3f11f2896136c90
commit b53704ed8747b4740dd0a876d2284c2f5fd0c9e5
commit c8526484b30b47694491664e331b8d5b5445d1b0
commit 31f033827f7d81e5fefcce96aa5af0adb4c30ce8
commit 65abe9804727e1fbc63a78c526d19e0b9bbecf45
commit 1492c578de1303fe56713622c56617d08b24183e
commit fef57279043d0e474448c9fb5d5ee6196a96ad32
commit b8adf102362ea9a133d373362f6ba58916b1b3c2
commit a867457d75ee30e70e27989bf8a1e4a024507653
commit 3fdc08a9eb0aa5ec68d2547e332e7677cb1f34ba
commit aa5dc453eef670e6bb6bee3c326cb850aa35d329
commit ff94381e7e5cdb47d99895df950302092b196f14
commit 6360e6c8b6ead22c46c32accdb785349b07a02a8
commit f6692e66ac4d5ec73975727ec007bd87c79753e8
commit d1b46e99bd75cbbed116234aa765145bde010a9b
commit fa703db8a6da35fb74782dc01cebda762c0a8c2c
commit cc41c7cfa03f05717374055e60c5761466e76e5e
commit c7f5450a964e0fa89a02303232972b4777e6ec63
commit db69a2959bdbb1ec8399282ff652867461de918e
commit cdde9149ff50425f0da5fee6ece40e87a60f6596
commit 01cd761023aa20d13eb080101733534d7811cfa0
commit b06a88d1aba69af84f3a5a7bf343b204fc47104d
commit b3871c0c5a29d6ec193584224b642d754a898d76
commit 38002904f4b16c8fd604833429c53ee8660b8a9d
commit 34df2175149cd27eedf4757e0322c1f9c87aaf8b
commit 70191d22a6c29bb2319c32936ce1f834e0b2d95c
commit f302e7d1bbfd460999a5c0ce59f01984f2cbb5a2
commit fe4f53eb5bf3ea7392ab227d46d3c2dd1082fa76
commit ed538a9594ee2d8d25caaf0630e62091c25955ca
commit 4e17aaf92766bea594382473a60f0c5eda81b350
commit dde0f0f8df3845b7d867ae9e0a61d6cdef3d6c77
commit 2caff709d66a8af421e1bd9e9d44dfd5a4383c54
commit 77bfa5657eba80d1d28b04fc3f3a95d9abd66579
commit dbc1c63d799c13393e48c7e07a194ab8a3702451
commit 0e8886705229c18d3bf5df22c406b140837b1cef
commit 5aa6ada589be17b0eaf77e92bfd3694f9bf67b10
commit 93fbb9ea8f17ecbb7799195011e6414654d93fef
commit 1819b6fb343ec35468c3f2394b13840264b690f2
commit 01319e1dc9f5bf7b9ac053e447f4b06a6743dff3
commit bff4b8a58c78875369406316063e3e10ae82ba6e
commit 8aa99687c36ecc5c173a5acb4a53be3a2123953f
commit 6c6bc0ae3e4fb92ff58394d2fbdca5cfd4a12426
commit 046e80361bff2ba8184a71a22fcef849abbd22fb
commit a4a4e3784dd07bc1f53387dadd5c74c3180a49bf
```
```
git log -L '/globalPluginDirs/',/^}/:internal/command/cliconfig/config_unix.go | grep '^commit'
commit 49ee3d3ef8f398fbf1a9c496f6c61466b03250e9
commit e4b0a989f353a0e9bbca45331c8ae3f9fd69dc50
commit c0b17610965450a89598da491ce9b6b5cbd6393f
commit 8173cd25bb69b4f0be7bf1a15105d5b1d0c08860
commit d3a609ac52dc699ba14bcb552279666d5dd9c24a
```
```
git log -L '/globalPluginDirs/',/^}/:plugins.go | grep '^commit'
commit 78b12205587fe839f10d946ea3fdc06719decb05
commit 52dbf94834cb970b510f2fba853a5b49ad9b1a46
commit 41ab0aef7a0fe030e84018973a64135b11abcd70
commit 66ebff90cdfaa6938f26f908c7ebad8d547fea17
commit 8364383c359a6b738a436d1b7745ccdce178df47
```
>Кто автор функции synchronizedWriters?

Т.к. поиск функции в файлах не дал результатов, то выполнялся поиск по совпадению строки в коммитах:
```
git log -S'synchronizedWriters' --pretty=format:'%H %an %ae %aD %s'
bdfea50cc85161dea41be0fe3381fd98731ff786 James Bardin j.bardin@gmail.com Mon, 30 Nov 2020 18:02:04 -0500 remove unused
fd4f7eb0b935e5a838810564fd549afe710ae19a James Bardin j.bardin@gmail.com Wed, 21 Oct 2020 13:06:23 -0400 remove prefixed io
5ac311e2a91e381e2f52234668b49ba670aa0fe5 Martin Atkins mart@degeneration.co.uk Wed, 3 May 2017 16:25:41 -0700 main: synchronize writes to
VT100-faker on Windows
```
Таким образом стало понятно, что `Martin Atkins` в коммите с хешем  `5ac311e2a91e381e2f52234668b49ba670aa0fe5` создал эту функцию, а `James Bardin` в коммите с хешем ` bdfea50cc85161dea41be0fe3381fd98731ff786` её удалил, т.к. она больше не использовалась.

