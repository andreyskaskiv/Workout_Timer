import tkinter as tk
from tkinter import ttk
from typing import Callable

import winsound


class WorkoutTimer:
    """
    A class used to represent a Workout Timer.

    ...

    Attributes
    ----------
    work_duration : int
        duration of work in seconds
    rest_duration : int
        duration of rest in seconds
    initial_repetitions : int
        initial number of repetitions
    repetitions : int
        current number of repetitions
    current_stage : str
        current stage of the workout
    current_time : int
        current time left in the current stage
    running : bool
        whether the timer is currently running

    """

    def __init__(self, work_duration: int, rest_duration: int, repetitions: int):
        """
        Constructs all the necessary attributes for the WorkoutTimer object.
        """
        self.work_duration = work_duration * 60
        self.rest_duration = rest_duration * 60
        self.initial_repetitions = repetitions
        self.repetitions = repetitions
        self.current_stage = 'Work ==>'
        self.current_time = self.work_duration
        self.running = False

    def start(self, update_stage: Callable[[str], None], update_label: Callable[[str], None],
              update_repetitions: Callable[[str], None], root: tk.Tk):
        """
        Starts the timer.
        """
        self.running = True
        self.countdown(update_stage, update_label, update_repetitions, root)

    def countdown(self, update_stage: Callable[[str], None], update_label: Callable[[str], None],
                  update_repetitions: Callable[[str], None], root: tk.Tk):
        """
        Counts down the current time.
        """
        if self.running and self.current_time > 0 and self.repetitions > 0:
            self.update_labels(update_stage, update_label, update_repetitions)
            self.beep_if_needed()
            self.current_time -= 1
            root.after(1000, self.countdown, update_stage, update_label, update_repetitions, root)
        elif self.running and self.repetitions > 0:
            self.switch_stage()
            self.repetitions -= 1
            root.after(1000, self.countdown, update_stage, update_label, update_repetitions, root)

    def update_labels(self, update_stage: Callable[[str], None], update_label: Callable[[str], None],
                      update_repetitions: Callable[[str], None]):
        """
        Updates the stage, timer, and repetitions labels.
        """
        minutes, seconds = divmod(self.current_time, 60)
        update_label(f"{minutes} : {seconds} min")
        update_repetitions(f"{self.repetitions}")
        update_stage(f"{self.current_stage}")

    def beep_if_needed(self):
        """
        Beeps if the current time is less than or equal to 10 seconds.
        """
        if self.current_time <= 5:
            winsound.Beep(1000, 100)

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
        self.running = not self.running

    def next(self):
        """
        Skips to the next stage or repetition.
        """
        if self.running and self.repetitions > 0:
            if self.current_stage == 'Work ==>':
                self.current_stage = 'Rest ==>'
                self.current_time = self.rest_duration
            else:
                self.current_stage = 'Work ==>'
                self.current_time = self.work_duration
            self.repetitions -= 1

    def back(self):
        """
        Goes back to the previous stage or repetition.
        """
        if self.running and self.repetitions < self.initial_repetitions:
            self.repetitions += 1
            if self.current_stage == 'Work ==>':
                self.current_stage = 'Rest ==>'
                self.current_time = self.rest_duration
            else:
                self.current_stage = 'Work ==>'
                self.current_time = self.work_duration


class Interface:
    """
    A class to create a graphical user interface for a workout timer.

    Attributes
    ----------
    root : tk.Tk
        The root window for the interface.
    timer : WorkoutTimer
        The workout timer to be controlled by the interface.
    run() -> None:
        Starts the main event loop for the interface.
    """

    def __init__(self, timer: 'WorkoutTimer'):
        """
        Constructs all the necessary attributes for the Interface object.

        Parameters
        ----------
        timer : WorkoutTimer
            The workout timer to be controlled by the interface.
        """
        self.root = tk.Tk()
        self.root.geometry("770x195")
        self.root.configure(bg='#2F4F4F')
        self.timer = timer

        style = ttk.Style()
        style.configure("TLabel",
                        foreground="#FFFF00",
                        background="#2F4F4F",
                        font=("Helvetica", 28, 'bold'),
                        padding=20)
        style.configure("TButton",
                        foreground="#00FF00",
                        background="#4B0082",
                        font=("Helvetica", 16, 'bold'),
                        padding=10)
        style.configure("TFrame",
                        background="#2F4F4F")

        self.stage_label = self.create_label(0, 0)
        self.timer_label = self.create_label(0, 1)
        self.repetitions_label = self.create_label(0, 2)

        self.start_button = self.create_button("Start/Pause", self.start_timer, 1, 0, 3)
        self.back_button = self.create_button("Back", self.timer.back, 2, 0)
        self.stop_button = self.create_button("Stop", self.timer.stop, 2, 1)
        self.next_button = self.create_button("Next", self.timer.next, 2, 2)

    def create_label(self, row: int, column: int) -> ttk.Label:
        """
        Creates a label and adds it to the grid.

        Parameters
        ----------
        row : int
            The row of the grid to add the label to.
        column : int
            The column of the grid to add the label to.

        Returns
        -------
        ttk.Label
            The created label.
        """
        label = ttk.Label(self.root, text="", width=10, anchor='center')
        label.grid(row=row, column=column, pady=0, padx=1, sticky='nsew')
        return label

    def create_button(self, text: str, command: Callable, row: int, column: int, columnspan: int = 1) -> ttk.Button:
        """
        Creates a button and adds it to the grid.

        Parameters
        ----------
        text : str
            The text to display on the button.
        command : Callable
            The function to call when the button is clicked.
        row : int
            The row of the grid to add the button to.
        column : int
            The column of the grid to add the button to.
        columnspan : int, optional
            The number of columns the button should span (default is 1).

        Returns
        -------
        ttk.Button
            The created button.
        """
        button = ttk.Button(self.root, text=text, command=command, width=10)
        button.grid(row=row, column=column, columnspan=columnspan, padx=1, sticky='nsew')
        return button

    def update_stage(self, text: str) -> None:
        """
        Updates the stage label with the given text.

        Parameters
        ----------
        text : str
            The text to display on the stage label.
        """
        self.stage_label.configure(text=text)

    def update_label(self, text: str) -> None:
        """
        Updates the timer label with the given text.

        Parameters
        ----------
        text : str
            The text to display on the timer label.
        """
        self.timer_label.configure(text=text)

    def update_repetitions(self, text: str) -> None:
        """
        Updates the repetitions label with the given text.

        Parameters
        ----------
        text : str
            The text to display on the repetitions label.
        """
        self.repetitions_label.configure(text=text)

    def start_timer(self) -> None:
        """
        Starts or pauses the timer.
        """
        if not self.timer.running:
            self.timer.start(self.update_stage, self.update_label, self.update_repetitions, self.root)
        else:
            self.timer.pause()

    def run(self) -> None:
        """
        Starts the main event loop for the interface.
        """
        self.root.mainloop()


if __name__ == "__main__":
    WORK = 8
    REST = 2
    NUMBER_OF_REPEATS = 8

    timer = WorkoutTimer(WORK, REST, NUMBER_OF_REPEATS)
    interface = Interface(timer)
    interface.run()
