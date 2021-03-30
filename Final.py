from lxml import etree  # Импортируем библиотеку для валидации XML и XSD файла.
import xml.etree.ElementTree as ET  # Импортируем библиотеку для работы с XML файлом после валидации.
import logging  # Импортируем библиотеку для ведения логов
import os  # Импортируем библиотеку для работы с файловой системой
import shutil  # Импортируем библиотеку для работы с файловой системой


logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)  # Cоздаем файл, куда будем писать лог.


def xml_xsd_validation():
    """Данная функция проверяет структуру XML файла, структуру XSD схемы и далее проверяет
    данный XML файл на соответствие схеме. Если все прошло успешно, то возвращает True, иначе - False"""
    # Проверяем конфигурационный (XML) файл
    try:
        xml_filename = 'config.xml'
        with open(xml_filename) as f:
            xml = etree.parse(f)
    except:
        logging.error('XML файл не прошел парсинг. Работа скрипта завершена.')
        return False
    # Проверяем XSD
    try:
        xsd_file_name = 'schema.xsd'
        with open(xsd_file_name) as s:
            schema_root = etree.parse(s)
            schema = etree.XMLSchema(schema_root)
    except:
        logging.error('XSD схема не прошла парсинг. Работа скрипта завершена.')
        return False
    # Сравниваем XML на соответствие XSD:
    if schema.validate(xml) is True:
        logging.debug('XML файл прошел валидацию по XSD схеме.')
    else:
        logging.error('XML файл не прошел валидацию по XSD схеме. Работа скрипта завершена')
        return False
    return True


def permit_exist_check(dirfile):

    """Данная функция проверяет проверяет права чтения/записи в исходной и целевой директориях.
     Если целевая директория отсутствует, то она создается.
     Параметр dirfile - корневой элемент <file> файла config.xml
     Функция возвращает True, если копирование файла по указанному пути возомжно,
     в противном случае функция возвращает False"""

    source = dirfile[0].text
    destination = dirfile[1].text
    filename = dirfile[2].text
    file_to_copy = source + '/' + filename

    # Проверяем существование файла в исходной директории
    if os.access(file_to_copy, os.F_OK) is True:
        logging.debug(f'Файл {file_to_copy} найден.')
        pass
    else:
        logging.warning(f'Файл {file_to_copy} не найден. Копирование невозможно.')
        return False

    # Проверяем наличие прав на чтение файла  в исходной директории
    if os.access(file_to_copy, os.R_OK) is True:
        logging.debug(f'Файл {file_to_copy} доступен для чтения.')
        pass
    else:
        logging.warning(f'Файл {file_to_copy} недоступен для чтения. Обратитесь к администратору.')
        return False

    # Проверяем существование целевой директории
    if os.access(destination, os.F_OK) is True:
        logging.debug(f'Директория {destination} для копирования найдена.')
        # Проверяем права на запись в целевую директорию
        if os.access(destination, os.W_OK) is True:
            pass
        else:
            logging.warning(f'Права записи в директорию {destination} отсутствуют.')
            return False
    else:
        # Если директории нет, то ее нужно создать
        logging.warning(f'Директория {destination} не существует или отсутствуют права на чтение/запись.')
        logging.debug(f'Пытаемся создать директорию {destination} для копирования....')
        try:
            os.makedirs(destination)
        except:
            logging.warning(f'Не удалось создать директорию {destination}. Копирование прервано.')
            return False
        logging.debug(f'Директория {destination} создана.')
    return True


def copy_file(dirfile):
    """Данная функция копирует файл из исходной директории в целевую директорию
    Параметр dirfile - корневой элемент <file> файла config.xml"""
    source = dirfile[0].text
    destination = dirfile[1].text
    filename = dirfile[2].text
    file_to_copy = source + '/' + filename
    try:
        shutil.copy(file_to_copy, destination)
    except:
        logging.error('При копировании файла что-то пошло не так...')
    logging.info(f'Файл {file_to_copy} успешно скопирован из {source} в {destination}')


def final_script():
    """Данная функция запускает:
    1. Функцию xml_xsd_validation() - для проверки XML и XSD, а также соответствия XML схеме XSD.
    2. Парсит файл config.xml для дальнейшего доступа к его элементам.
    3. Для каждого элемента <file> из файла XML запускает функции:
        3.1 permit_exist_check() - для проверки прав чтения/записи в исходной и целевой директориях
        3.2 copy_file() - для копирования файла из исходной в целевую директорию
    """
    if xml_xsd_validation() is True:
        # Получаем корневой элемент для дальнейшей работы
        tree = ET.parse('config.xml')  # Парсим XML файл
        root = tree.getroot()  # Получаем корневой элемент
        for dirfile in root:
            if permit_exist_check(dirfile) is True:
                copy_file(dirfile)
            else:
                continue
    else:
        return False


final_script()
