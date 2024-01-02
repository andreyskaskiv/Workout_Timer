import winsound
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QTabWidget, QHBoxLayout


class WorkoutTimer:
    """
    The WorkoutTimer class is a timer for interval training.
    It allows you to set the duration of work, rest and number of repetitions.
    """

    def __init__(self, work_duration: int, rest_duration: int, repetitions: int):
        """
        Initializes a timer with the specified work, rest, and repetition parameters.

        :param work_duration: Duration of work in minutes.
        :param rest_duration: Rest duration in minutes.
        :param repetitions: Number of repetitions.
        """
        self.work_duration = work_duration * 60
        self.rest_duration = rest_duration * 60
        self.initial_repetitions = repetitions
        self.repetitions = repetitions
        self.current_stage = 'Work ==>'
        self.current_time = self.work_duration
        self.running = False

    def start(self) -> None:
        """
        Starts the timer.
        """
        self.running = True

    def stop(self) -> None:
        """
        Stops the timer and resets it to its initial parameters.
        """
        self.running = False
        self.current_stage = 'Work ==>'
        self.current_time = self.work_duration
        self.repetitions = self.initial_repetitions

    def pause(self) -> None:
        """
        Pauses or resumes the timer.
        """
        self.running = not self.running

    def next(self) -> None:
        """
        Moves to the next stage (work or rest) if the timer is running and there are repetitions left.
        """
        if self.running and self.repetitions > 0:
            if self.current_stage == 'Work ==>':
                self.current_stage = 'Rest ==>'
                self.current_time = self.rest_duration
            else:
                self.current_stage = 'Work ==>'
                self.current_time = self.work_duration
            self.repetitions -= 1

    def back(self) -> None:
        """
        Returns one step back (work or rest)
        if the timer is running and the maximum number of repetitions has not been reached.
        """
        if self.running and self.repetitions < self.initial_repetitions:
            self.repetitions += 1
            if self.current_stage == 'Work ==>':
                self.current_stage = 'Rest ==>'
                self.current_time = self.rest_duration
            else:
                self.current_stage = 'Work ==>'
                self.current_time = self.work_duration

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


class Interface(QTabWidget):
    """Interface class for the workout timer."""

    def __init__(self):
        super().__init__()

        # Initialize timers
        self.init_timers()

        # Create tabs
        self.init_tabs()

        # Configure Timer tab
        self.configure_timer_tab()

        # Configure Settings tab
        self.configure_settings_tab()

        # Set the style
        self.set_style()

    def set_style(self):
        """Sets the style of the interface."""
        style = """
            QWidget {
                background-color: #2F3136;
                color: #FFFFFF;
                font-size: 16px;
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
                background-color: #8B008B;
                border: none;
                border-radius: 4px;
                padding: 5px;
                color: #FFFFFF;
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
        """
        self.setStyleSheet(style)

    def init_timers(self):
        """Initializes the timers."""
        self.timer = WorkoutTimer(6, 2, 8)
        self.qt_timer = QTimer()
        self.qt_timer.timeout.connect(self.update_timer)

    def init_tabs(self):
        """Initializes the tabs."""
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.addTab(self.tab1, "Timer")
        self.addTab(self.tab2, "Settings")

    def configure_timer_tab(self):
        """Configures the Timer tab."""
        self.layout1 = QVBoxLayout(self.tab1)

        # Configure info layout
        self.init_info_layout()

        # Configure Start/Pause button
        self.init_start_button()

        # Configure buttons layout
        self.init_buttons_layout()

    def init_info_layout(self):
        """Initializes the info layout."""
        self.info_layout = QHBoxLayout()
        self.stage_label = QLabel()
        self.timer_label = QLabel()
        self.repetitions_label = QLabel()
        self.info_layout.addWidget(self.stage_label)
        self.info_layout.addWidget(self.timer_label)
        self.info_layout.addWidget(self.repetitions_label)
        self.layout1.addLayout(self.info_layout)

    def init_start_button(self):
        """Initializes the Start/Pause button."""
        self.start_button = QPushButton('Start/Pause')
        self.start_button.clicked.connect(self.start_timer)
        self.layout1.addWidget(self.start_button)

    def init_buttons_layout(self):
        """Initializes the buttons layout."""
        self.buttons_layout = QHBoxLayout()
        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.back)
        self.buttons_layout.addWidget(self.back_button)

        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop)
        self.buttons_layout.addWidget(self.stop_button)

        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.next)
        self.buttons_layout.addWidget(self.next_button)

        self.layout1.addLayout(self.buttons_layout)

    def configure_settings_tab(self):
        """Configures the Settings tab."""
        self.layout2 = QVBoxLayout(self.tab2)

        # Configure input fields
        self.init_input_fields()

    def init_input_fields(self):
        """Initializes the input fields."""
        self.work_input = QLineEdit()
        self.work_input.setText("8")
        self.layout2.addWidget(QLabel("Work (in minutes)"))
        self.layout2.addWidget(self.work_input)

        self.rest_input = QLineEdit()
        self.rest_input.setText("2")
        self.layout2.addWidget(QLabel("Rest (in minutes)"))
        self.layout2.addWidget(self.rest_input)

        self.repeats_input = QLineEdit()
        self.repeats_input.setText("8")
        self.layout2.addWidget(QLabel("Repeats"))
        self.layout2.addWidget(self.repeats_input)

    def start_timer(self):
        """Starts the timer."""
        work_duration = int(self.work_input.text())
        rest_duration = int(self.rest_input.text())
        repetitions = int(self.repeats_input.text())

        self.timer = WorkoutTimer(work_duration, rest_duration, repetitions)
        self.timer.start()

        if self.qt_timer.isActive():
            self.qt_timer.stop()
        else:
            self.qt_timer.start(1000)

    def update_timer(self):
        """Updates the timer."""
        if self.timer.running and self.timer.current_time > 0 and self.timer.repetitions > 0:
            minutes, seconds = divmod(self.timer.current_time, 60)
            self.update_labels(minutes, seconds)

            self.timer.current_time -= 1
            if self.timer.current_time < 5:
                winsound.Beep(1000, 100)
                # QSound.play("beep.wav")
        elif self.timer.running and self.timer.repetitions > 0:
            self.timer.switch_stage()
            self.timer.repetitions -= 1

    def update_labels(self, minutes, seconds):
        """Updates the labels on the interface."""
        self.timer_label.setText(f"Time: {minutes}:{seconds}")
        self.repetitions_label.setText(f"Repeat: {self.timer.repetitions}")
        self.stage_label.setText(f"{self.timer.current_stage}")
        color = "#00FF00" if self.timer.current_stage == 'Work ==>' else "yellow"
        self.stage_label.setStyleSheet(f"color: {color}")
        self.timer_label.setStyleSheet(f"color: {color}")
        self.repetitions_label.setStyleSheet(f"color: {color}")

    def back(self):
        """Goes back to the previous stage of the timer."""
        self.timer.back()

    def stop(self):
        """Stops the timer."""
        self.timer.stop()

    def next(self):
        """Goes to the next stage of the timer."""
        self.timer.next()


if __name__ == "__main__":
    app = QApplication([])
    interface = Interface()
    interface.show()
    app.exec_()
