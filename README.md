# Предустановка    
`python -m pip install -r requirements.txt`
# Задание 1. Скрипты для обновления фида    
Скрипт `feed_update.py`, создает директорию feed_update_data в ней сохраняется файл источника, а также обновленный целевой файл.    
Файлы скачиваются с помощью requests, обработка происходит с помощью xml. Обновление происходит итеративно чанками по 50 товаров из исходного файла.     
Пример использования: `python feed_update.py`

# Задание 2. Обработка изображений
Используется Pillow. Исходное изображение плашки вручную обрезал для более удобной работы.    
****Важно***: работа с исходными и результирующими файлами ведется в папке `image_processing_data`*.     
На вход подаем название исходного файла, плашки и желаемого названия файла с результатом).     
Пример использования: `python image_processing.py img.jpg plashka.png result.png`    
