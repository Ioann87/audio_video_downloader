import sys

import humanize
import pafy
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

ui, _ = loadUiType("main.ui")


class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.init_ui()
        self.handle_buttons()

    def init_ui(self):
        pass

    def handle_buttons(self):
        # Audio buttons
        self.pushButton_3.clicked.connect(self.get_audio_data)
        self.pushButton_2.clicked.connect(self.save_browse_audio)
        self.pushButton.clicked.connect(self.download_audio)

        # Video buttons
        self.pushButton_4.clicked.connect(self.get_video_data)
        self.pushButton_6.clicked.connect(self.save_browse_video)
        self.pushButton_5.clicked.connect(self.download_video)

    ################################################################################################
    # Audio
    def get_audio_data(self):
        audio_url = self.lineEdit.text()
        if audio_url == '':
            QMessageBox.warning(self, "Enter a URL")
        else:

            video = pafy.new(audio_url)

            audio_streams = video.audiostreams
            for stream in audio_streams:
                size = humanize.naturalsize(stream.get_filesize())

                data = f"{stream.bitrate} {stream.extension} {size} "
                self.comboBox.addItem(data)

    def save_browse_audio(self):
        save_path = QFileDialog.getSaveFileName(self,
                                                caption="Save as",
                                                directory=".",
                                                filter="All Files(*.*)")
        self.lineEdit_2.setText(str(save_path[0]))

    def audio_progress(self, total, received, ratio, rate, time):
        read_data = received
        if total > 0:
            download_percentage = read_data * 100 / total
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()

    def download_audio(self):
        download_url = self.lineEdit.text()
        save_path = self.lineEdit_2.text()

        if download_url == '':
            QMessageBox.warning(self, "Enter a URL")

        elif save_path == '':
            QMessageBox.warning(self, "Choose location")
        else:
            video = pafy.new(download_url)
            audio_streams = video.audiostreams
            audio_quality = self.comboBox.currentIndex()
            audio_streams[audio_quality].download(filepath=save_path, callback=self.audio_progress)

        QMessageBox.information(self, "Download Completed", "Successfully")

        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.progressBar.setValue(0)
        self.comboBox.clear()

    ###############################################################################################
    #  YOUTUBE Video

    def get_video_data(self):
        video_url = self.lineEdit_3.text()

        if video_url == '':
            QMessageBox.warning(self, "Enter a URL")
        else:

            video = pafy.new(video_url)

            video_streams = video.videostreams
            for stream in video_streams:
                size = humanize.naturalsize(stream.get_filesize())
                data = f"{stream.mediatype} {stream.extension} {stream.quality} {size}"
                self.comboBox_2.addItem(data)

    def video_progress(self, total, received, ratio, rate, time):
        read_data = received
        if total > 0:
            download_percentage = read_data * 100 / total
            self.progressBar_2.setValue(download_percentage)
            QApplication.processEvents()

    def download_video(self):
        download_url = self.lineEdit_3.text()
        save_path = self.lineEdit_4.text()

        if download_url == '':
            QMessageBox.warning(self, "Enter a URL")
        elif save_path == '':
            QMessageBox.warning(self, "Choose location")
        else:
            video = pafy.new(download_url)
            video_streams = video.videostreams
            video_quality = self.comboBox_2.currentIndex()
            video_streams[video_quality].download(filepath=save_path, callback=self.video_progress)

        QMessageBox.information(self, "Download Completed", "Successfully")

        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.progressBar_2.setValue(0)
        self.comboBox_2.clear()

    def save_browse_video(self):
        save_path = QFileDialog.getSaveFileName(self,
                                                caption="Save as",
                                                directory=".",
                                                filter="All Files(*.*)")
        self.lineEdit_4.setText(str(save_path[0]))


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
