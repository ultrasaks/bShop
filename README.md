bShop — магазин приложений, написанный на pyQT с клиентской стороны и PHP с серверной. 
Приложение выполнено в стиле material. В светлой теме элементы парят в воздухе, в тёмной — светятся.


### Возможности
* Имеется система аккаунтов, благодаря которой
* В магазине присутствует поиск, благодаря которому Вы можете найти любое нужное вам приложение.

### Использованные библиотеки
* PyQT5
* qt-material

### Системные требования
* Не менее 150мб свободного места на жёстком диске
* Python версии 3.7 и выше

### Сборка
1. Установить Python версии 3.7 и выше
2. Установить рip
3. Через pip установить библиотеки PyQT5, qt-material и pyinstaller
4. Через командную строку скомпилировать проект командой `pyinstaller --windowed --onedir --add-data "[путь до папки]bShop/icons;icons/" "[путь до папки]bShop/mainpage.py"`
