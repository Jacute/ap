import sys
import os

from mutagen.mp3 import MP3
from mutagen import MutagenError
from random import shuffle
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTextEdit, QFileDialog, \
<<<<<<< HEAD
    QInputDialog, QLabel
=======
    QInputDialog, QAction, QLabel
>>>>>>> master
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import *
from PyQt5 import uic


def time(ms):
    # Расчёт длительности трека
    h, r = divmod(ms, 3600000)
    m, r = divmod(r, 60000)
    s, _ = divmod(r, 1000)
    return ("%d:%02d" % (m,s) if h == 0 else "%d:%02d:%02d" % (h,m,s))


class Player(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('audioplayer.ui', self)  # Загрузка .ui файла
        # Инициализация
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)
        self.list_of_ways_to_files = list()
        self.player.setVolume(50)
        self.list_of_names_of_playlists = list()
        self.list_of_tracks_of_playlists = list()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('Audioplayer')
        self.check_playlists()
        self.add_track.triggered.connect(self.add)
        self.add_folder.triggered.connect(self.add_directory)
        self.delete_track.triggered.connect(self.delete)
        self.check_text.triggered.connect(self.check_text_of_song)
<<<<<<< HEAD
        self.add_songs_to_playlist.clicked.connect(self.add_new_playlist)
        self.delete_playlist.clicked.connect(self.delete_playlist_from_list)
        self.mix_tracks.triggered.connect(self.mix)
        self.clear.triggered.connect(self.delete_all)
        self.play.clicked.connect(self.play_player)
        self.pause.clicked.connect(self.pause_player)
=======
        self.play.clicked.connect(self.play_player)
        self.pause.clicked.connect(self.pause_player)
        self.clear.triggered.connect(self.delete_all)
        self.mix_tracks.triggered.connect(self.mix)
>>>>>>> master
        self.next.clicked.connect(self.next_song)
        self.previous.clicked.connect(self.previous_song)
        self.stop.clicked.connect(self.stop_player)
        self.volume_slider.valueChanged[int].connect(self.change_vol)
        self.player.durationChanged.connect(self.update_duration)
        self.player.positionChanged.connect(self.update_position)
        self.time_slider.valueChanged[int].connect(self.change_pos)
<<<<<<< HEAD
        self.playlists.currentIndexChanged.connect(self.download_playlist)

    def add(self, fnames):
        if not fnames:
            # Диалоговое окно для выбора аудиофайлов
=======
        self.add_tracks_to_playlist.triggered.connect(self.add_new_playlist)
        self.del_playlist.triggered.connect(self.delete_playlist)

    def add(self, fnames):
        if not fnames:
            #Диалоговое окно для выбора аудиофайлов
>>>>>>> master
            fnames = QFileDialog.getOpenFileNames(
                self, 'Выбрать аудиофайл', '',
                'Аудиофайл (*.mp3)')[0]
        try:
            if fnames != ['']:
                for i in fnames:
                    self.list_of_songs.addItem(self.get_title(i))
                    self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(i)))
                self.list_of_ways_to_files.extend(fnames)
        except MutagenError:
<<<<<<< HEAD
            error = ErrorForm()
            error.show()

    def add_directory(self):
        # Диалоговое окно для выбора каталога
        directory = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        if directory != '':
            # Получаем все файлы в выбранной директории
            all_files = os.listdir(directory)
            # Сортируем файлы на те, которые оканчиваются на .mp3
            audiofiles = [directory + '/' + i for i in list(filter(lambda x: x.endswith('.mp3'), all_files))]
            self.add(audiofiles)

    def mix(self):
        # Перемешивание
        # Очищаем MediaPlaylist, а также ListWidget
=======
            self.error = ErrorForm()
            self.error.show()

    def add_directory(self):
        #Диалоговое окно для выбора каталога
        dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        if dirlist != '':
            all_files = os.listdir(dirlist) #Все файлы в выбранной директории
            audiofiles = [dirlist + '/' + i for i in list(filter(lambda x: x.endswith('.mp3'), all_files))]
            self.add(audiofiles)

    def mix(self):
        #Перемешивание
>>>>>>> master
        self.playlist.clear()
        self.list_of_songs.clear()
        # Перемешиваем список с путями к файлам
        shuffle(self.list_of_ways_to_files)
        for i in self.list_of_ways_to_files:
            # Заново получаем все данные об аудиофайлах и наполняем
            # MediaPlaylist и ListWidget
            self.list_of_songs.addItem(self.get_title(i))
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(i)))
        self.setWindowTitle('Audioplayer')
        self.now_playing_track()

    def delete(self):
<<<<<<< HEAD
        # Удаление выбранных аудиофайлов из плейлиста
        # Получаем список выбранных строк в ListWidget
=======
        #Удаление выбранных аудиофайлов из плейлиста
