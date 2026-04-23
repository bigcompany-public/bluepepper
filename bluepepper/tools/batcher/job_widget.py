from qtpy.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout


class JobWidget(QFrame):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        # Add a container with a few pixels of margin to make the selection more visually clear in the JobListWidget
        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 0, 0, 0)

        main_frame = QFrame()
        main_frame.setProperty("depth", "4")
        layout.addWidget(main_frame)
        main_layout = QHBoxLayout(main_frame)

        # Below is just an example to test the sizeHints
        label = QLabel("My Job")
        main_layout.addWidget(label)
        button = QPushButton("LOL")
        main_layout.addWidget(button)
        button.setProperty("status", "important")
