import sys
import pafy

from random import shuffle
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog
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
        uic.loadUi('online_audioplayer.ui', self)
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)
        self.list_of_videos = list()
        self.player.setVolume(50)
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('Online Audioplayer')
        self.add_url.triggered.connect(self.add)
        self.delete_track.triggered.connect(self.delete)
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

    def add(self):
        url, ok_pressed = QInputDialog.getText(
            self, "Введите url видео на YouTube'е", 'YouTube URL',)
        try:
            if ok_pressed:
                video = pafy.new(url)
                best = video.getbestaudio()
                name = video.title
                playurl = best.url
                self.playlist.addMedia(QMediaContent(QUrl(playurl)))
                self.list_of_songs.addItem(name)
                self.list_of_videos.append(video)
        except:
            self.add()


    def mix(self):
        #Перемешивание
        self.playlist.clear()
        self.list_of_songs.clear()
        shuffle(self.list_of_videos)
        for video in self.list_of_videos:
            best = video.getbestaudio()
            name = video.title
            playurl = best.url
            self.list_of_songs.addItem(name)
            self.playlist.addMedia(QMediaContent(QUrl(playurl)))
        self.setWindowTitle('Online Audioplayer')

    def delete(self):
        #Удаление выбранных аудиофайлов из плейлиста
        items = self.list_of_songs.selectedItems()
        for item in items:
            index = self.list_of_songs.row(item)
            self.list_of_songs.takeItem(index)
            self.playlist.removeMedia(index)
            del self.list_of_videos[index]
            self.now_playing_track()

    def delete_all(self):
        #Удаление плейлиста полностью
        self.playlist.clear()
        self.list_of_songs.clear()
        self.list_of_videos = list()
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
        if self.playlist.isEmpty():
            self.setWindowTitle('Online Audioplayer')
            self.end_time.setText('0:00')
        else:
            video = self.list_of_videos[self.playlist.currentIndex()]
            self.setWindowTitle(video.title)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Player()
    ex.show()
    sys.exit(app.exec())