>>>>>>> master
        items = self.list_of_songs.selectedItems()
        for item in items:
            # Удаляем выбранные строки из списка с путями к файлам,
            # ListWidget и MediaPlaylist
            index = self.list_of_songs.row(item)
            self.list_of_songs.takeItem(index)
            self.playlist.removeMedia(index)
            del self.list_of_ways_to_files[index]
        self.now_playing_track()

    def delete_all(self):
<<<<<<< HEAD
        # Удаление плейлиста полностью
=======
        #Удаление плейлиста полностью
>>>>>>> master
        self.playlist.clear()
        self.list_of_songs.clear()
        self.list_of_ways_to_files = list()
        self.now_playing_track()

    def play_player(self):
<<<<<<< HEAD
        # Проигрывание
=======
        #Проигрывание
>>>>>>> master
        self.player.play()
        self.now_playing_track()

    def pause_player(self):
<<<<<<< HEAD
        # Пауза
        self.player.pause()

    def stop_player(self):
        # Остановка плеера
=======
        #Пауза
        self.player.pause()

    def stop_player(self):
        #Остановка плеера
>>>>>>> master
        self.player.stop()

    def next_song(self):
        # Переключение на следующий аудиофайл
        self.playlist.next()
        self.now_playing_track()

    def previous_song(self):
<<<<<<< HEAD
        # Переключение на предыдущий аудиофайл
=======
        #Переключение на предыдущий аудиофайл
>>>>>>> master
        self.playlist.previous()
        self.now_playing_track()

    def change_vol(self):
<<<<<<< HEAD
        # Изменение громкости
        # Громкость в player ставится в соответствии значению volume_slider'а
        self.player.setVolume(self.volume_slider.value())

    def update_duration(self, duration):
        # Установка максимального значения time_slider'а и вывод длительности
        # аудиофайла на end_time (QLabel справа от time_slider)
=======
        #Изменение громкости
        self.player.setVolume(self.volume_slider.value())

    def update_duration(self, duration):
        #Вывод длительности аудиофайла
>>>>>>> master
        self.time_slider.setMaximum(duration)
        self.end_time.setText(time(duration))

    def update_position(self, position):
<<<<<<< HEAD
        # Изменение позиции QSlider'а по мере продвижения аудиофайла
=======
        #Изменение позиции QSlider'а по мере продвижения аудиофайла
        if position > 0:
            self.now_playing_track()
>>>>>>> master
        self.play_time.setText(time(position))
        self.time_slider.setValue(position)

    def change_pos(self):
<<<<<<< HEAD
        # Изменение позиции плеера по мере продвижения QSlider'а (перемотка)
=======
        #Изменение позиции плеера по мере продвижения QSlider'а (перемотка)
>>>>>>> master
        if self.player.duration() != self.player.position() and self.player.duration() != 0:
            self.player.setPosition(self.time_slider.value())

    def now_playing_track(self):
<<<<<<< HEAD
        # Вывод всяческой информации о песне, которая играет в данный момент
        if self.playlist.isEmpty() or not self.player.isSeekable():
            # Если сейчас ничего не играет или плейлист пустой, то
            # длительность аудиофайла и заголовок окна сбрасываются, а
            # обложка альбома прячется
=======
        #Вывод всяческой информации о песне, которая играет в данный момент
        if self.playlist.isEmpty() or not self.player.isSeekable():
>>>>>>> master
            self.setWindowTitle('Audioplayer')
            self.end_time.setText('0:00')
            self.album_pic.hide()
        else:
            track = self.list_of_ways_to_files[self.playlist.currentIndex()]
            self.setWindowTitle(self.get_title(track))
            self.statusBar().showMessage(self.check_info_about_song(track))
            self.getting_album_pic(track)

    def get_title(self, file):
<<<<<<< HEAD
        # Получение  заголовка для окна
        audio = MP3(file)  # Считывание всех метаданных
=======
        #Получение  заголовка для окна
        audio = MP3(file) #Считывание всех метаданных
        '''TDRC (год), TALB (альбом), TIT2 (название трека),
        TPE1 (исполнитель), TCON (жанр), COMM:XXX (текст), APIC (обложка альбома)'''
>>>>>>> master
        if 'TIT2' in audio:
            title = str(audio['TIT2'])
        else:
            title = 'Unknown title'
        if 'TPE1' in audio:
            artist = str(audio['TPE1'])
        else:
            artist = 'Unknown artist'
        return f'{artist} - {title}'

    def check_info_about_song(self, file):
<<<<<<< HEAD
        # Получение всей основной информации о песне из метаданных
        audio = MP3(file)  # Считывание всех метаданных
        # Ключи к метаданным: TDRC - год, TALB - альбом,
        # TIT2 - название трека, TPE1 - исполнитель, TCON - жанр,
        # COMM:XXX - текст, APIC - обложка альбома
