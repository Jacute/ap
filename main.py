import sys
import os
from functools import partial
from random import shuffle
import traceback
from functools import partial

from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.flac import FLAC
from mutagen import MutagenError
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTextEdit, QFileDialog, \
    QInputDialog, QAction, QLabel
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import *
from PyQt5 import uic


def time(ms):
    # Расчёт длительности аудиофайла

    h, r = divmod(ms, 3600000)
    m, r = divmod(r, 60000)
    s, _ = divmod(r, 1000)

    return ("%d:%02d" % (m,s) if h == 0 else "%d:%02d:%02d" % (h,m,s))


class Player(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.abspath('static/audioplayer.ui'), self)

        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)
        self.player.setVolume(50)
        self.setFixedWidth(1024)
        self.setFixedHeight(778)

        self.list_of_ways_to_files = list()
        self.list_of_names_of_playlists = list()
        self.list_of_tracks_of_playlists = list()

        border_path = os.path.abspath('static/border.png')
        self.border_pic = QPixmap(border_path)
        self.border.setPixmap(self.border_pic)
        self.album_pic.hide()

        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('Audioplayer')
        self.statusbarMessage = QLabel()
        self.statusBar().addWidget(self.statusbarMessage)

        self.check_playlists()
        self.add_track.triggered.connect(self.add)
        self.add_folder.triggered.connect(self.add_directory)
        self.delete_track.triggered.connect(self.delete)
        self.play.clicked.connect(self.play_player)
        self.pause.clicked.connect(self.pause_player)
        self.clear.triggered.connect(self.delete_all)
        self.mix_tracks.triggered.connect(self.mix)
        self.next.clicked.connect(self.next_song)
        self.previous.clicked.connect(self.previous_song)
        self.stop.clicked.connect(self.stop_player)
        self.volume_slider.valueChanged[int].connect(self.change_vol)
        self.player.durationChanged.connect(self.update_duration)
        self.player.positionChanged.connect(self.update_position)
        self.time_slider.valueChanged[int].connect(self.change_pos)
        self.add_tracks_to_playlist.triggered.connect(self.add_new_playlist)
        self.del_playlist.triggered.connect(self.delete_playlist)
        self.list_of_songs.itemDoubleClicked.connect(self.play_choosing_song)

    def add(self, fnames):
        if not fnames:
            # Диалоговое окно для выбора аудиофайлов
            fnames = QFileDialog.getOpenFileNames(
                self, 'Выбрать аудиофайл', '',
                'Аудиофайл (*.mp3 *.wav *.flac)')[0]
        try:
            if fnames != ['']:
                for i in fnames:
                    self.list_of_songs.addItem('{} - {}'.format(
                        *self.get_metadata(i)
                    ))
                    self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(i)))
                self.list_of_ways_to_files.extend(fnames)
        except MutagenError:
            self.error = ErrorForm(traceback.format_exc())
            print(traceback.format_exc())
            self.error.show()

    def add_directory(self):
        # Диалоговое окно для выбора каталога
        dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        if dirlist != '':
            all_files = os.listdir(dirlist)  # Все файлы в выбранной директории
            audiofiles = [dirlist + '/' + i for i in list(filter(lambda x: x.endswith('.mp3') or
                                                                           x.endswith('.wav') or
                                                                           x.endswith('.flac'), all_files))]
            self.add(audiofiles)

    def mix(self):
        # Перемешивание
        self.playlist.clear()
        self.list_of_songs.clear()
        shuffle(self.list_of_ways_to_files)
        for i in self.list_of_ways_to_files:
            self.list_of_songs.addItem(f'{self.get_metadata(i)[0]} - {self.get_metadata(i)[1]}')
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(i)))
        self.now_playing_track()

    def delete(self):
        # Удаление выбранных аудиофайлов из плейлиста
        items = self.list_of_songs.selectedItems()
        for item in items:
            index = self.list_of_songs.row(item)
            self.list_of_songs.takeItem(index)
            self.playlist.removeMedia(index)
            del self.list_of_ways_to_files[index]
            self.now_playing_track()

    def delete_all(self):
        # Удаление плейлиста полностью
        self.playlist.clear()
        self.list_of_songs.clear()
        self.list_of_ways_to_files = list()
        self.now_playing_track()

    def play_player(self):
        # Проигрывание
        self.list_of_songs.setCurrentRow(self.playlist.currentIndex())
        self.player.play()

    def play_choosing_song(self):
        index = self.list_of_songs.currentRow()
        self.playlist.setCurrentIndex(index)
        self.play_player()

    def pause_player(self):
        # Пауза
        self.player.pause()

    def stop_player(self):
        # Остановка плеера
        self.player.stop()

    def next_song(self):
        # Переключение на следующий аудиофайл
        self.playlist.next()
        self.list_of_songs.setCurrentRow(self.playlist.currentIndex())
        self.now_playing_track()

    def previous_song(self):
        # Переключение на предыдущий аудиофайл
        self.playlist.previous()
        self.list_of_songs.setCurrentRow(self.playlist.currentIndex())
        self.now_playing_track()

    def change_vol(self):
        # Изменение громкости
        self.player.setVolume(self.volume_slider.value())

    def update_duration(self, duration):
        # Вывод длительности аудиофайла
        self.time_slider.setMaximum(duration)
        self.end_time.setText(time(duration))

    def update_position(self, position):
        # Изменение позиции QSlider'а по мере продвижения аудиофайла
        if position >= 0:
            self.play_time.setText(time(position))
            self.now_playing_track()

        self.time_slider.blockSignals(True)
        self.time_slider.setValue(position)
        self.time_slider.blockSignals(False)

    def change_pos(self):
        # Изменение позиции плеера по мере продвижения QSlider'а (перемотка)
        if self.player.duration() != self.player.position() and self.player.duration() != 0:
            self.player.setPosition(self.time_slider.value())

    def now_playing_track(self):
        # Вывод информации о песне, которая играет в данный момент
        if self.playlist.isEmpty() or not self.player.isSeekable():
            self.setWindowTitle('Audioplayer')
            self.end_time.setText('0:00')
            self.statusbarMessage.setText("")
            self.album_pic.hide()
        else:
            song = self.list_of_ways_to_files[self.playlist.currentIndex()]
            self.setWindowTitle(f'{self.get_metadata(song)[0]} - {self.get_metadata(song)[1]}')
            self.statusbarMessage.setText('Исполнитель: {}. Название: {}. Альбом: {}. Жанр: {}. Дата: {}.'.format(
                *self.get_metadata(song)))
            self.getting_album_pic(song)

    def get_metadata(self, file):
        if file.endswith('.mp3'):
            audio = MP3(file)  # Считывание всех метаданных
        elif file.endswith('.wav'):
            audio = WAVE(file)
        elif file.endswith('.flac'):
            audio = FLAC(file)
        '''TDRC (год), TALB (альбом), TIT2 (название трека),
        TPE1 (исполнитель), TCON (жанр), COMM:XXX (текст), APIC (обложка альбома)'''
        if 'TIT2' in audio:
            title = str(audio['TIT2'])
        elif 'title' in audio:
            title = str(audio['title'][0])
        else:
            title = 'Unknown title'
        if 'TPE1' in audio:
            artist = str(audio['TPE1'])
        elif 'artist' in audio:
            artist = str(audio['artist'][0])
        else:
            artist = 'Unknown musician'
        if 'TDRC' in audio:
            date = str(audio['TDRC'])
        elif 'date' in audio:
            date = str(audio['date'][0])
        else:
            date = 'Unknown date'
        if 'TALB' in audio:
            album = str(audio['TALB'])
        elif 'album' in audio:
            album = str(audio['album'][0])
        else:
            album = 'Unknown album'
        if 'TCON' in audio:
            genre = str(audio['TCON'])
        elif 'genre' in audio:
            genre = str(audio['genre'][0])
        else:
            genre = 'Unknown genre'
        return [artist, title, album, genre, date]

    def getting_album_pic(self, file):
        # Получение обложки альбома из метаданных
        cover_name = 'cover.png'
        cover_key = ''
        if file.endswith('.mp3'):
            audio = MP3(file)  # Считывание всех метаданных
        elif file.endswith('.wav'):
            audio = WAVE(file)
        elif file.endswith('.flac'):
            audio = FLAC(file)
        for i in audio.keys():
            if i.startswith('APIC'):
                cover_key = i  # Получение правильного ключа с обложкой
        if cover_key != '':
            cover_binary = audio[cover_key]
            with open(cover_name, mode="wb") as cover:
                cover.write(cover_binary.data)
            cover = QPixmap(cover_name)
            cover = cover.scaled(250, 250)
            self.album_pic.setPixmap(cover)
            self.album_pic.show()
            os.remove('cover.png')
        else:
            self.album_pic.hide()

    def add_new_playlist(self):
        # Добавление плейлиста
        title, ok_pressed = QInputDialog.getText(
            self, "Плейлист", 'Введите название плейлиста')
        with open('static/playlists.txt', mode='a+', encoding='utf-8') as txt_of_playlists:
            if ok_pressed:
                all_files = "\n".join(self.list_of_ways_to_files)
                txt_of_playlists.write(f'{title}\n{all_files}\n\n')
        self.check_playlists()

    def download_playlist(self):
        # Загрузка плейлиста на QListWidget
        self.delete_all()
        name = self.sender().text()
        ind = self.list_of_names_of_playlists.index(name)
        fnames = self.list_of_tracks_of_playlists[ind]
        self.add(*fnames)

    def check_playlists(self):
        # Проверка playlists.txt на наличие плейлистов
        with open('static/playlists.txt', mode='r', encoding='utf-8') as txt_of_playlists:
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
        # Удаление плейлиста
        title, ok_pressed = QInputDialog.getText(
            self, "Плейлист", 'Введите название плейлиста')
        if title in self.list_of_names_of_playlists:
            with open('static/playlists.txt', mode='a+', encoding='utf-8') as txt_of_playlists:
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


class ErrorForm(QWidget):
    def __init__(self, error):
        # Форма для ошибки аудиофайла с неправильной директорией
        super().__init__()
        self.error = error
        self.setupUI()

    def setupUI(self):
        self.setGeometry(300, 300, 440, 440)
        self.setWindowTitle('Ошибка')
        self.txt = QLabel(self)
        self.txt.setText(self.error)
        self.txt.resize(440, 440)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Player()
    ex.show()
    sys.exit(app.exec())
