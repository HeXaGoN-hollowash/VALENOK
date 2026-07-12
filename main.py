import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import subprocess  # Эта штука нужна, чтобы запускать FFmpeg
import os
import sys
import json
import winsound
import webbrowser

def resource_path(relative_path):
    """ Функция для поиска внутренних ресурсов при компиляции в единый EXE """
    try:
        import sys
        # PyInstaller создает временную папку _MEIPASS при запуске монолитного EXE
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Жёстко переключаем рабочую папку всей программы на временную папку распаковки EXE!
if hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

# --- ИНТЕРФЕЙС ОKНА ---
root = tk.Tk()
root.title("VALENOK Video Converter v1.1 (Explorer fix)")
root.geometry("550x440")

# === ГЛОБАЛЬНЫЙ СЛОВАРЬ ЛОКАЛИЗАЦИИ ВЕРСИИ 1.0 GLOBAL ===
LANG_DICT = {
    "ru": {
        "lbl_frame_expert": " ⚙️ Расширенные параметры",
        "lbl_select_mode": "Выбери режим ковертации:",
        "btn_render_discord": "👾СЖАТЬ ПОД DISCORD",
        "btn_render_youtube": "🚀РЕНДЕР ДЛЯ YOUTUBE",
        "btn_render_shorts": "🔥РЕНДЕР ДЛЯ SHORTS",
        "btn_render_custom": "⚙️СЖАТЬ ПО БИТРЕЙТУ",
        "btn_render_concat": "🔗НАЧАТЬ СКЛЕЙКУ КЛИПОВ",
        "btn_render_animation": "🖼️СОЗДАТЬ GIF-АНИМАЦИЮ",
        "btn_render_expert": "💾ЗАПУСТИТЬ ЭКСПЕРТНЫЙ РЕНДЕР",
        "btn_music_select": "🎵 Выбрать фоновую музыку",
        "btn_music_ready": "🎵 Музыка: ",
        "lbl_slider_quality_shorts": "⚙️ Настройка Shorts (Меньше значение = Шире обзор / Больше значение = Крупный план):",
        "lbl_slider_quality_custom": "⚙️ Выбери битрейт (Качество Мбит):",
        "lbl_slider_quality_expert": "⚙️ Выбери CRF (Меньше значение = Лучше картинка):",
        "chk_2k": "🚀 Апскейл / Рендер в 2K (1440p) для кодека VP09",
        "msg_ready_title": "Успех!",
        "msg_ready_text": "Видео готово и лежит тут:\n",
        "msg_error_title": "Ошибка",
        "msg_error_empty_video": "Сначала выбери видео файл!",
        "msg_error_general": "Что-то пошло не так. Проверь логи в VS Code.\n\n",
        "fd_video_title": "Выбери исходное видео",
        "fd_video_types": "Видео файлы",
        "fd_save_title": "Куда сохранить готовый файл?",
        "fd_music_title": "Выбери фоновую музыку",
        "fd_music_types": "Аудио файлы",
        "fd_concat_title": "Выбери пачку клипов для мгновенной склейки",
        "lbl_concat_ready": "✅ К склейке готово клипов: ",
        "lbl_settings_hw": "Выбери видеокарту/процессор для рендера:",
        "lbl_about_title": "VALENOK Видео Конвертер v1.1",
        "btn_about_boosty": "◈ ПОДДЕРЖАТЬ АВТОРА НА BOOSTY ◈",
        "btn_about_close": "❌ ЗАКРЫТЬ",
        "fd_all_types": "Все файлы",
        "lbl_src_file": "Исходный файл:",
        "lbl_dest_file": "Куда сохранить:",
        "lbl_timings": "Тайминги обрезки (если нужно):",
        "lbl_start": "Старт:",
        "lbl_end": "Конец:",
        "btn_browse": "Обзор...",
        "lbl_discord_warning": "⚠️ Желательно использовать клипы длительностью 20-30 сек!\nВидео длиннее будет иметь размер больше 20 Мб.",
        "chk_2k_full": "🚀 Апскейл / Рендер в 2K (1440p) для кодека VP09, от меньшего большему.",
        "lbl_exp_res": "Разрешение видео:",
        "lbl_exp_format": "Формат контейнера:",
        "lbl_exp_audio": "Режим звука:",
        "lbl_exp_stream": "Выбор аудиодорожки (Потока):",
        "menu_settings": "⚙️ Настройки",
        "menu_about": "❓ Справка",
        "lbl_concat_status_def": "⚠️ Внимание! Выберите сразу несколько файлов для сшивания.",
        "btn_choose_concat": "📂 ВЫБРАТЬ ПАЧКУ КЛИПОВ",
        "msg_concat_err_count": "Братан, для склейки нужно выбрать как минимум 2 клипа!",
        "msg_concat_err_path": "Выбери папку и имя для сохранения готового ролика!",
        "msg_concat_success": "Клипы мгновенно сшиты без потери качества!\nФайл сохранен: ",
        "msg_concat_fail": "Ошибка склейки. FFmpeg не смог сшить клипы.\nУбедись, что они записаны с одинаковыми настройками в OBS.",
        "license_text": (
            "Программа предоставляется БЕСПЛАТНО и 'КАК ЕСТЬ' (AS IS).\n"
            "Автор не несет ответственности за любые сбои вашего железа,\n"
            "сгоревшие чипы или материнские платы.\n"
            "Софт полностью чист, безопасен и собран вручную.\n"
            "Вы можете свободно делиться им с друзьями!"
        ),
        "preset_list": (
            "👾Видео: Сжатие для Discord (До 8 МБ)",
            "🚀Видео: YouTube (Оригинал)",
            "🔥Видео: (YouTube Shorts)",
            "🔗Видео: Сшивание клипов (Склейка)",
            "🖼️Видео: Создание GIF-анимации",
            "⚙️Видео: Кастомный битрейт",
            "🎛️Видео: Экспертный режим (OBS)"
        )
    },
    "en": {
        "lbl_frame_expert": " ⚙️ Advanced Settings ",
        "lbl_select_mode": "Select conversion mode:",
        "btn_render_discord": "👾COMPRESS FOR DISCORD",
        "btn_render_youtube": "🚀RENDER FOR YOUTUBE",
        "btn_render_shorts": "🔥RENDER FOR SHORTS",
        "btn_render_custom": "⚙️COMPRESS BY BITRATE",
        "btn_render_concat": "🔗START CLIPS CONCATENATION",
        "btn_render_animation": "🖼️CREATE GIF ANIMATION",
        "btn_render_expert": "💾RUN EXPERT ENCODING",
        "btn_music_select": "🎵 Select Background Music",
        "btn_music_ready": "🎵 Track: ",
        "lbl_slider_quality_shorts": "⚙️ Shorts Setup (Lower value = Wider view / Higher value = Close-up):",
        "lbl_slider_quality_custom": "⚙️ Select Bitrate (Encoding Quality Mbps):",
        "lbl_slider_quality_expert": "⚙️ Select CRF (Lower value = Better image):",
        "chk_2k": "🚀 Upscale / Render in 2K (1440p) for VP09 Codec",
        "msg_ready_title": "Success!",
        "msg_ready_text": "Video is ready and saved here:\n",
        "msg_error_title": "Error",
        "msg_error_empty_video": "Select a video file first!",
        "msg_error_general": "Something went wrong. Check logs in VS Code.\n\n",
        "fd_video_title": "Select Source Video",
        "fd_video_types": "Video Files",
        "fd_save_title": "Where to save the output file?",
        "fd_music_title": "Select Background Music",
        "fd_music_types": "Audio Files",
        "fd_concat_title": "Select a batch of clips for instant merging",
        "lbl_concat_ready": "✅ Ready to merge clips: ",
        "lbl_settings_hw": "Select GPU/CPU for rendering:",
        "lbl_about_title": "VALENOK Video Converter v1.1",
       "btn_about_boosty": "◈ SUPPORT AUTHOR ON BOOSTY ◈",
        "btn_about_close": "❌ CLOSE",
        "fd_all_types": "All Files",
        "lbl_src_file": "Source file:",
        "lbl_dest_file": "Where to save:",
        "lbl_timings": "Cut timings (optional):",
        "lbl_start": "Start:",
        "lbl_end": "End:",
        "btn_browse": "Browse...",
        "lbl_discord_warning": "⚠️ Recommended clip duration: 20-30 sec!\nLonger videos will exceed the strict 20 MB size limit.",
        "chk_2k_full": "🚀 Upscale / Render in 2K (1440p) for VP09 Codec (Upscale processing).",
        "lbl_exp_res": "Video Resolution:",
        "lbl_exp_format": "Container Format:",
        "lbl_exp_audio": "Audio Mode:",
        "lbl_exp_stream": "Select Audio Track (Stream):",
        "menu_settings": "⚙️ Settings",
        "menu_about": "❓ About / Help",
        "lbl_concat_status_def": "⚠️ Warning! Select multiple files at once for merging.",
        "btn_choose_concat": "📂 SELECT BATCH OF CLIPS",
        "msg_concat_err_count": "Bro, you need to select at least 2 clips for merging!",
        "msg_concat_err_path": "Select a folder and name to save the output video!",
        "msg_concat_success": "Clips instantly merged without quality loss!\nFile saved: ",
        "msg_concat_fail": "Merge error. FFmpeg failed to join clips.\nMake sure they are recorded with identical settings in OBS.",
        "license_text": (
            "This software is FREE and provided 'AS IS' without any warranty.\n"
            "The author is not responsible for any hardware failures,\n"
            "burnt chips, or fried motherboards.\n"
            "The software is completely clean, safe, and hand-built.\n"
            "You are free to share it with your friends!"
        ),
        "preset_list": (
            "👾 Video: Compress for Discord (Up to 8 MB)",
            "🚀 Video: YouTube (Original)",
            "🔥 Video: (YouTube Shorts)",
            "🔗 Video: Merge Clips Together (Concat)",
            "🖼️ Video: Create GIF Animation",
            "⚙️ Video: Custom Bitrate Encoding",
            "🎛️ Video: Expert Mode (OBS Tracks)"
        )
    }
}

