import sys
import os

from mutagen.mp3 import MP3
from random import shuffle
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QTextEdit
from PyQt5.QtCore import QUrl
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
        self.play.clicked.connect(self.play_playlist)
        self.pause.clicked.connect(self.pause_playlist)
        self.clear_playlist.triggered.connect(self.delete_all)
        self.mix_playlist.triggered.connect(self.mix)
        self.next.clicked.connect(self.next_song)
        self.previous.clicked.connect(self.previous_song)
        self.stop.clicked.connect(self.stop_playlist)
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
        self.playlist.clear()
        self.list_of_songs.clear()
        shuffle(self.list_of_ways_to_files)
        for i in self.list_of_ways_to_files:
            self.list_of_songs.addItem(self.get_title(i))
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(i)))
        self.setWindowTitle('Audioplayer')

    def delete(self):
        items = self.list_of_songs.selectedItems()
        for item in items:
            index = self.list_of_songs.row(item)
            self.list_of_songs.takeItem(index)
            self.playlist.removeMedia(index)
            del self.list_of_ways_to_files[index]
            self.now_playing_track()

    def delete_all(self):
        self.playlist.clear()
        self.list_of_songs.clear()
        self.list_of_ways_to_files = list()
        self.now_playing_track()

    def play_playlist(self):
        self.player.play()
        self.now_playing_track()

    def pause_playlist(self):
        self.player.pause()

    def stop_playlist(self):
        self.player.stop()

    def next_song(self):
        self.playlist.next()
        self.now_playing_track()

    def previous_song(self):
        self.playlist.previous()
        self.now_playing_track()

    def change_vol(self):
        self.player.setVolume(self.volume_slider.value())

    def update_duration(self, duration):
        self.time_slider.setMaximum(duration)
        self.end_time.setText(time(duration))

    def update_position(self, position):
        if position > 0:
            self.now_playing_track()
        self.play_time.setText(time(position))
        self.time_slider.setValue(position)

    def change_pos(self):
        if self.player.duration() != self.player.position() and self.player.duration() != 0:
            self.player.setPosition(self.time_slider.value())

    def now_playing_track(self):
        if self.playlist.isEmpty():
            self.setWindowTitle('Audioplayer')
        else:
            track = self.list_of_ways_to_files[self.playlist.currentIndex()]
            self.setWindowTitle(self.get_title(track))
            self.statusBar().showMessage(self.check_info_about_song(track))

    def get_title(self, file):
        audio = MP3(file)
        '''TDRC (год) TALB (альбом) TIT2 (название трека)
        TPE1 (исполнитель) TCON (жанр) COMM:XXX (текст)'''
        if audio == {}:
            return 'Unknown artist - Unknown title'
        elif 'TIT2' in audio and 'TPE1' not in audio:
            title = audio['TIT2']
            return f'Unknown artist - {title}'
        elif 'TIT2' not in audio and 'TPE1' in audio:
            artist = audio['TPE1']
            return f'{artist} - Unknown title'
        else:
            title = audio['TIT2']
            artist = audio['TPE1']
            return f'{artist} - {title}'

    def check_info_about_song(self, file):
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
        return f'Исполнитель: {artist}. Название: {artist}. Альбом: {album}. Жанр: {genre}.' \
               f' Год: {year}.'

    def check_text_of_song(self):
        audio = MP3(self.list_of_ways_to_files[self.list_of_songs.currentRow()])
        if 'COMM::XXX' in audio:
            self.text = str(audio['COMM::XXX'])
        else:
            self.text = 'Unknown text'
        self.form_for_text = SecondForm(self, self.text)
        self.form_for_text.show()


class SecondForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
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