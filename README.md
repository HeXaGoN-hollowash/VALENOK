================================================================================
🚀 VALENOK Video Converter & Clipper v1.0.1 🚀
================================================================================
Author: .HeXaGoN. / hollowash
Studio: Hex Wasteland Project
License: MIT (Open Source & Free Software)
Core Engine: Powered by FFmpeg (https://ffmpeg.org)
Format: Portable (No installation required, single standalone file)

================================================================================
📋 CONVERSION MODES (PRESETS) OVERVIEW:
================================================================================
🔗 Clip Stitching   - Merges multiple selected video files into one monolithic video.
🚀 YouTube/Standard - Fast video clipping without quality loss, optimized for standard players.
🔥 Shorts/TikTok    - Cuts and automatically reformats videos into vertical aspect ratios.
🖼️ GIF Mode         - Converts the selected video segment into a high-quality animation.
🎛️ Expert Mode      - Maximum control: custom video codecs, bitrate, and render up to 2K.
                      Also features a separate panel to merge a specific audio track 
                      with video or extract audio completely.
⚙️ Custom Bitrate   - Compress file size or preserve maximum possible video quality.
👾 Discord Mode     - Compresses video quality to fit the 20 MB Discord upload limit. 
                      Recommended for 1920x1080 videos with a duration of up to 30 seconds.
                      If the duration is longer, the output file will 100% exceed the Discord limit.

================================================================================
⚠️ IMPORTANT FEATURES AND USAGE RULES:
================================================================================
1. Smart Timestamp Protection:
   The app automatically validates clipping timestamps before starting the render. 
   If the START time is greater than or equal to the END time, the software blocks 
   the process and shows a warning. Time inputs are totally ignored ONLY in 
   the Clip Stitching mode (🔗).

2. Empty File Cleanup:
   If FFmpeg outputs a corrupted empty file (0 KB) due to incorrect timecodes or 
   system errors, the app automatically deletes it, frees up disk space, and 
   displays an error window.

3. GIF Creation Specifics:
   The default animation preset is optimized for standard HD videos (1280x720) 
   and forces a center crop. If your source video has a different resolution 
   (e.g., 1920x1080) and you want to capture the ENTIRE frame without automatic 
   cropping, pre-convert your video to 720p or use the advanced 🎛️ Expert Mode.

4. GPU Selection (Hardware Acceleration):
   You can select your GPU (NVIDIA / AMD) in the settings to speed up heavy rendering.
   Note: Intel graphics cards are NOT supported. If you have integrated Intel UHD 
   graphics or an older PC, use the default CPU (Any PC) mode.

5. Pure Portability:
   The program is a 100% monolithic standalone .exe file. The configuration file 
   (language, hardware settings) is automatically and silently saved to the user's 
   system AppData folder. No junk files or configs are generated next to the app.

6. Corrupted/VFR Files Warning (ShadowPlay):
   The encoder requires a stable, standard video stream. If you try to process 
   corrupted files or gameplay clips recorded via Nvidia ShadowPlay with 
   Variable Frame Rate (VFR), FFmpeg may throw a "Corrupt frame detected" error. 
   👉 NOTE: If the rendering process gets stuck on a broken file, click on the opened CONSOLE (TERMINAL)
   window and press CTRL + C to force stop it.
   For flawless rendering, it is highly recommended to record clips via OBS Studio 
   with Constant Framerate (CFR) or pre-convert broken files via HandBrake.


================================================================================
🎧 AUDIO ACCOMPANIMENT:
================================================================================
🔊 ready.wav - Victory sound effect played upon successful render completion.
🔊 error.wav - Played during critical errors or when empty files are detected.


Thank you for using VALENOK! Enjoy and save your time! 🦾

================================================================================
================================================================================
РУССКАЯ ВЕРСИЯ / RUSSIAN VERSION
================================================================================
================================================================================
Автор: .HeXaGoN. / hollowash
Студия: Hex Wasteland Project
Лицензия: MIT (Открытый и бесплатный софт)
Основной движок: Работает на базе FFmpeg (https://ffmpeg.org)
Формат: Portable (Работает без установки, один файл)
================================================================================
📋 ОБЗОР РЕЖИМОВ (ПРЕСЕТОВ):
================================================================================
🔗 Сшивание клипов - Склеивает несколько выбранных видео в один монолитный файл.
🚀 YouTube/Стандарт - Быстрая обрезка видео без потери качества под стандартный плеер.
🔥 Shorts/TikTok    - Нарезка вертикальных видео с автоматическим изменением формата.
🖼️ Режим GIF       - Конвертация выбранного куска видео в качественную анимацию.
🎛️ Эксперт-режим   - Максимальный контроль: кастомные кодеки видео, битрейт и рендер вплоть до 2K.
                     Также есть возможность склеивать 1 конкретную аудиодорожку с видео или вырезать звук. (Имеет отдельную панель)
⚙️ Кастом:Битрейт  - Ужатие или сохранение максимального качества видео.
👾 Discord режим    - Ужимает видео по качеству до лимита Discord в 20 Мб. Рекомендуется использовать видео разрешением 1920x1080, длительностью до 30 секунд.
                     Если длительность будет выше, выйдет файл 100% не по лимиту Discord.

================================================================================
⚠️ ВАЖНЫЕ ОСОБЕННОСТИ И ПРАВИЛА ИСПОЛЬЗОВАНИЯ:
================================================================================
1. Умная защита таймингов:
   Программа автоматически проверяет время обрезки перед запуском рендера. 
   Если время НАЧАЛА больше или равно времени КОНЦА, софт заблокирует запуск 
   и выдаст предупреждение. Поля ввода времени тотально игнорируются только 
   в режиме Сшивания клипов (🔗).

2. Зачистка пустых файлов:
   Если из-за кривых таймкодов или сбоя системы FFmpeg выдаст повреждённый 
   пустой файл (0 КБ), программа автоматически удалит его, очистит диск 
   и выдаст понятное окно с ошибкой.

3. Нюанс при создании GIF (картинок):
   Дефолтный пресет анимации оптимизирован под ролики стандартного HD-разрешения 
   (1280x720) и принудительно делает кроп по центру. Если ваше исходное видео 
   имеет другое разрешение (например, 1920x1080) и вы хотите запечатлеть ВЕСЬ 
   кадр целиком без автоматической обрезки — предварительно переведите видео 
   в формат 720p или воспользуйтесь тонкой настройкой в 🎛️ Эксперт-режиме.

4. Выбор видеокарты (Аппаратное ускорение):
   В настройках программы доступен выбор графического процессора (NVIDIA / AMD) 
   для рендера тяжелых пресетов. Видеокарты Intel НЕ поддерживаются. Если у вас 
   встроенная графика Intel или старый ПК, используйте стандартный режим CPU (Any PC).

5. Полная автономность и чистота:
   Программа является 100% монолитным .exe файлом. Файл конфигурации (язык, 
   настройки железа) автоматически и скрытно сохраняется в системную папку 
   AppData пользователя. Рядом с программой не плодится никакой мусор.

6. Предупреждение о битых и VFR файлах (Nvidia ShadowPlay):
   Движок программы требует стабильного и технически правильного видеопотока. 
   Если скормить конвертеру повреждённые файлы или клипы "Мгновенного повтора" 
   Nvidia ShadowPlay с переменной частотой кадров (VFR), FFmpeg может выдать ошибку 
   "Corrupt frame detected" и прервать рендер. 
 👉 ПРИМЕЧАНИЕ: Если процесс рендера намертво завис на битом файле — кликните по открывшемуся окну
    КОНСОЛИ (ТЕРМИНАЛА) и нажмите CTRL + C для принудительной остановки.
   Для идеальной работы рекомендуется записывать повторы через OBS Studio с постоянной 
   частотой кадров (CFR) либо предварительно лечить побитые файлы через программу HandBrake.

================================================================================
🎧 ЗВУКОВОЕ СОПРОВОЖДЕНИЕ:
================================================================================
🔊 ready.wav — Победный звуковой сигнал об успешном окончании рендера.
🔊 error.wav — Воспроизводится при критических ошибках или пустых файлах.

Спасибо, что используете VALENOK! Пользуйтесь на здоровье и экономьте время! 🦾