# Память для пути фоновой музыки (ВЕРСИЯ 0.8)
music_path = ""

# --- ЕДИНАЯ СИСТЕМА НАСТРОЕК (JSON) ПРИ СТАРТЕ ---
default_settings = {
    "hardware": "CPU (Any PC)",
    "lang": "ru" # ДОПИСАЛИ БАЗОВЫЙ ЯЗЫК!
}

# --- ОПРЕДЕЛЯЕМ ПУТЬ К КОНФИГУ В СКРЫТОЙ ПАПКЕ APPDATA ---
appdata_path = os.getenv('APPDATA')
valenok_dir = os.path.join(appdata_path, "HexWastelandProject")
if not os.path.exists(valenok_dir):
    os.makedirs(valenok_dir)

config_path = os.path.join(valenok_dir, "config.json")

# --- ЗАГРУЗКА НАСТРОЕК ПРИ СТАРТЕ ---
if os.path.exists(config_path):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
            # Если в файле есть ключ hardware, обновляем дефолтное значение
            if "hardware" in loaded_data and loaded_data["hardware"] in ["CPU (Any PC)", "NVIDIA (GPU)", "AMD (GPU)"]:
                default_settings["hardware"] = loaded_data["hardware"]
            # Читаем язык из файла конфигурации на диске при старте софта
            if "lang" in loaded_data:
                default_settings["lang"] = loaded_data["lang"]
    except:
        pass # При сбое файла откатимся на безопасные дефолты

# Принудительно передаем считанные из файла настройки в переменные интерфейса Ткинтера
current_lang = default_settings.get("lang", "ru")

# --- АВТОМАТИЧЕСКАЯ УСТАНОВКА ИКОНКИ МАСКОТА (ВЕРСИЯ 0.8) ---
#try:
    # Обернули пути в resource_path, чтобы они работали внутри EXE!
 #   if os.path.exists(resource_path("icon.ico")):
   #     root.iconbitmap(resource_path("icon.ico"))
  #  elif os.path.exists(resource_path("icon.png")):
   #     from PIL import Image
  #      img = Image.open(resource_path("icon.png"))
   #     img.save(resource_path("icon.ico"), format="ICO", sizes=[(256, 256)])
   #     root.iconbitmap(resource_path("icon.ico"))
#except Exception as e:
   # pass

# --- ПРИНУДИТЕЛЬНАЯ УСТАНОВКА ИКОНКИ ДЛЯ ВСЕХ ОКОН МОНОЛИТА ---
try:
    if os.path.exists(resource_path("icon.png")):
        root.wm_iconphoto(True, tk.PhotoImage(file=resource_path("icon.png")))
    elif os.path.exists(resource_path("icon.ico")):
        root.wm_iconphoto(True, tk.PhotoImage(file=resource_path("icon.ico")))
except Exception:
    pass

current_hardware = tk.StringVar(value=default_settings["hardware"])
frame_expert = tk.LabelFrame(root, text=LANG_DICT[current_lang]["lbl_frame_expert"])
main_left_frame = tk.Frame(root)
main_left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

# --- ФУНКЦИИ ---
def choose_file():
    file_path = filedialog.askopenfilename(
        title=LANG_DICT[current_lang]["fd_video_title"],
        filetypes=[(LANG_DICT[current_lang]["fd_video_types"], "*.mp4 *.mov *.mkv *.avi ")]
    )
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

def choose_output_path():
    # Открывает окно сохранения файла Windows
    file_path = filedialog.asksaveasfilename(
        title=LANG_DICT[current_lang]["fd_save_title"],
        filetypes=[(LANG_DICT[current_lang]["fd_video_types"], "*.mp4 *.mkv *.mov *.avi *.gif")]
    )
    if file_path:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, file_path)

# --- ПЕРЕМЕННАЯ ДЛЯ КЛИПОВ СКЛЕЙКИ (ВЕРСИЯ 0.7) ---
selected_clips_paths = []

def choose_multiple_files():
    global selected_clips_paths
    files = filedialog.askopenfilenames(
        title=LANG_DICT[current_lang]["fd_concat_title"],
        filetypes=[(LANG_DICT[current_lang]["fd_video_types"], "*.mp4 *.mkv *.mov *.avi"), (LANG_DICT[current_lang]["msg_error_title"], "*.*")]
    )
    if files:
        selected_clips_paths = list(files)
        # Меняем цвет на зеленый и пишем статус, когда файлы успешно выбраны!
        lbl_concat_status.config(
            text=f"{LANG_DICT[current_lang]['lbl_concat_ready']}{len(selected_clips_paths)}",
            fg="#3ba55d", 
            font=("Segoe UI", 10, "bold")
        )
