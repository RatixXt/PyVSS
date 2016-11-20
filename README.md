# PyVSS
Repository for course project about using Microsoft Volume Snapshot Service, Shadow Copy.
<h2>vss_functions</h2>
Библиотека с функциями взаимодействующими с VSS через WMI. Доступны следующие функции:
<h3> Внешние функции </h3>
<ul>
<li>List_shadows() - выводит параметры всех существующих объектов теневых копий в консоль</li>
<li>get_shadow_paths() - получает обычный путь к файлу и возвращает список возможных эквивалентных теневых путей к файлу</li>
<li>unshadow_path() - превращает теневой путь в обычный</li>
<li>get_last_shadow_path() - возвращает последнюю теневую копию из списка теневых копий.</li>
<li>open_shadow() - позволяет открыть теневой файл как обычный.</li>
<li>copy_shadow_as_file() - позволяет скопировать файл из теневой копии.</li>
<li>vss_create() - создает теневую копию указанного тома.</li>
<li>vss_delete() - удаляет теневую копию по id.</li>
</ul>
<h3> Служебные функции, используемые внутри библиотеки </h3>
<ul>
<li> WMIDateStringToDate() - переводит дату из WMI строки в нормальный формат.</li>
<li> get_shadows_objects() - получает объекты теневых копий, используется для получения теневых путей.</li>
</ul>
<h2>Vss_admin.py</h2>
<h3>Описание скрипта</h3>
Скрипт, предназначенный для получения информации о теневых копиях и создания/удаления теневых копий.
<h3>Работа со скриптом</h3>
Скрипт использует следующие параметры запуска:
<ul>
<li>--h: Выводит сообщение с описанием утилиты и инструкцией по возможным параметрам. </li>
<li>--LS, -List_shadows: Отображает все теневые копии и их атрибуты. </li>
<li>--С, -Сreate_shadow: Создает теневую копию тома, используется совместно с параметром –D для указания тома. </li>
<li>--DS, -Delete_shadow: Удаляет теневую копию тома, используется совместно с параметром –id для указания id теневой копии. </li>
<li>--D: После указания этого параметра вводится буква диска, для которого будет создаваться теневая копия. </li>
<li>--id: После указания этого параметра вводится id теневой копии. </li>
</ul>
<h2>Hash_owner.py</h2>
<h3>Описание скрипта</h3>
Скрипт, позволяющий скопировать файлы SAM и SYSTEM из теневой копии в директорию указанную пользователем.
<h3>Работа со скриптом</h3>
Скрипт использует следующие параметры запуска:
<ul>
<li>Обязательный параметр для запуска указывающий директорию в которую будут помещены файлы SAM и SYSTEM, вводится без ключа. </li>
<li>--h: Выводит сообщение с описанием утилиты и инструкцией по возможным параметрам. </li>
</ul>
<h2>Vss_explorer.py</h2>
<h3>Описание скрипта</h3>
Vss_explorer предоставляет консольный интерфейс для просмотра теневых копий тома и возможности по работе с ее содержанием, а также позволяет подключить теневую копию к системе в виде каталога местоположение которого задает пользователь. 
<h3>Работа со скриптом</h3>
Скрипт использует следующие параметры запуска:
<ul>
<li>Обязательный параметр определяющий букву диска с которым будет работать скрипт, задается без ключа. </li>
<li>--h: Выводит сообщение с описанием утилиты и инструкцией по возможным параметрам. </li>
<li>--E, --Explorer: Выполняет вход в режим консольного просмотра последней теневой копии диска, в этом режиме доступны команды: </li>
<ul>
<li>help — вывести информацию о доступных командах </li>
<li>cd DIRECTORY— перемещение в поддиректорию DIRECTORY, если вместо DIRECTORY указано «..», то перемещение в родительскую директорию. </li>
<li>copy FILE_NAME OUTPUT_PATH — копирование файла из теневой копии в OUTPUT_PATH </li>
<li>ls — вывести содержимое текущей директории </li>
<li>stat FILE_NAME— возвращает статус файла </li>
<li>open — вывести содержимое файла в консоль в бинарном формате. </li>
</ul>
<li>--CL, --Create_link: создает символьные ссылки на все теневые копии диска, символьные ссылки помещаются в директорию указываемую параметром –О </li>
<li>--О: задает директорию в которую будут помещены символьные ссылки. </li>
</ul>