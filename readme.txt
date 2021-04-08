Здравствуйте. В качестве тестового задания я решил выбрать для себя Задачу #1:
_____________________________________________________________________________________________________________________
Задача 1
Реализовать программу, осуществляющую копирование файлов в соответствии с конфигурационным файлом.
Конфигурационный файл должен иметь формат xml. Для каждого файла в конфигурационном файле должно быть указано его имя,
исходный путь и путь, по которому файл требуется скопировать.

Пример
Конфигурационный файл:

<config>
    <file
            source_path="C:\Windows\system32"
            destination_path="C:\Program files"
            file_name="kernel32.dll"
    />
    <file
            source_path="/var/log"
            destination_path="/etc"
            file_name="server.log"
    />
</config>
____________________________________________________________________________________________________________________
1. Так как конфигурационный файл был дан как пример и содержал ошибки, то я решил что мой скрпит будет принимать на вход конфигурационный
файл следующего формата (файл config.xml):

<config>

    <file>
	<source_path>C:\Windows\system32</source_path>
	<destination_path>C:/Users/KimAlex/Desktop/OS_shutilcheck</destination_path>
	<file_name>kernel+100500.dll</file_name>
	</file>

	<file>
	<source_path>C:\Windows\system32</source_path>
	<destination_path>C:/Users/KimAlex/Desktop/OS_shutilcheck/funnydog</destination_path>
	<file_name>kernel32.dll</file_name>
	</file>
	
	<file>
	<source_path>/var/log</source_path>
	<destination_path>/etc</destination_path>
	<file_name>server.log</file_name>
	</file>

</config>

2. Для проверки структуры конфигурационного файла я сгенерировал XSD схему на сайте https://www.freeformatter.com/xsd-generator.html.
Далее в скрипте конфигурационный файл(config.xml) проверяется на соответствие этой схеме(schema.xsd).

3. Для запуска скрипта нужно вызвать функцию final_script() в модуле Final.py.

4. В результате запуска скрпита происходит копирование файлов и формируется лог(example.log).

Вот так вот!

5. Скрипт проверен на Windows 10 64bit и Ubuntu Linux 20.04.2 LTS 64bit.