#===========================================================================
def on_preset_change(event):
    preset = combo_preset.get()
    
    # 1. Режим Эксперта
    if "🎛️" in preset:
        root.geometry("850x480")
        label_discord_warning.pack_forget() # ПРЯЧЕМ ВАРНИНГ ДЛЯ ДИСКОРДА
        frame_concat.pack_forget() #ПРЯЧЕМ ВАРНИНГ ДЛЯ СКЛЕЙКИ                
        btn_music.pack_forget() # Эксперту музыка не нужна, у него своя логика дорожек!
        check_2k.pack_forget()
        frame_quality.pack(pady=10)
        lbl_quality.config(text=LANG_DICT[current_lang]["lbl_slider_quality_expert"])
        frame_expert.pack(side=tk.RIGHT, padx=20, pady=10, fill=tk.Y)
        btn_start.config(text=LANG_DICT[current_lang]["btn_render_expert"])
        root.update()
        # Возвращаем выбор одиночного файла на законное место ну и перед блоком сохранения до кучи (через frame_output!)

        frame_top_input.pack(side=tk.TOP, pady=(10, 0), before=lbl_output_title)
        
        btn_start.pack_forget()
        btn_start.pack(pady=30)


    # 2. Режим Кастома
    elif "⚙️" in preset:
        root.geometry("550x500")
        label_discord_warning.pack_forget() # ПРЯЧЕМ ВАРНИНГ ДЛЯ ДИСКОРДА
        frame_concat.pack_forget() #ПРЯЧЕМ ВАРНИНГ ДЛЯ СКЛЕЙКИ
        frame_quality.pack_forget()
        btn_music.pack(side=tk.TOP, pady=(15, 0))
        check_2k.pack(pady=(5, 0))
        frame_quality.pack(pady=10)
        lbl_quality.config(text=LANG_DICT[current_lang]["lbl_slider_quality_custom"])       
        frame_expert.pack_forget()
        btn_start.config(text=LANG_DICT[current_lang]["btn_render_custom"])
        # Возвращаем выбор одиночного файла на законное место (через frame_output!)

        frame_top_input.pack(side=tk.TOP, pady=(10, 0), before=lbl_output_title)

        btn_start.pack_forget()
        btn_start.pack(pady=30)

    # 3. Режим Анимации (Мем-Гифка)
    elif "🖼️" in preset:
        root.geometry("550x380")
        label_discord_warning.pack_forget() # ПРЯЧЕМ ВАРНИНГ ДЛЯ ДИСКОРДА
        frame_concat.pack_forget() #ПРЯЧЕМ ВАРНИНГ ДЛЯ СКЛЕЙКИ
        frame_quality.pack_forget()
        check_2k.pack_forget()
        frame_expert.pack_forget()
        btn_music.pack_forget()
        btn_start.pack_forget()
        btn_start.pack(pady=30)
        btn_start.config(text=LANG_DICT[current_lang]["btn_render_animation"])
        # Возвращаем выбор одиночного файла на законное место (через frame_output!)

        frame_top_input.pack(side=tk.TOP, pady=(10, 0), before=lbl_output_title)

    # 4. Режим Discord (Явная и строгая проверка!)
    elif "👾" in preset:
        root.geometry("550x440")
        frame_concat.pack_forget() #ПРЯЧЕМ ВАРНИНГ ДЛЯ СКЛЕЙКИ
        frame_quality.pack_forget()
        frame_expert.pack_forget()
        check_2k.pack_forget()
        # Возвращаем выбор одиночного файла на законное место (через frame_output!)

        frame_top_input.pack(side=tk.TOP, pady=(10, 0), before=lbl_output_title)
        # Сначала пакуем рабочие элементы
        btn_music.pack(side=tk.TOP, pady=(15, 0))
        
        # Переносим варнинг СЮДА (строго НАД переприжимом кнопки!)
        label_discord_warning.pack(pady=(10, 10))
        
        # И только в самом конце перепаковываем кнопку, чтобы она ВСЕГДА ложилась на пол!
        btn_start.pack_forget()
        btn_start.pack(pady=30)
        btn_start.config(text=LANG_DICT[current_lang]["btn_render_discord"])

    # 5. Режим YouTube (Явная и строгая проверка!)
    elif "🚀" in preset:
        root.geometry("550x450")
        label_discord_warning.pack_forget() # ПРЯЧЕМ ВАРНИНГ ДЛЯ ДИСКОРДА
        frame_concat.pack_forget() #ПРЯЧЕМ ВАРНИНГ ДЛЯ СКЛЕЙКИ
        frame_quality.pack_forget()
        frame_expert.pack_forget()
        
        btn_start.config(text=LANG_DICT[current_lang]["btn_render_youtube"])
        # Возвращаем выбор одиночного файла на законное место (через frame_output!)

        frame_top_input.pack(side=tk.TOP, pady=(10, 0), before=lbl_output_title)
        btn_music.pack(side=tk.TOP, pady=(15, 0))
        check_2k.pack(pady=(10, 0))
        btn_start.pack_forget()
        btn_start.pack(pady=30)
    
    elif "🔥" in preset:
        root.geometry("550x480") # Увеличили высоту окна под ползунок!
        label_discord_warning.pack_forget()
        frame_concat.pack_forget()
        frame_expert.pack_forget()
        frame_quality.pack_forget()

        btn_start.config(text=LANG_DICT[current_lang]["btn_render_shorts"])

        # Вёрстка конвейера: выводим файлы, музыку и фрейм ползунка на экран
        frame_top_input.pack(side=tk.TOP, pady=(10, 0), before=lbl_output_title)
        btn_music.pack(side=tk.TOP, pady=(15, 0))
        check_2k.pack(pady=(5, 0))
        frame_quality.pack(pady=10) # Вывели ползунок на экран в его первозданном виде!
        lbl_quality.config(text=LANG_DICT[current_lang]["lbl_slider_quality_shorts"])
        btn_start.pack_forget()
        btn_start.pack(pady=20)
        return


    # === НАШ НОВЫЙ БЛОК СКЛЕЙКИ 0.7 ===
    elif "🔗" in preset:
        root.geometry("550x400") # Стандартный компактный размер окна
        
        # 1. Прячем всё лишнее (ползунок качества, эксперт-панель и варнинг дискорда)
        btn_music.pack_forget()
        frame_quality.pack_forget()
        frame_expert.pack_forget()
        label_discord_warning.pack_forget()
        frame_top_input.pack_forget()
        check_2k.pack_forget()
        
        # 2. ПОКАЗЫВАЕМ НАШ ИНТЕРФЕЙС СКЛЕЙКИ
        frame_concat.pack(pady=10)
        
        # 3. Меняем текст на кнопке запуска на ПКД
        btn_start.config(text=LANG_DICT[current_lang]["btn_render_concat"])
        root.update() # <-- ДОПИСАЛИ СЮДА! ПРИНУДИТЕЛЬНО ОБНОВЛЯЕМ ЭКРАН!
        btn_start.pack_forget()
        btn_start.pack(pady=30)
         # Выходим из функции, чтобы нижние if/elif не срабатывали