=======
        #Получение всей основной информации о песне из метаданных
        audio = MP3(file) #Считывание всех метаданных
>>>>>>> master
        if 'TIT2' in audio:
            title = str(audio['TIT2'])
        else:
            title = 'Unknown title'
        if 'TPE1' in audio:
            artist = str(audio['TPE1'])
        else:
            artist = 'Unknown artist'
        if 'TDRC' in audio:
            year = str(audio['TDRC'])
        else:
            year = 'Unknown year'
        if 'TALB' in audio:
            album = str(audio['TALB'])
        else:
            album = 'Unknown album'
        if 'TCON' in audio:
            genre = str(audio['TCON'])
        else:
            genre = 'Unknown genre'
        return f'Исполнитель: {artist}. Название: {title}. Альбом: {album}. Жанр: {genre}.' \
               f' Год: {year}.'

    def getting_album_pic(self, track):
<<<<<<< HEAD
        # Получение обложки альбома из метаданных
        cover_name = 'cover.png'
        cover_key = ''
        audio = MP3(track)  # Считывание всех метаданных
        for i in audio.keys():
            if i.startswith('APIC'):
                cover_key = i  # Получение правильного ключа с обложкой
=======
        #Получение обложки альбома из метаданных
        cover_name = 'cover.png'
        cover_key = ''
        audio = MP3(track) #Считывание всех метаданных
        for i in audio.keys():
            if i.startswith('APIC'):
                cover_key = i #Получение правильного ключа с обложкой
>>>>>>> master
        if cover_key != '':
            cover_binary = audio[cover_key]
            with open(cover_name, mode="wb") as cover:
                cover.write(cover_binary.data)
            cover = QPixmap(cover_name)
            cover = cover.scaled(251, 251)
            self.album_pic.setPixmap(cover)
            self.album_pic.show()
        else:
            self.album_pic.hide()

    def check_text_of_song(self):
<<<<<<< HEAD
        # Просмотр текста песни из метаданных
=======
        #Просмотр текста песни из метаданных
>>>>>>> master
        audio = MP3(self.list_of_ways_to_files[self.list_of_songs.currentRow()])
        if 'COMM::XXX' in audio:
            self.text = str(audio['COMM::XXX'])
        else:
            self.text = 'Unknown text'
        self.form_for_text = TextForm(self, self.text)
        self.form_for_text.show()

    def add_new_playlist(self):
<<<<<<< HEAD
        # Добавление плейлиста
        # Диалоговое окно с вводом названия плейлиста
=======
        #Добавление плейлиста
>>>>>>> master
        title, ok_pressed = QInputDialog.getText(
            self, "Плейлист", 'Введите название плейлиста')
        with open('playlists.txt', mode='a+', encoding='utf-8') as txt_of_playlists:
            if ok_pressed:
<<<<<<< HEAD
                # Получение всех путей к файлам в виде строки, разделённой \n
                all_files = "\n".join(self.list_of_ways_to_files)
                # Запись в playlists.txt (в начале идёт название, потом все
                # пути к аудиофайлам, разделённые \n, а в конце \n\n
                txt_of_playlists.write(f'{title}\n{all_files}\n\n')
        self.check_playlists()

    def download_playlist(self):
        # Загрузка плейлиста на QListWidget
        # self.playlists - ComboBox
        name = self.playlists.currentText()  # Выбранный текст в ComboBox
        if name != 'Плейлисты':  # "Плейлисты" - начальное значение ComboBox'а
            # Удаление всех текущих аудиофайлов
            self.delete_all()
            # Получаем индекс данного плейлиста в списке с названиями плейлистов
            ind = self.list_of_names_of_playlists.index(name)
            # Получаем все пути к файлам и загружаем их
            file_names = self.list_of_tracks_of_playlists[ind]
            self.add(*file_names)

    def check_playlists(self):
        # Проверка playlists.txt на наличие плейлистов
        with open('playlists.txt', mode='r', encoding='utf-8') as txt_of_playlists:
            # Считываем playlists.txt и получаем список из плейлистов (text)
            text = txt_of_playlists.read().split('\n\n')
            if text != ['']:
                # Цикл всех плейлистов кроме последнего,
                # так как в последнем пустая строка
                for i in text[:-1]:
                    # Разделяем все данные текущего плейлиста
                    playlist = i.split('\n')
                    # Если данного названия плейлиста нету в списке текущих
                    # загруженных плейлистов, то мы его загружаем
                    if playlist[0] not in self.list_of_names_of_playlists:
                        # Добавляем название плейлиста в ComboBox
                        self.playlists.addItem(playlist[0])
                        # Добавляем название плейлиста, а также его содержимое
                        # в соответствующие плейлисты
                        self.list_of_names_of_playlists.append(playlist[0])
                        self.list_of_tracks_of_playlists.append([playlist[1:]])

    def delete_playlist_from_list(self):
        # Удаление плейлиста
        name = self.playlists.currentText()  # Выбранный текст в ComboBox
        if name != 'Плейлисты':  # "Плейлисты" - начальное значение ComboBox'а
            # Получаем название плейлиста, который хотим удалить
            title = self.list_of_names_of_playlists[
                self.playlists.currentIndex() - 1]
            with open('playlists.txt', mode='a+', encoding='utf-8') as txt_of_playlists:
                # Получаем плейлисты, исключая тот, который хотим удалить
                text = list(filter(lambda x: not x.startswith(title),
                                   txt_of_playlists.read().split('\n\n')))
                # Получаем индекс плейлиста, который хотим удалить
                ind = self.list_of_names_of_playlists.index(title)
                # Удаляем плейлист из списков с данными о нём
                del self.list_of_names_of_playlists[ind]
                del self.list_of_tracks_of_playlists[ind]
                # Удаляем плейлист из ComboBox
                self.playlists.removeItem(ind + 1)
                # Удаляем плейлист из playlists.txt
                txt_of_playlists.seek(0)
                txt_of_playlists.truncate()
                txt_of_playlists.write('\n\n'.join(text))


