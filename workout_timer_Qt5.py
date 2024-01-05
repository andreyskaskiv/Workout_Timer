import sys
from typing import Any

import winsound
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QProgressBar, \
    QLineEdit, QTabWidget, QFormLayout


class WorkoutTimer:
    """
    The WorkoutTimer class is a timer for interval training.
    It allows you to set the duration of work, rest and number of repetitions.
    """

    def __init__(self, work_duration: int, rest_duration: int, repetitions: int):
        self.work_duration = work_duration * 60
        self.rest_duration = rest_duration * 60
        self.initial_repetitions = repetitions
        self.repetitions = repetitions
        self.current_stage = 'Work ==>'
        self.current_time = self.work_duration
        self.running = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.countdown)

    def start(self):
        """
        Starts the timer.
        """
        if not self.running:
            self.running = True
            self.timer.start(1000)

    def countdown(self):
        """
        Counts down the current time.
        """
        if self.running and self.current_time > 0 and self.repetitions > 0:
            self.current_time -= 1
        elif self.running and self.repetitions > 0:
            self.switch_stage()
            self.repetitions -= 1

    def switch_stage(self):
        """
        Switches between the 'Work ==>' and 'Rest ==>' stages.
        """
        if self.current_stage == 'Work ==>':
            self.current_stage = 'Rest ==>'
            self.current_time = self.rest_duration
        else:
            self.current_stage = 'Work ==>'
            self.current_time = self.work_duration

    def stop(self):
        """
        Stops the timer and resets the current stage, current time, and repetitions.
        """
        self.running = False
        self.current_stage = 'Work ==>'
        self.current_time = self.work_duration
        self.repetitions = self.initial_repetitions

    def pause(self):
        """
        Pauses or resumes the timer.
        """
        if self.running:
            self.timer.stop()
        else:
            self.timer.start(1000)
        self.running = not self.running

    def next(self):
        """
        Skips to the next stage or repetition.
        """
        if self.running and self.repetitions > 0:
            self.switch_stage()
            self.repetitions -= 1

    def back(self):
        """
        Goes back to the previous stage or repetition.
        """
        if self.running and self.repetitions < self.initial_repetitions:
            self.repetitions += 1
            self.switch_stage()


