import sys
import os
import pafy

from mutagen.mp3 import MP3
from random import shuffle
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTextEdit, QFileDialog, QInputDialog
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import *
from PyQt5 import uic


def time(ms):
    #Расчёт длительности трека
    h, r = divmod(ms, 3600000)
    m, r = divmod(r, 60000)
    s, _ = divmod(r, 1000)
    return ("%d:%02d" % (m,s) if h == 0 else "%d:%02d:%02d" % (h,m,s))


class Player(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('audioplayer.ui', self)
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)
        self.list_of_ways_to_files = list()
        self.player.setVolume(50)
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('Audioplayer')
        self.add_track.triggered.connect(self.add)
        self.add_folder.triggered.connect(self.add_directory)
        self.delete_track.triggered.connect(self.delete)
        self.check_text.triggered.connect(self.check_text_of_song)
        self.play.clicked.connect(self.play_player)
        self.pause.clicked.connect(self.pause_player)
        self.clear_playlist.triggered.connect(self.delete_all)
        self.mix_playlist.triggered.connect(self.mix)
        self.next.clicked.connect(self.next_song)
        self.previous.clicked.connect(self.previous_song)
        self.stop.clicked.connect(self.stop_player)
        self.volume_slider.valueChanged[int].connect(self.change_vol)
        self.player.durationChanged.connect(self.update_duration)
        self.player.positionChanged.connect(self.update_position)
        self.time_slider.valueChanged[int].connect(self.change_pos)

    def add(self, fnames):
        if fnames == False:
            fnames = QFileDialog.getOpenFileNames(
                self, 'Выбрать аудиофайл', '',
                'Аудиофайл (*.mp3)')[0]
        if fnames != ['']:
            for i in fnames:
                self.list_of_songs.addItem(self.get_title(i))
                self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(i)))
            self.list_of_ways_to_files.extend(fnames)

    def add_directory(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        if dirlist != '':
            all_files = os.listdir(dirlist)
            audiofiles = [dirlist + '/' + i for i in list(filter(lambda x: x.endswith('.mp3'), all_files))]
            self.add(audiofiles)

    def mix(self):
        #Перемешивание
        self.playlist.clear()
        self.list_of_songs.clear()
        shuffle(self.list_of_ways_to_files)
        for i in self.list_of_ways_to_files:
            self.list_of_songs.addItem(self.get_title(i))
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(i)))
        self.setWindowTitle('Audioplayer')
        self.now_playing_track()

    def delete(self):
        #Удаление выбранных аудиофайлов из плейлиста
        items = self.list_of_songs.selectedItems()
        for item in items:
            index = self.list_of_songs.row(item)
            self.list_of_songs.takeItem(index)
            self.playlist.removeMedia(index)
            del self.list_of_ways_to_files[index]
            self.now_playing_track()

    def delete_all(self):
        #Удаление плейлиста полностью
        self.playlist.clear()
        self.list_of_songs.clear()
        self.list_of_ways_to_files = list()
        self.now_playing_track()

    def play_player(self):
        #Проигрывание
        self.player.play()
        self.now_playing_track()

    def pause_player(self):
        #Пауза
        self.player.pause()

    def stop_player(self):
        #Остановка плеера
        self.player.stop()

    def next_song(self):
        # Переключение на следующий аудиофайл
        self.playlist.next()
        self.now_playing_track()

    def previous_song(self):
        #Переключение на предыдущий аудиофайл
        self.playlist.previous()
        self.now_playing_track()

    def change_vol(self):
        #Изменение громкости
        self.player.setVolume(self.volume_slider.value())

    def update_duration(self, duration):
        #Вывод длительности аудиофайла
        self.time_slider.setMaximum(duration)
        self.end_time.setText(time(duration))

    def update_position(self, position):
        #Изменение позиции QSlider'а по мере продвижения аудиофайла
        if position > 0:
            self.now_playing_track()
        self.play_time.setText(time(position))
        self.time_slider.setValue(position)

    def change_pos(self):
        #Изменение позиции плеера по мере продвижения QSlider'а (перемотка)
        if self.player.duration() != self.player.position() and self.player.duration() != 0:
            self.player.setPosition(self.time_slider.value())

    def now_playing_track(self):
        #Вывод всяческой информации о песне, которая играет в данный момент
        if self.playlist.isEmpty() or not self.player.isSeekable():
            self.setWindowTitle('Audioplayer')
            self.end_time.setText('0:00')
            self.album_pic.hide()
        else:
            track = self.list_of_ways_to_files[self.playlist.currentIndex()]
            self.setWindowTitle(self.get_title(track))
            self.statusBar().showMessage(self.check_info_about_song(track))
            self.getting_album_pic(track)

    def get_title(self, file):
        #Получение  заголовка для окна
        audio = MP3(file)
        '''TDRC (год), TALB (альбом), TIT2 (название трека),
        TPE1 (исполнитель), TCON (жанр), COMM:XXX (текст), APIC (обложка альбома)'''
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
        #Получение всей основной информации о песне из метаданных
        audio = MP3(file)
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
        #Получение обложки альбома из метаданных
        cover_name = 'cover.png'
        audio = MP3(track)
        if 'APIC:Cover' in audio:
            cover_binary = audio['APIC:Cover']
            with open(cover_name, mode="wb") as cover:
                cover.write(cover_binary.data)
            cover = QPixmap(cover_name)
            cover = cover.scaled(251, 251)
            self.album_pic.setPixmap(cover)
            self.album_pic.show()
        else:
            self.album_pic.hide()

    def check_text_of_song(self):
        #Просмотр текста песни из метаданных
        audio = MP3(self.list_of_ways_to_files[self.list_of_songs.currentRow()])
        if 'COMM::XXX' in audio:
            self.text = str(audio['COMM::XXX'])
        else:
            self.text = 'Unknown text'
        self.form_for_text = SecondForm(self, self.text)
        self.form_for_text.show()


class SecondForm(QWidget):
    def __init__(self, *args):
        #Вторая форма для отображения текста выбранного аудиофайла
        super().__init__()
        self.setupUI(args)

    def setupUI(self, args):
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Текст')
        self.txt = QTextEdit(self)
        self.txt.setText(args[-1])
        self.txt.setReadOnly(True)
        self.txt.resize(800, 600)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Player()
    ex.show()
    sys.exit(app.exec())