class TextForm(QWidget):
    def __init__(self, *args):
        # Форма для отображения текста выбранного аудиофайла
=======
                all_files = "\n".join(self.list_of_ways_to_files)
                txt_of_playlists.write(f'{title}\n{all_files}\n\n')
        self.check_playlists()

    def download_playlist(self):
        #Загрузка плейлиста на QListWidget
        self.delete_all()
        name = self.sender().text()
        ind = self.list_of_names_of_playlists.index(name)
        fnames = self.list_of_tracks_of_playlists[ind]
        self.add(*fnames)

    def check_playlists(self):
        #Проверка playlists.txt на наличие плейлистов
        with open('playlists.txt', mode='r', encoding='utf-8') as txt_of_playlists:
            text = txt_of_playlists.read().split('\n\n')
            if text != ['']:
                for i in text[:-1]:
                    playlist = i.split('\n')
                    if playlist[0] not in self.list_of_names_of_playlists:
                        self.tmp = QAction(self)
                        self.tmp.setText(playlist[0])
                        self.tmp.setObjectName(playlist[0])
                        self.playlist_menu.addAction(self.tmp)
                        self.tmp.triggered.connect(self.download_playlist)
                        self.list_of_names_of_playlists.append(playlist[0])
                        self.list_of_tracks_of_playlists.append([playlist[1:]])

    def delete_playlist(self):
        #Удаление плейлиста
        title, ok_pressed = QInputDialog.getText(
            self, "Плейлист", 'Введите название плейлиста')
        if title in self.list_of_names_of_playlists:
            with open('playlists.txt', mode='a+', encoding='utf-8') as txt_of_playlists:
                if ok_pressed:
                    text = list(filter(lambda x: not x.startswith(title),
                                       txt_of_playlists.read().split('\n\n')))
                    ind = self.list_of_names_of_playlists.index(title)
                    del self.list_of_names_of_playlists[ind]
                    del self.list_of_tracks_of_playlists[ind]
                    self.playlist_menu.removeAction(self.findChild(QAction, title))
                    txt_of_playlists.seek(0)
                    txt_of_playlists.truncate()
                    txt_of_playlists.write('\n\n'.join(text))
        else:
            self.delete_playlist()


class TextForm(QWidget):
    def __init__(self, *args):
        #Форма для отображения текста выбранного аудиофайла
>>>>>>> master
        super().__init__()
        self.setupUI(args)

    def setupUI(self, args):
<<<<<<< HEAD
        self.setGeometry(300, 300, 640, 480)
=======
        self.setGeometry(300, 300, 800, 600)
>>>>>>> master
        self.setWindowTitle('Текст')
        self.txt = QTextEdit(self)
        self.txt.setText(args[-1])
        self.txt.setReadOnly(True)
        self.txt.resize(640, 480)


class ErrorForm(QWidget):
    def __init__(self):
        # Форма для ошибки аудиофайла с неправильной директорией
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(300, 300, 350, 50)
        self.setWindowTitle('Ошибка')
        self.txt = QLabel(self)
        self.txt.setText(f'Ошибка. Задан неправильный путь к аудиофайлу(ам).')
        self.txt.resize(350, 50)


class ErrorForm(QWidget):
    def __init__(self):
        #Форма для ошибки аудиофайла с неправильной директорией
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(300, 300, 350, 50)
        self.setWindowTitle('Ошибка')
        self.txt = QLabel(self)
        self.txt.setText(f'Ошибка. Задан неправильный путь к аудиофайлу(ам).')
        self.txt.resize(350, 50)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Player()
    ex.show()
    sys.exit(app.exec())