class Interface(QWidget):
    def __init__(self, timer: Any) -> None:
        super().__init__()

        # Timer object
        self.timer = timer

        # Create tabs
        self.tab_widget = QTabWidget()

        # Create first tab
        self.tab1 = QWidget()
        self.tab_widget.addTab(self.tab1, "Timer")

        # Create second tab
        self.tab2 = QWidget()
        self.tab_widget.addTab(self.tab2, "Settings")

        # Create vertical layout for widgets
        layout1 = QVBoxLayout(self.tab1)

        # Create label to display current state
        self.state_label = QLabel('Work')
        layout1.addWidget(self.state_label, alignment=Qt.AlignCenter)

        # Create label to display time
        self.time_label = QLabel('00:00:00')
        layout1.addWidget(self.time_label, alignment=Qt.AlignCenter)

        # Create progress bar to visualize elapsed time
        self.progress_bar = QProgressBar()
        layout1.addWidget(self.progress_bar)

        # Create labels to display number of repetitions
        repetitions_label = QLabel('Repetitions:')
        self.repetitions_layout = QHBoxLayout()
        for _ in range(self.timer.initial_repetitions):
            dot_label = QLabel('•')
            self.repetitions_layout.addWidget(dot_label)
        repetitions_layout = QHBoxLayout()
        repetitions_layout.addWidget(repetitions_label)
        repetitions_layout.addLayout(self.repetitions_layout)
        layout1.addLayout(repetitions_layout)

        # Create buttons for Start and Pause
        start_button = QPushButton('Start')
        start_button.clicked.connect(self.start_timer)
        pause_button = QPushButton('Pause')
        pause_button.clicked.connect(self.pause_timer)
        start_pause_layout = QHBoxLayout()
        start_pause_layout.addWidget(start_button)
        start_pause_layout.addWidget(pause_button)
        layout1.addLayout(start_pause_layout)

        # Create buttons for Back, Stop and Next
        back_button = QPushButton('Back')
        back_button.clicked.connect(self.back_stage)
        stop_button = QPushButton('Stop')
        stop_button.clicked.connect(self.stop_timer)
        next_button = QPushButton('Next')
        next_button.clicked.connect(self.next_stage)
        button_layout = QHBoxLayout()
        button_layout.addWidget(back_button)
        button_layout.addWidget(stop_button)
        button_layout.addWidget(next_button)
        layout1.addLayout(button_layout)

        # Create form for input values on second tab
        layout2 = QFormLayout(self.tab2)
        self.work_duration_input = QLineEdit(str(self.timer.work_duration // 60))
        self.rest_duration_input = QLineEdit(str(self.timer.rest_duration // 60))
        self.repetitions_input = QLineEdit(str(self.timer.initial_repetitions))
        layout2.addRow('Work Duration (minutes):', self.work_duration_input)
        layout2.addRow('Rest Duration (minutes):', self.rest_duration_input)
        layout2.addRow('Repetitions:', self.repetitions_input)
        apply_button = QPushButton('Apply')
        apply_button.clicked.connect(self.apply_settings)
        layout2.addRow(apply_button)

        # Set main layout of the window
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.tab_widget)

        # Update label every second
        self.timer.timer.timeout.connect(self.update_time_label)
        self.timer.timer.timeout.connect(self.update_state_label)
        self.timer.timer.timeout.connect(self.update_repetitions_label)
        self.timer.timer.timeout.connect(self.update_progress_bar)

        # Set styles
        self.setStyleSheet("""
                   QWidget {
                       background-color: #2F3136;
                       color: #FFFFFF;
                       font-size: 18px;
                   }
                   QPushButton {
                       background-color: #2F4F4F;
                       border: none;
                       border-radius: 4px;
                       padding: 10px;
                       min-width: 100px;
                       font-size: 20px;
                       font-weight: bold;
                   }
                   QPushButton:hover {
                       background-color: #677BC4;
                   }
                   QPushButton:pressed {
                       background-color: #2F4F4F;
                   }
                   QLineEdit {
                       background-color: #3f3f3f;
                       border: none;
                       border-radius: 4px;
                       padding: 5px;
                       color: #FFFFFF;
                   }
                   QProgressBar {
                       border: 2px solid grey;
                       border-radius: 5px;
                       text-align: center;
                   }
                   QProgressBar::chunk {
                       background-color: #05B8CC;
                       width: 20px;
                       margin: 0.5px;
                   }
                   QLabel {
                       font-size: 22px;
                       font-weight: bold;
                   }
                   QTabBar::tab:selected {
                       background: #2F4F4F;
                       border: 2px solid #FFFFFF;
                       border-radius: 4px;
                       box-shadow: 0 0 10px #FFFFFF;
                       min-width: 150px;  
                   }
                   QTabBar::tab:!selected {
                       background: #696969;
                       border: 2px solid #FFFFFF;
                       border-radius: 4px;
                       box-shadow: 0 0 10px #FFFFFF;
                       min-width: 150px;  
                   }
               """)

    def start_timer(self) -> None:
        self.timer.start()

    def stop_timer(self) -> None:
        self.timer.stop()

    def pause_timer(self) -> None:
        self.timer.pause()

    def next_stage(self) -> None:
        self.timer.next()

    def back_stage(self) -> None:
        self.timer.back()

    def update_time_label(self) -> None:
        """
        Updates the time label.
        """
        time = QTime(0, 0).addSecs(self.timer.current_time)
        self.time_label.setText(time.toString())

        # If less than 5 seconds are left on the timer, play a sound notification
        if self.timer.current_time < 5:
            winsound.Beep(300, 100)

    def update_state_label(self) -> None:
        """
        Updates the state label.
        """
        if self.timer.current_stage == 'Work ==>':
            self.state_label.setText('Work')
            self.state_label.setStyleSheet("color: #00FF00;")
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #00FF00; }")
        else:
            self.state_label.setText('Rest')
            self.state_label.setStyleSheet("color: yellow;")
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: yellow; }")

    def update_repetitions_label(self) -> None:
        """
        Updates the repetitions labels.
        """
        # First, delete all current tags
        while self.repetitions_layout.count():
            item = self.repetitions_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # Then we add labels according to the current number of repetitions
        for _ in range(self.timer.repetitions):
            dot_label = QLabel('•')
            self.repetitions_layout.addWidget(dot_label)

    def update_progress_bar(self) -> None:
        """
        Updates the progress bar.
        """
        if self.timer.current_stage == 'Work ==>':
            self.progress_bar.setMaximum(self.timer.work_duration)
        else:
            self.progress_bar.setMaximum(self.timer.rest_duration)
        self.progress_bar.setValue(self.timer.current_time)

    def apply_settings(self) -> None:
        """
        Applies settings from the second tab.
        """
        self.timer.work_duration = int(self.work_duration_input.text()) * 60
        self.timer.rest_duration = int(self.rest_duration_input.text()) * 60
        self.timer.initial_repetitions = int(self.repetitions_input.text())
        self.timer.repetitions = self.timer.initial_repetitions
        self.timer.current_time = self.timer.work_duration
        self.timer.current_stage = 'Work ==>'
        self.timer.stop()
        self.update_time_label()
        self.update_state_label()
        self.update_repetitions_label()
        self.update_progress_bar()


if __name__ == '__main__':
    # We create an instance of QApplication.
    app = QApplication(sys.argv)

    # We create an instance of WorkoutTimer.
    timer = WorkoutTimer(8, 2, 8)

    # We create an instance of the graphical interface of your application.
    window = Interface(timer)

    # Showing the graphical interface of your application.
    window.show()

    # We start the event loop (or main loop) of your application.
    sys.exit(app.exec_())

'''
self.setStyleSheet("""
    QWidget {
        background-color: #2F3136;  # Устанавливает цвет фона всех виджетов на темно-серый.
        color: #FFFFFF;  # Устанавливает цвет текста всех виджетов на белый.
        font-size: 18px;  # Устанавливает размер шрифта всех виджетов на 18 пикселей.
    }
    QPushButton {
        background-color: #2F4F4F;  # Устанавливает цвет фона всех кнопок на темно-зеленый.
        border: none;  # Убирает границу у всех кнопок.
        border-radius: 4px;  # Устанавливает радиус скругления границ всех кнопок на 4 пикселя.
        padding: 10px;  # Устанавливает внутренний отступ всех кнопок в 10 пикселей.
        min-width: 100px;  # Устанавливает минимальную ширину всех кнопок в 100 пикселей.
        font-size: 20px;  # Устанавливает размер шрифта всех кнопок на 20 пикселей.
        font-weight: bold;  # Устанавливает жирность шрифта всех кнопок.
    }
    QPushButton:hover {
        background-color: #677BC4;  # Устанавливает цвет фона всех кнопок при наведении на синий.
    }
    QPushButton:pressed {
        background-color: #2F4F4F;  # Устанавливает цвет фона всех кнопок при нажатии на темно-зеленый.
    }
    QLineEdit {
        background-color: #8B008B;  # Устанавливает цвет фона всех полей ввода на фиолетовый.
        border: none;  # Убирает границу у всех полей ввода.
        border-radius: 4px;  # Устанавливает радиус скругления границ всех полей ввода на 4 пикселя.
        padding: 5px;  # Устанавливает внутренний отступ всех полей ввода в 5 пикселей.
        color: #FFFFFF;  # Устанавливает цвет текста всех полей ввода на белый.
    }
    QProgressBar {
        border: 2px solid grey;  # Устанавливает границу всех прогресс-баров в 2 пикселя и серого цвета.
        border-radius: 5px;  # Устанавливает радиус скругления границ всех прогресс-баров на 5 пикселей.
        text-align: center;  # Устанавливает выравнивание текста всех прогресс-баров по центру.
    }
    QProgressBar::chunk {
        background-color: #05B8CC;  # Устанавливает цвет фона заполненной части всех прогресс-баров на голубой.
        width: 20px;  # Устанавливает ширину заполненной части всех прогресс-баров в 20 пикселей.
        margin: 0.5px;  # Устанавливает внешний отступ заполненной части всех прогресс-баров в 0.5 пикселя.
    }
    QLabel {
        font-size: 22px;  # Устанавливает размер шрифта всех меток на 22 пикселя.
        font-weight: bold;  # Устанавливает жирность шрифта всех меток.
    }
    QTabBar::tab:selected {
        background: #2F4F4F;  # Устанавливает цвет фона выбранной вкладки на темно-зеленый.
        border: 2px solid #FFFFFF;  # Устанавливает границу выбранной вкладки в 2 пикселя и белого цвета.
        border-radius: 4px;  # Устанавливает радиус скругления границ выбранной вкладки на 4 пикселя.
        box-shadow: 0 0 10px #FFFFFF;  # Устанавливает тень выбранной вкладки в 10 пикселей и белого цвета.
        min-width: 150px;  # Устанавливает минимальную ширину выбранной вкладки в 150 пикселей.
    }
    QTabBar::tab:!selected {
        background: #696969;  # Устанавливает цвет фона невыбранных вкладок на серый.
        border: 2px solid #FFFFFF;  # Устанавливает границу невыбранных вкладок в 2 пикселя и белого цвета.
        border-radius: 4px;  # Устанавливает радиус скругления границ невыбранных вкладок на 4 пикселя.
        box-shadow: 0 0 10px #FFFFFF;  # Устанавливает тень невыбранных вкладок в 10 пикселей и белого цвета.
        min-width: 150px;  # Устанавливает минимальную ширину невыбранных вкладок в 150 пикселей.
    }
""")
'''