def open_settings_window():
    global default_settings

    # 1. Создаем второе независимое окно поверх главного (Toplevel)
    settings_win = tk.Toplevel(root)
    settings_win.title("⚙️ Settings")
    settings_win.geometry("400x240") # Просто поменяли 180 на 240!
    settings_win.resizable(False, False) # Запрещаем растягивать окно настроек
    
    # Делаем так, чтобы окно настроек было главным, пока пользователь его не закроет
    settings_win.grab_set()
    
    # 2. Добавляем текстовую надпись внутри окна
    lbl_hw = tk.Label(settings_win, text=LANG_DICT[current_lang]["lbl_settings_hw"], font=("Segoe UI", 10))
    lbl_hw.pack(pady=(15, 5))
    
    # 3. Создаем выпадающий список выбора железа внутри окна настроек
    combo_hw_settings = ttk.Combobox(settings_win, values=[
        "CPU (Any PC)",
        "NVIDIA (GPU)",
        "AMD (GPU)"
    ], state="readonly", width=30, font=("Segoe UI", 10))
    
    # Подтягиваем из памяти то железо, которое уже было выбрано ранее
    combo_hw_settings.set(current_hardware.get())
    combo_hw_settings.pack(pady=5)

    # === ШАГ №1: СОЗДАЕМ ВЫБОР ЯЗЫКА В ОКНО НАСТРОЕК (ВЕРСИЯ 1.0 GLOBAL) ===
    tk.Label(settings_win, text="Выбери язык интерфейса / Select language:", font=("Segoe UI", 10)).pack(pady=(15, 5))
    combo_lang = ttk.Combobox(settings_win, values=["Русский (RU)", "English (EN)"], state="readonly", width=25)
    combo_lang.pack(pady=5) # Выполнялось только на русском!
    # Автоматически выставляем текущий язык из конфига при открытии окна
    if default_settings.get("lang", "ru") == "en":
        combo_lang.current(1)
    else:
        combo_lang.current(0)
    

    # # 4. Функция, которая сработает при нажатии кнопки "Сохранить"
    def save_settings():
        selected_hw = combo_hw_settings.get()
        current_hardware.set(selected_hw)
        
        # Перехватываем выбранный язык с экрана (Шаг №2)
        selected_lang = "en" if "English" in combo_lang.get() else "ru"
        
        # Сохраняем ВСЁ в наш глобальный словарь памяти программы
        default_settings["hardware"] = selected_hw
        default_settings["lang"] = selected_lang
        
        # Записываем обновленный конфиг в наш единый config.json файл на диск
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(default_settings, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Couldn't save settings:\n{e}")

        # ВОТ ЭТУ СТРОЧКУ ВЕРНИ СЮДА! ОНА ОТВЕЧАЕТ ЗА ОБНОВЛЕНИЕ НА ХОДУ!
        update_interface_language()    
    # Закрываем окно настроек и выдаем красивую плашку успеха с предупреждением о перезапуске
        settings_win.destroy()
    
    # Текст сообщения динамически подстраивается под выбранный язык
        if selected_lang == "en":
            msg_success = "Your changes are saved! Meow!\n\n(Note: Some interface elements will update after restarting the app)"
        else:
            msg_success = "Настройки успешно сохранены! Мяу!\n\n(Примечание: Некоторые элементы интерфейса обновятся после перезапуска программы)"
        
        messagebox.showinfo("Nice", msg_success)

        
    # 5. Кнопка "Сохранить" внизу окна настроек
    btn_save = tk.Button(
        settings_win, 
        text="💾 СОХРАНИТЬ", 
        font=("Segoe UI", 10, "bold"), 
        bg="#2f3136", 
        fg="white", 
        activebackground="#3ba55d", 
        activeforeground="white", 
        relief=tk.FLAT, 
        width=15,
        command=save_settings
    )
    btn_save.pack(pady=15)

def update_interface_language():
    global current_lang, lbl_select_mode  # ДОПИСАЛИ ПЕРЕМЕННУЮ ЧЕРЕЗ ЗАПЯТУЮ!
    # 1. Читаем актуальный язык из нашей общей конфигурации
    current_lang = default_settings.get("lang", "ru")
    
    # 2. Вытаскиваем нужную языковую ветку (RU или EN) из LANG_DICT
    texts = LANG_DICT[current_lang]
    
    # 3. Перезаливаем боковое меню пресетов на лету!
    # Запоминаем, какой индекс сейчас выбран челиком, чтобы фокус не сбрасывался
    current_idx = combo_preset.current()
    if current_idx == -1: 
        current_idx = 0
        
    combo_preset['values'] = texts["preset_list"]
    combo_preset.current(current_idx)
    
    # 4. Перекрашиваем галочку 2К
    check_2k.config(text=texts["chk_2k"])
    
    # 5. Если музыкальный трек ещё не выбран геймером, переводим базовый текст кнопки музыки
    if not music_path:
        btn_music.config(text=texts["btn_music_select"])
    
        # Перекрашиваем рамку эксперта на лету!
    frame_expert.config(text=LANG_DICT[current_lang]["lbl_frame_expert"])
    lbl_quality.config(text=LANG_DICT[current_lang]["lbl_slider_quality_custom"])
        # Перевод элементов главного экрана на лету

    lbl_file_title.config(text=texts["lbl_src_file"])
    btn_browse.config(text=texts["btn_browse"])
    lbl_output_title.config(text=texts["lbl_dest_file"])
    btn_output_browse.config(text=texts["btn_browse"])
    lbl_timings_title.config(text=texts["lbl_timings"])
    lbl_start_title.config(text=texts["lbl_start"])
    lbl_end_title.config(text=texts["lbl_end"])
        # Перевод правой панели Эксперта и верхнего системного меню на лету!

    lbl_exp_res.config(text=texts["lbl_exp_res"])
    lbl_exp_format.config(text=texts["lbl_exp_format"])
    lbl_exp_audio.config(text=texts["lbl_exp_audio"])
    lbl_exp_stream.config(text=texts["lbl_exp_stream"])
    
    # 1. Получаем текущую строку из комбобокса пресетов
    current_mode_text = combo_preset.get()

    # 2. Проверяем смайлик и мгновенно переводим главную кнопку
    if "🔗" in current_mode_text:
        btn_start.config(text=LANG_DICT[current_lang]["btn_render_concat"])
    elif "👾" in current_mode_text:
        btn_start.config(text=LANG_DICT[current_lang]["btn_render_discord"])
    elif "🚀" in current_mode_text:
        btn_start.config(text=LANG_DICT[current_lang]["btn_render_youtube"])
    elif "🔥" in current_mode_text:
        btn_start.config(text=LANG_DICT[current_lang]["btn_render_shorts"])
    elif "⚙️" in current_mode_text or "⚙" in current_mode_text:
        btn_start.config(text=LANG_DICT[current_lang]["btn_render_custom"])
    elif "🖼️" in current_mode_text or "🖼" in current_mode_text:
        btn_start.config(text=LANG_DICT[current_lang]["btn_render_animation"])
    elif "💾" in current_mode_text:
        btn_start.config(text=LANG_DICT[current_lang]["btn_render_expert"])
  #######  
        # Перекрашиваем блок Склейки клипов на лету!
    # Если пачка клипов ещё не выбрана, возвращаем базовый переведённый статус
    if not selected_clips_paths:
        lbl_concat_status.config(text=LANG_DICT[current_lang]["lbl_concat_status_def"])
    btn_choose_concat.config(text=LANG_DICT[current_lang]["btn_choose_concat"])

    lbl_select_mode.config(text=LANG_DICT[current_lang]["lbl_select_mode"])

    # === ПЕРЕВОД БОКОВОГО МЕНЮ ПРЕСЕТОВ НА ЛЕТУ ===
    current_idx = combo_preset.current()
    if current_idx == -1: 
        current_idx = 0
        
    combo_preset['values'] = LANG_DICT[current_lang]["preset_list"]
    combo_preset.current(current_idx)

def open_about_window():
    # 1. Создаем всплывающее независимое окно поверх главного
    about_win = tk.Toplevel(root)
    about_win.title("❓ About")
    about_win.geometry("450x430")
    about_win.resizable(False, False)
    about_win.grab_set()
    
    # 2. Используем Pillow, чтобы загрузить ТВОЮ ЛУЧШУЮ АВАТАРКУ!
    try:
        from PIL import Image, ImageTk
        # Тоже обернули путь к аве в resource_path!
        if os.path.exists(resource_path("avatar.png")):
            img = Image.open(resource_path("avatar.png")).resize((90, 90))
            render_img = ImageTk.PhotoImage(img)
            lbl_img = tk.Label(about_win, image=render_img)
            lbl_img.image = render_img
            lbl_img.pack(pady=10)
    except:
        pass
        
    # 3. Красивый заголовок и Твой Ник
    tk.Label(about_win, text=LANG_DICT[current_lang]["lbl_about_title"], font=("Segoe UI", 12, "bold")).pack(pady=5)
    tk.Label(about_win, text="Автор: .HeXaGoN. (Steam ID: hollowash)", font=("Segoe UI", 10, "italic"), fg="#3ba55d").pack()
    
    # 4. Наш юридический щит-лицензия MIT (Программа чистая, безопасная, "AS IS")
    license_text = LANG_DICT[current_lang]["license_text"]

    tk.Label(about_win, text=license_text, font=("Segoe UI", 9), justify=tk.CENTER, fg="#a3a6aa").pack(pady=15)
     
        # 1. Функция, которая откроет браузер при клике
    def open_boosty():
        # Сюда ты потом вставишь свою реальную ссылку вместо заглушки!
        webbrowser.open("https://boosty.to/hollowash")

    # 2. Создаем сочную оранжевую кнопку поддержки автора!
    tk.Button(about_win, text=LANG_DICT[current_lang]["btn_about_boosty"], font=("Segoe UI", 9, "bold"),
              bg="#FF6600", fg="white", activebackground="#E65C00", activeforeground="white",
              relief=tk.FLAT, command=open_boosty).pack(pady=5)

    # 5. Кнопка закрытия
    tk.Button(about_win, text=LANG_DICT[current_lang]["btn_about_close"], font=("Segoe UI", 9, "bold"), bg="#2f3136", fg="white", 
              width=12, relief=tk.FLAT, command=about_win.destroy).pack(pady=5)

def create_music_button():
    """ Изолированная функция создания одной умной аудиокнопки (ВЕРСИЯ 0.8) """
    def choose_music_file():
        global music_path
        m_file = filedialog.askopenfilename(
            title=LANG_DICT[current_lang]["fd_music_title"],
            filetypes=[(LANG_DICT[current_lang]["fd_music_types"], "*.mp3 *.wav *.ogg *.m4a"), (LANG_DICT[current_lang]["fd_all_types"], "*.*")]
        )
        if m_file:
            music_path = m_file
            file_name = os.path.basename(m_file)
            btn_music.config(text=f"{LANG_DICT[current_lang]['btn_music_ready']}{file_name}", bg="#3ba55d", fg="white")
        else:
            music_path = ""
            btn_music.config(text=LANG_DICT[current_lang]["btn_music_select"], bg="#2f3136", fg="white")

    global btn_music
    btn_music = tk.Button(main_left_frame, text=LANG_DICT[current_lang]["btn_music_select"], font=("Segoe UI", 9, "bold"),
                          bg="#2f3136", fg="white", relief=tk.FLAT, width=35, command=choose_music_file)

def time_to_seconds(t_str):
    if not t_str or t_str.strip() == "00:00:00" or t_str.strip() == "00:00":
        return 0.0
    try:
        parts = list(map(float, t_str.strip().split(':')))
        if len(parts) == 3:      # ЧЧ:ММ:СС
            return parts[0] * 3600 + parts[1] * 60 + parts[2]
        elif len(parts) == 2:    # ММ:СС
            return parts[0] * 60 + parts[1]
        elif len(parts) == 1:    # Просто секунды
            return parts[0]
    except:
        return -1.0  # Ошибка парсинга
    return 0.0

def check_render_result(output_file, current_lang):
    # Проверяем, что файл существует и весит БОЛЬШЕ 1 КБ (1024 байт)
    if os.path.exists(output_file) and os.path.getsize(output_file) > 1024:
        # Включаем звук успеха прямо здесь
        if os.path.exists("ready.wav"):
            winsound.PlaySound("ready.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            
        messagebox.showinfo(
            LANG_DICT[current_lang]["msg_ready_title"],
            LANG_DICT[current_lang]["msg_ready_text"] + f" {output_file}"
        )
        return True
    else:
        # Если файл — мелкий огрызок или пустышка, зачищаем мусор
        if os.path.exists(output_file):
            try: os.remove(output_file)
            except: pass
            
        # Бьём юзера по рукам
        if current_lang == "en":
            messagebox.showerror("Error", "The output file is corrupted or empty! Specified timings exceed the actual video duration.")
        else:
            messagebox.showerror("Ошибка", "Файл повреждён или пуст! Указанные тайминги выходят за пределы длины видео.")
        return False

def start_conversion():
    # 1. Забираем текст из полей на экране
    input_file = entry_file.get().strip()
    start_time = entry_start.get().strip()
    end_time = entry_end.get().strip()
    # Умный расчёт высоты кадра на основе состояния нашей галочки (ВЕРСИЯ 0.9)
    target_height = 1440 if var_2k.get() == 1 else 1080
    hw = current_hardware.get() # Теперь эта переменная сама спустится во все Discord, YouTube и Кастом ниже по коду! (Меню настроек делаем)
    preset = combo_preset.get() # Теперь пресет создаётся первым делом!

    # === НАЧАЛО ЛОГИКИ СКЛЕЙКИ КЛИПОВ (ВЕРСИЯ 0.7) ===
    if "🔗" in preset:
        # 1. Проверяем входные данные
        if len(selected_clips_paths) < 2:
            messagebox.showerror(LANG_DICT[current_lang]["msg_error_title"], LANG_DICT[current_lang]["msg_concat_err_count"])
            return

        output_file = entry_output.get().strip()
        if not output_file:
            messagebox.showerror(LANG_DICT[current_lang]["msg_error_title"], LANG_DICT[current_lang]["msg_concat_err_path"])
            return

        if not output_file.lower().endswith(('.mp4', '.mkv', '.mov', '.avi')):
            output_file += ".mp4"

        try:
            root.withdraw() # Прячем главное окно от зависания

            # 1. Автоматически вычисляем букву диска, где лежит самый первый выбранный клип юзера
            first_clip_path = selected_clips_paths[0]
            drive_letter = os.path.splitdrive(first_clip_path)[0] # Вернет "G:" или "E:"
            
            # 2. Создаем временный буфер строго в корне ТОГО ЖЕ ДИСКА, где лежат видосы!
            # Путь будет выглядеть как "G:/valenok_temp" — кристально чисто, коротко и без апострофов!
            temp_dir = os.path.join(drive_letter, "/", "valenok_temp").replace("\\", "/")

            if os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir, exist_ok=True)

            temp_clips = []
            # Бесшумно линкуем или копируем файлы под простыми именами (1.mp4, 2.mp4...)
            for idx, clip_path in enumerate(selected_clips_paths, start=1):
                ext = os.path.splitext(clip_path)[1] or ".mp4"
                temp_clip_name = f"{idx}{ext}"
                temp_clip_path = os.path.join(temp_dir, temp_clip_name).replace("\\", "/")
                
                # Используем жесткую ссылку Windows (os.link) — это мгновенно и не тратит место на диске!
                # Если диски разные, сработает безопасное резервное копирование shutil
                try:
                    os.link(clip_path, temp_clip_path)
                except:
                    import shutil
                    shutil.copy2(clip_path, temp_clip_path)
                
                temp_clips.append(temp_clip_path)

            # Создаем list.txt внутри нашей изолированной папки TEMP
            abs_list_path = os.path.join(temp_dir, "list.txt").replace("\\", "/")
            with open(abs_list_path, "w", encoding="utf-8") as f:
                for t_clip in temp_clips:
                    # Пути теперь кристально чистые, короткие, без пробелов и апострофов!
                    f.write(f"file '{t_clip}'\n")

            # Временный выходной файл собираем там же, в чистой папке
            temp_output = os.path.join(temp_dir, "output_concat.mp4").replace("\\", "/")

            # Собираем ультимативную команду мгновенной сшивки
            cmd = ['ffmpeg.exe', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', abs_list_path, '-c', 'copy', temp_output]
            
            # Запуск процесса склейки внутри буфера
            subprocess.run(cmd, check=True)

            # Переносим готовый сшитый монолит по реальному пути геймера
            if os.path.exists(temp_output):
                import shutil
                shutil.move(temp_output, output_file)

            # ТОТАЛЬНАЯ ЗАЧИСТКА: сносим временную папку со всем содержимым
            if os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir)

            root.deiconify()  # Возвращаем главное окно на экран

            if os.path.exists("ready.wav"):
                winsound.PlaySound("ready.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)    
            messagebox.showinfo("Nice!", LANG_DICT[current_lang]["msg_concat_success"])
            
            # Автоматически открываем проводник Windows и ювелирно выделяем мышкой готовый `.mp4`!
            #try:
                #win_output_path = os.path.abspath(output_file).replace("/", "\\")
                #subprocess.run(['explorer', '/select,', win_output_path])
            #except:
                #pass

                    # Автоматически открываем папку с готовым результатом без дублирования проводника
            os.startfile(os.path.dirname(os.path.abspath(output_file)))     
            return

        except Exception as e:
            # Аварийная зачистка буфера в случае любого краша
            if 'temp_dir' in locals() and os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir)
            root.deiconify()
        # ВРУБАЕМ ЗВУК КРАША ДЛЯ СКЛЕЙКИ ЧЕРЕЗ WINSOUND!
            if os.path.exists("error.wav"):
                winsound.PlaySound("error.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            # Выпрямили showerror на каноничный синтаксис Tkinter с двумя аргументами
            messagebox.showerror("Error", LANG_DICT[current_lang]["msg_concat_fail"])
            return


        #===========================================================

    if not input_file:
        # Скрытый запуск мемного звука ошибки, если челик забыл выбрать видео!
        if os.path.exists("error.wav"):
            winsound.PlaySound("error.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

        messagebox.showerror("Error", "Сначала выбери видео файл!\nPlease choose file!")
        return

    # 2. Выбор сохранения файла
    output_file = entry_output.get().strip()
    if not output_file:
        # Скрытый запуск мемного звука ошибки, если челик забыл выбрать куда сохранить!
        if os.path.exists("error.wav"):
            winsound.PlaySound("error.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            
        messagebox.showerror("Ошибка", "Выбери, куда сохранить файл!\nChoose save path")
        return

    # === УМНАЯ ВАЛИДАЦИЯ ТАЙМКОДОВ ДО ЗАПУСКА ===
    start_sec = time_to_seconds(start_time)
    end_sec = time_to_seconds(end_time)

    # 1. Проверяем на сломанный формат ввода (если функция вернула -1)
    if start_sec < 0 or end_sec < 0:
        if current_lang == "en":
            messagebox.showerror("Error", "Invalid time format! Use HH:MM:SS or MM:SS.")
        else:
            messagebox.showerror("Ошибка", "Неверный формат времени! Используйте ЧЧ:ММ:СС или ММ:СС.")
        return  # Стопаем выполнение функции, до FFmpeg дело не дойдёт

    # 2. Проверяем логику: время конца не может быть меньше или равно времени начала
    # (Проверку делаем, только если конечное время вообще задано и не равно нулю)
    if end_sec > 0 and start_sec >= end_sec:
        if current_lang == "en":
            messagebox.showerror("Error", "Stop time cannot be less than or equal to start time!")
        else:
            messagebox.showerror("Ошибка", "Время окончания не может быть меньше или равно времени начала!")
        return  # Жесткий стоп


    # 3. Начинаем собирать команду для FFmpeg из кирпичиков
        # Добавляем флаг -y, чтобы FFmpeg молча перезаписывал файлы без вопросов в консоли
    cmd = ['ffmpeg.exe', '-y']

    # Умная проверка таймингов для Валенка 0.2 +
    if start_time and start_time != "00:00:00": 
        cmd += ['-ss', start_time]
    if end_time and end_time != "00:00:00": 
        cmd += ['-to', end_time]

    # Добавляем исходник (СУКА Я ДОБАВИЛ ВСЕ КАРТЫ ДОРОЖЕК БЛЯТЬ! ЗДЕСЬ СУКА. ёбаный нахуй рот сука блять.)
    cmd += ['-i', input_file]

        # === ДОБАВЛЕНИЕ ВТОРОГО ИСТОЧНИКА ЗВУКА СТРОГО ПОД ВИДЕО ИГРЫ (ВЕРСИЯ 0.8) ===
    # Теперь игра ВСЕГДА будет файлом, тайминги режут её идеально, а музыка ВСЕГДА будет файлом!
    #if music_path and os.path.exists(music_path) and "🔗" not in preset and "🖼️" not in preset and "🎛️" not in preset:
        #cmd += ['-i', music_path]

        # Если выбран режим без фоновой музыки, принудительно очищаем переменную в памяти
    if "🔗" in preset or "🖼️" in preset or "🎛️" in preset:
        music_path = ""

    # Теперь базовое условие сработает идеально во всех режимах!
    if music_path and os.path.exists(music_path):
        cmd += ['-i', music_path]

    # Умная проверка: если пользователь забыл расширение, дописываем его сами
    if not output_file.lower().endswith(('.mp4', '.mkv', '.avi', '.gif','.mov')):
        if "🖼️" in preset:
            output_file += ".gif"
        else:
            output_file += ".mp4"

    if "👾" in preset:
        # Умный выбор кодека для Дискорда в зависимости от железа
        if hw == "NVIDIA (GPU)":
            cmd += ['-c:v', 'h264_nvenc', '-b:v', '6M', '-maxrate', '7M', '-bufsize', '10M']
        elif hw == "AMD (GPU)":
            cmd += ['-c:v', 'h264_amf', '-b:v', '6M']
        elif hw == "CPU (Any PC)":
            cmd += ['-c:v', 'libx264', '-preset', 'fast', '-crf', '26']
        
        # Дописываем общий звук для Дискорда и выходной файл
                # Умный микшер дорожек для пресета YouTube:
        if music_path and os.path.exists(music_path):
            cmd += [
                '-filter_complex', '[0:a?][1:a]amix=inputs=2:duration=first:dropout_transition=2[aout]',
                '-map', '0:v:0', '-map', '[aout]', '-c:a', 'aac', '-b:a', '192k', output_file
            ]
        else:
            cmd += ['-map', '0:v?', '-map', '0:a?', '-c:a', 'aac', '-b:a', '192k', output_file]
    
    elif "🚀" in preset:

        # Если челик нажал галочку 2К, принудительно делаем апскейл до 1440p для VP09 кодека!
        if var_2k.get() == 1:
            cmd += ['-vf', 'scale=-1:1440', '-pix_fmt', 'yuv420p']

        # Умный выбор кодека для YouTube в зависимости от железа
        if hw == "NVIDIA (GPU)":
            cmd += ['-c:v', 'h264_nvenc', '-b:v', '18M', '-maxrate', '22M', '-bufsize', '25M']
        elif hw == "AMD (GPU)":
            cmd += ['-c:v', 'h264_amf', '-b:v', '18M']
        elif hw == "CPU (Any PC)":
            cmd += ['-c:v', 'libx264', '-preset', 'fast', '-crf', '18']
            
        # Дописываем максимальный звук для YouTube и выходной файл
                # Умный микшер дорожек для пресета YouTube:
        if music_path and os.path.exists(music_path):
            cmd += [
                '-filter_complex', '[0:a?][1:a]amix=inputs=2:duration=first:dropout_transition=2[aout]',
                '-map', '0:v:0', '-map', '[aout]', '-c:a', 'aac', '-b:a', '192k', output_file
            ]
        else:
            cmd += ['-map', '0:v?', '-map', '0:a?', '-c:a', 'aac', '-b:a', '192k', output_file]

    elif "🔥" in preset:
        # 1. Забираем значение из твоего родного ползунка (от 15 до 30)
        crop_val = scale_quality.get()
        
        # 2. Вычисляем нормальный коэффициент приближения для ползунка
        zoom_factor = crop_val / 10.0
        
        # 3. Адаптивная математика кропа: если галка 2К стоит — принудительно режем под 1440,
        # если выключена — отдаем оригинальную высоту 'ih' прямо в руки FFmpeg без деления в Питоне!
        if var_2k.get() == 1:
            crop_filter = f"crop=w=(1440/{zoom_factor})*9/16:h=1440/{zoom_factor}"
        else:
            crop_filter = f"crop=w=(ih/{zoom_factor})*9/16:h=ih/{zoom_factor}"
            
        cmd += ['-vf', crop_filter, '-pix_fmt', 'yuv420p']

        # # 3. Умный выбор кодека и ДИНАМИЧЕСКИЙ БИТРЕЙТ для защиты деталей при зуме!
        # Чем сильнее приближение (ближе к 30), тем выше битрейт. На 15 выдаст 15M, на 30 выдаст 25M!
        dynamic_bitrate = 15 + (crop_val - 15) * 0.66
        bitrate_str = f"{int(dynamic_bitrate)}M"
        maxrate_str = f"{int(dynamic_bitrate + 3)}M"
        bufsize_str = f"{int(dynamic_bitrate + 5)}M"
        
        if hw == "NVIDIA (GPU)":
            cmd += ['-c:v', 'h264_nvenc', '-b:v', bitrate_str, '-maxrate', maxrate_str, '-bufsize', bufsize_str]
        elif hw == "AMD (GPU)":
            cmd += ['-c:v', 'h264_amf', '-b:v', bitrate_str]
        elif hw == "CPU (Any PC)":
            # Для проца принудительно зажимаем CRF (делаем качество выше), если кадр сильно зумится
            chosen_crf = 18 - int((crop_val - 15) * 0.2)
            cmd += ['-c:v', 'libx264', '-preset', 'fast', '-crf', str(chosen_crf)]

        # 4. Умный микшер дорожек (наш триумф из патча 0.8!)
        if music_path and os.path.exists(music_path):
            cmd += [
                '-filter_complex', '[0:a?][1:a]amix=inputs=2:duration=first:dropout_transition=2[aout]',
                '-map', '0:v:0', '-map', '[aout]', '-c:a', 'aac', '-b:a', '192k', output_file
            ]
        else:
            cmd += ['-map', '0:v?', '-map', '0:a?', '-c:a', 'aac', '-b:a', '192k', output_file]
    
    elif "🖼️" in preset:
        cmd += ['-vf', 'crop=1280:720,fps=25,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse', '-an', output_file]

    elif "⚙️" in preset:
        # Считываем железку и ползунок качества
        quality = str(scale_quality.get())
        
        # Если челик нажал галочку 2К, делаем апскейл Кастомного режима до 1440p!
        if var_2k.get() == 1:
            cmd += ['-vf', 'scale=-1:1440', '-pix_fmt', 'yuv420p']


        if hw == "NVIDIA (GPU)":
            cmd += ['-c:v', 'h264_nvenc', '-rc', 'constqp', '-qp', quality]
        elif hw == "AMD (GPU)":
            cmd += ['-c:v', 'h264_amf', '-rc', '0', '-qp_i', quality, '-qp_p', quality]
        elif hw == "CPU (Any PC)":
            cmd += ['-c:v', 'libx264', '-preset', 'fast', '-crf', quality]
            
        # Дописываем стандартный звук и выходной файл ОДИН РАЗ в самом коде Кастома
                # Умный микшер дорожек для пресета YouTube:
        if music_path and os.path.exists(music_path):
            cmd += [
                '-filter_complex', '[0:a?][1:a]amix=inputs=2:duration=first:dropout_transition=2[aout]',
                '-map', '0:v:0', '-map', '[aout]', '-c:a', 'aac', '-b:a', '192k', output_file
            ]
        else:
            cmd += ['-map', '0:v?', '-map', '0:a?', '-c:a', 'aac', '-b:a', '192k', output_file]

    elif "🎛️" in preset:
        # 1. Забираем настройки из правой панели и ползунка
        res = combo_res.get()
        fmt = combo_format.get()
        audio = combo_audio.get()
        stream = combo_stream.get()  # Читаем наш новый список дорожек!
        quality = str(scale_quality.get())

    
        # 2. Логика изменения разрешения (масштабирование) в Эксперте
        if "1440p" in res:
            cmd += ['-vf', 'scale=-1:1440']  # FFmpeg сам выставит 2560x1440 пиксель в пиксель!
        elif "1080p" in res:
            cmd += ['-vf', 'scale=-1:1080']
        elif "720p" in res:
            cmd += ['-vf', 'scale=-1:720']
        elif "480p" in res:
            cmd += ['-vf', 'scale=-1:480']
            
        # 3. Настройка кодека видео в зависимости от железа
        if "🎵" in stream:
            # Если вытаскиваем MP3: отключаем видеоряд намертво
            cmd += ['-vn', '-c:a', 'libmp3lame', '-q:a', '2'] 
            fmt = ".mp3"
        else:
            # Для обычного видео ставим только выбранный кодек видео
            if hw == "NVIDIA (GPU)":
                cmd += ['-c:v', 'h264_nvenc', '-rc', 'constqp', '-qp', quality]
            elif hw == "AMD (GPU)":
                cmd += ['-c:v', 'h264_amf', '-rc', '0', '-qp_i', quality, '-qp_p', quality]
            elif hw == "CPU (Any PC)":
                cmd += ['-c:v', 'libx264', '-preset', 'fast', '-crf', quality]

        # 4. Умная логика выбора конкретной аудиодорожки (Потока) и её кодека
        a_mode = 'copy' if "Копировать" in audio else 'aac'
        
        if "🌐" in stream:
            # Для всех дорожек оставляем как было, чтобы забрать всё видео
            cmd += ['-map', '0:v?', '-map', '0:a?', '-c:a', a_mode]
            if a_mode == 'aac': cmd += ['-b:a', '192k']
        elif "🎮" in stream:
            # Меняем '0:v?' на '0:v:0', чтобы взять строго одну первую видеодорожку!
            cmd += ['-map', '0:v:0', '-map', '0:a:0?', '-c:a:0', a_mode]
            if a_mode == 'aac': cmd += ['-b:a:0', '192k']
        elif "🎙️" in stream:
            # Меняем '0:v?' на '0:v:0', чтобы взять строго одну первую видеодорожку!
            cmd += ['-map', '0:v:0', '-map', '0:a:1?', '-c:a:0', a_mode]
            if a_mode == 'aac': cmd += ['-b:a:0', '192k']
        elif "🎧" in stream:
            # Меняем '0:v?' на '0:v:0', чтобы взять строго одну первую видеодорожку!
            cmd += ['-map', '0:v:0', '-map', '0:a:2?', '-c:a:0', a_mode]
            if a_mode == 'aac': cmd += ['-b:a:0', '192k']

        # 5. Принудительно меняем расширение файла сохранения на выбранный формат
        output_file = os.path.splitext(output_file)[0] + fmt
        
        # 6. Дописываем готовое имя файла в конец нашей команды
        cmd.append(output_file)
        
    # 4. Запускаем!
    try:
        # Прячем окно на время конвертации, чтобы оно не зависало
        root.withdraw() 
        
        # Запускаем процесс и ждем окончания
        subprocess.run(cmd, check=True)
        
        # Возвращаем окно обратно
        root.deiconify()
        
               # Запускаем нашу универсальную проверку
        success = check_render_result(output_file, current_lang)

        # Открываем папку с проводником, ТОЛЬКО если файл реально создался успешно!
        if success:
            #abs_output_path = os.path.abspath(output_file).replace('/', '\\')
            #subprocess.Popen(f'explorer.exe /select,"{abs_output_path}"')
            os.startfile(os.path.dirname(os.path.abspath(output_file)))

    except Exception as e:
        root.deiconify()
        
        # 3. Скрытый запуск мемного звука критической ошибки
        if os.path.exists("error.wav"):
            winsound.PlaySound("error.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            
        messagebox.showerror("Error", f"Something goes worng check VScode Log.\n\n{e}")

# # Блок выбора файла (Сборка в единый каркас)
frame_top_input = tk.Frame(main_left_frame)
frame_top_input.pack(pady=(10, 0)) # И убрали .pack() у внутренних элементов, они теперь внутри frame_top_input!

lbl_file_title = tk.Label(frame_top_input, text=LANG_DICT[current_lang]["lbl_src_file"])
lbl_file_title.pack(pady=(0, 5))

frame_file = tk.Frame(frame_top_input)
frame_file.pack()

entry_file = tk.Entry(frame_file, width=50)
entry_file.pack(side=tk.LEFT, padx=5)

btn_browse = tk.Button(frame_file, text=LANG_DICT[current_lang]["btn_browse"], command=choose_file)
btn_browse.pack(side=tk.LEFT)

# Блок сохранения файла
lbl_output_title = tk.Label(main_left_frame, text=LANG_DICT[current_lang]["lbl_dest_file"])
lbl_output_title.pack(pady=(15, 0))
frame_output = tk.Frame(main_left_frame)
frame_output.pack()
entry_output = tk.Entry(frame_output, width=50)
entry_output.pack(side=tk.LEFT, padx=5)
btn_output_browse = tk.Button(frame_output, text=LANG_DICT[current_lang]["btn_browse"], command=choose_output_path)
btn_output_browse.pack(side=tk.LEFT)

# Блок таймингов
lbl_timings_title = tk.Label(main_left_frame, text=LANG_DICT[current_lang]["lbl_timings"])
lbl_timings_title.pack(pady=(20, 0))
frame_time = tk.Frame(main_left_frame)
frame_time.pack()
lbl_start_title = tk.Label(frame_time, text=LANG_DICT[current_lang]["lbl_start"])
entry_start = tk.Entry(frame_time, width=10)
entry_start.grid(row=0, column=1, padx=5)
lbl_end_title = tk.Label(frame_time, text=LANG_DICT[current_lang]["lbl_end"])
entry_end = tk.Entry(frame_time, width=10)
entry_end.grid(row=0, column=3, padx=5)
# Автоматически заполняем поля маской времени при старте
entry_start.insert(0, "00:00:00")
entry_end.insert(0, "00:00:00")

# Блок выбора режима
lbl_select_mode = tk.Label(main_left_frame, text=LANG_DICT[current_lang]["lbl_select_mode"])
lbl_select_mode.pack(pady=(20, 0))
combo_preset = ttk.Combobox(main_left_frame, values=LANG_DICT[current_lang]["preset_list"], state="readonly", width=42)
combo_preset.current(0)
combo_preset.pack()
combo_preset.bind("<<ComboboxSelected>>", on_preset_change)

# === Ручной режим (Здесь был костль до Настроек) ===

# --- БЛОК 4.5: ПОЛЗУНОК КАЧЕСТВА (общий для Кастома и Эксперта) ---
frame_quality = tk.Frame(main_left_frame)

lbl_quality = tk.Label(frame_quality, text=LANG_DICT[current_lang]["lbl_slider_quality_custom"])
lbl_quality.pack(anchor=tk.W, padx=5)
scale_quality = tk.Scale(frame_quality, from_=15, to=30, orient=tk.HORIZONTAL, length=200)
scale_quality.set(23)
scale_quality.pack(padx=5, pady=5)

# === ФЛАЖОК ДЛЯ 2К РЕНДЕРА (ВЕРСИЯ 0.9) ===
# Скрытая переменная, которая хранит состояние: 1 — галочка стоит (2К), 0 — не стоит (1080p)
var_2k = tk.IntVar(value=0)
    
# Создаём сочную галочку с огоньком прямо под ползунком!
check_2k = tk.Checkbutton(main_left_frame, text=LANG_DICT[current_lang]["chk_2k_full"], variable=var_2k)
check_2k.pack(pady=(5, 0))

check_2k.pack_forget()

# Создаём аудиокнопку в памяти прямо над кнопкой рендера
create_music_button()

# --- НАШ НОВЫЙ ЭЛЕМЕНТ: ПОДГЛЯДЫВАЮЩИЙ ВАРНИНГ ДЛЯ DISCORD ---
label_discord_warning = tk.Label(
    main_left_frame, 
    text=LANG_DICT[current_lang]["lbl_discord_warning"],
    font=("Segoe UI", 9, "italic"), 
    fg="#000000",  # Negr word, 
    justify=tk.LEFT
)
# При самом первом старте программы (так как выбран Дискорд) мы его сразу показываем:
btn_music.pack(side=tk.TOP, pady=(15, 0))
label_discord_warning.pack(pady=(5, 5))

# --- НАШ НОВЫЙ КИРПИЧИК: КНОПКА ЗАПУСКА ---
btn_start = tk.Button(main_left_frame, text="RENDER", font=("Segoe UI", 11, "bold"), bg="#2f3136", fg="white", activebackground="#3ba55d", activeforeground="white", relief=tk.FLAT, width=32, command=start_conversion)
btn_start.pack(pady=30)

# --- НАПОЛНЯЕМ БОКОВУЮ ПАНЕЛЬ ЭКСПЕРТА (для режима Эксперт) ---

# 1. Выбор разрешения видео
lbl_exp_res = tk.Label(frame_expert, text=LANG_DICT[current_lang]["lbl_exp_res"])
lbl_exp_res.pack(anchor=tk.W, padx=5, pady=(5, 0))
combo_res = ttk.Combobox(frame_expert, values=["Original", "1440p (2K)", "1080p (FullHD)", "720p (HD)", "480p (Meme)"], state="readonly", width=22)
combo_res.current(0)
combo_res.pack(padx=5, pady=5)

# 2. Выбор формата файла (контейнера)
lbl_exp_format = tk.Label(frame_expert, text=LANG_DICT[current_lang]["lbl_exp_format"])
lbl_exp_format.pack(anchor=tk.W, padx=5, pady=(5, 0))
combo_format = ttk.Combobox(frame_expert, values=[".mp4", ".mkv", ".mov", ".avi"], state="readonly", width=22)
combo_format.current(0)
combo_format.pack(padx=5, pady=5)

# 3. Настройка аудиодорожки
lbl_exp_audio = tk.Label(frame_expert, text=LANG_DICT[current_lang]["lbl_exp_audio"])
lbl_exp_audio.pack(anchor=tk.W, padx=5, pady=(5, 0))
combo_audio = ttk.Combobox(frame_expert, values=["Copy original sound", "Convert to AAC (Stantard)"], state="readonly", width=22)
combo_audio.current(1)
combo_audio.pack(padx=5, pady=5)

# 4. Выбор аудиодорожки (потока)
lbl_exp_stream = tk.Label(frame_expert, text=LANG_DICT[current_lang]["lbl_exp_stream"])
lbl_exp_stream.pack(anchor=tk.W, padx=5, pady=(5, 0))
combo_stream = ttk.Combobox(frame_expert, values=[
    "🌐 All Audio Tracks (Default)",
    "🎮 Track #1 (Game / Main Sound)",
    "🎙️ Track #2 (Microphone)",
    "🎧 Track #3 (Discord / Voice chat)",  # НАШ НОВЫЙ КИРПИЧИК!
    "🎵 Only Audio (Extract to .mp3)"
], state="readonly", width=22)
combo_stream.current(0)
combo_stream.pack(padx=5, pady=5)

# --- СОЗДАНИЕ ВЕРХНЕГО СИСТЕМНОГО МЕНЮ ---
# 1. Создаем главный невидимый каркас для верхнего меню
main_menu = tk.Menu(root)

# 2. Добавляем кнопку "⚙️ Настройки" и вешаем на неё вызов нашей функции со строки 83
main_menu.add_command(label=LANG_DICT[current_lang]["menu_settings"], command=open_settings_window)
main_menu.add_command(label=LANG_DICT[current_lang]["menu_about"], command=open_about_window)
# 3. Говорим главному окну root, что теперь у него поверху красуется наше меню
root.config(menu=main_menu)

# --- ВИЗУАЛЬНЫЙ БЛОК ДЛЯ РЕЖИМА СКЛЕЙКИ (0.7) ---
frame_concat = tk.Frame(main_left_frame)

# НАШ ВАРНИНГ: Пишется по дефолту оранжевым, пока файлов нет
lbl_concat_status = tk.Label(
    frame_concat, 
    text=LANG_DICT[current_lang]["lbl_concat_status_def"],
    font=("Segoe UI", 9, "italic"), 
    fg="#000000", 
    justify=tk.LEFT
)
lbl_concat_status.pack(pady=5)

btn_choose_concat = tk.Button(
    frame_concat, 
    text=LANG_DICT[current_lang]["btn_choose_concat"],
    font=("Segoe UI", 10, "bold"), 
    bg="#2f3136", 
    fg="white", 
    relief=tk.FLAT, 
    width=25,
    command=choose_multiple_files # Связали с функцией сверху!
)
btn_choose_concat.pack(pady=5)

root.mainloop()
