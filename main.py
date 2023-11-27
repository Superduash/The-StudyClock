import sys, os, subprocess, random
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QSlider, QLabel, QPushButton, QDialog
from PyQt5.QtCore import Qt, QUrl, QProcess, QPropertyAnimation
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5 import uic
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.set_volume(1.0)
        self.music_folder = "music"
        self.music_files = [f for f in os.listdir(self.music_folder) if f.endswith(".mp3")]
        self.current_media_index = -1

    def play_random_music(self):
        if not self.music_files:
            QMessageBox.warning(None, "Error", "No music files found.")
            return

        new_index = random.randint(0, len(self.music_files) - 1)
        while new_index == self.current_media_index:
            new_index = random.randint(0, len(self.music_files) - 1)

        self.current_media_index = new_index
        selected_music = self.music_files[new_index]
        music_path = os.path.join(self.music_folder, selected_music)

        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play()

            title = selected_music  # Use the filename as the title for simplicity
            print(f"Now playing: {title}")
        except Exception as e:
            print("Error", f"An error occurred: {str(e)}")

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def stop_music(self):
        pygame.mixer.music.stop()

class CreditsDialog(QDialog):
    def __init__(self, parent=None):
        super(CreditsDialog, self).__init__(parent)
        uic.loadUi('ui/credits.ui', self)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.load_ui()
        self.setup_ui_elements()
        self.setup_animations()
        self.sound_effect = QSoundEffect(self)
        self.sound_effect.setSource(QUrl.fromLocalFile("resources/click.wav"))
        self.subprocesses = {}
        self.process = QProcess(self)
        self.force_close_triggered = False

        # Creating the music player after the application instance
        self.music_player = MusicPlayer()

    def load_ui(self):
        from PyQt5 import uic
        uic.loadUi('ui/main.ui', self)

    def setup_ui_elements(self):
        self.credits.clicked.connect(self.show_credits)
        self.music.clicked.connect(self.toggle_music)
        self.pauseplay.clicked.connect(self.pause_play)
        self.twentytimer.clicked.connect(lambda: self.open_subprocess("twenty_timer", ["python", "202020.py"]))
        self.studyfocus.clicked.connect(lambda: self.open_subprocess("study_focus", ["python", "studyfocus.py"]))
        self.taskbuddy.clicked.connect(lambda: self.open_subprocess("task_buddy", ["python", "todolistgui.py"]))
        self.forceclose.clicked.connect(self.force_close_all)

        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setFixedSize(self.size())

        self.volume_slider = self.findChild(QSlider, "volume")
        if self.volume_slider:
            self.volume_slider.setValue(100)
            self.volume_slider.valueChanged.connect(self.adjust_volume)
        self.comingsoon.setEnabled(False)

        fact_label = self.findChild(QLabel, "facts")
        if fact_label:
            random_fact = self.get_random_fact()
            fact_label.setText(random_fact)
        self.reload_button = self.findChild(QPushButton, "reload")
        if self.reload_button:
            self.reload_button.clicked.connect(self.reload_fact)

        self.fact_label = self.findChild(QLabel, "facts")
        if self.fact_label:
            self.display_random_fact()

    def reload_fact(self):
        self.play_click_sound()
        self.display_random_fact()

    def display_random_fact(self):
        random_fact = self.get_random_fact()
        self.fact_label.setText(random_fact)

    def get_random_fact(self):
        from facts import study_facts
        return random.choice(study_facts)

    def setup_animations(self):
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setDuration(500)
        self.fade_in_animation.start()

    def play_click_sound(self):
        self.sound_effect.play()

    def show_credits(self):
        self.play_click_sound()
        credits_dialog = CreditsDialog(self)
        credits_dialog.exec_()

    def toggle_music(self):
        self.play_click_sound()
        try:
            self.music_player.play_random_music()
        except Exception as e:
            print("Error", f"An error occurred: {str(e)}")

    def pause_play(self):
        self.play_click_sound()
        try:
            pygame.mixer.music.pause() if pygame.mixer.music.get_busy() else pygame.mixer.music.unpause()
        except Exception as e:
            print("Error", f"An error occurred: {str(e)}")

    def adjust_volume(self, value):
        volume = value / 100.0
        self.music_player.set_volume(volume)

    def open_subprocess(self, key, command):
        self.play_click_sound()
        if key in self.subprocesses and self.subprocesses[key].poll() is None:
            return
        self.subprocesses[key] = subprocess.Popen(command)

    def force_close_all(self):
        self.play_click_sound()
        for _, subprocess_instance in self.subprocesses.items():
            if subprocess_instance and subprocess_instance.poll() is None:
                subprocess_instance.terminate()
                subprocess_instance.wait()
        sys.exit()

    def closeEvent(self, event):
        if self.force_close_triggered:
            for _, subprocess_instance in self.subprocesses.items():
                if subprocess_instance and subprocess_instance.poll() is None:
                    subprocess_instance.terminate()
                    subprocess_instance.wait()
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
