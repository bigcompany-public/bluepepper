import qtawesome
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from bluepepper.clipboard import send_html_to_clipboard, send_text_to_clipboard
from bluepepper.core import root_dir
from bluepepper.gui.utils import get_theme
from bluepepper.gui.widgets.container import ContainerDialog, ContainerWidget, get_qt_app
from bluepepper.openfile import show_in_explorer
from bluepepper.tools.helpme.ticket_model import TicketModel


class InformationWidget(QWidget):
    _accepted = Signal()

    def __init__(self, ticket: TicketModel):
        super().__init__()
        self.ticket = ticket
        self.setup_ui()
        self.setup_signals()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        label = QLabel("The ticket content was copied to your clipboard.\nYou may paste it into an email.")
        layout.addWidget(label)
        label_warning = QLabel(
            "WARNING: Some applications do not support pasting both text and images. If needed, you can find the screenshots below."
        )
        label_warning.setWordWrap(True)
        label_warning.setProperty("status", "warning")
        layout.addWidget(label_warning)
        self.browse_screenshots_button = QPushButton("Browse Screenshots")
        layout.addWidget(self.browse_screenshots_button)

        self.ok_button = QPushButton("OK")
        self.ok_button.setProperty("status", "important")
        layout.addWidget(self.ok_button)

        if not self.ticket.screenshots:
            label_warning.setHidden(True)
            self.browse_screenshots_button.setHidden(True)

    def setup_signals(self):
        self.ok_button.clicked.connect(self.ok_clicked)
        self.browse_screenshots_button.clicked.connect(self.browse_button_clicked)

    def ok_clicked(self):
        self._accepted.emit()

    def browse_button_clicked(self):
        show_in_explorer(self.ticket.screenshots[0])


def send_ticket_content_to_clipboard(ticket: TicketModel):
    paragraphs = []
    paragraphs.append(f"ticket: {ticket.name}")
    paragraphs.append(f"user: {ticket.user}")
    paragraphs.append(f"computer: {ticket.computer}")
    if ticket.error:
        paragraphs.append(f"error: {ticket.error}")
    if ticket.traceback:
        paragraphs.append(f"traceback: {ticket.traceback}")
    if ticket.path:
        paragraphs.append(f"path: {ticket.path}")
    if ticket.asset:
        paragraphs.append(f"asset: {ticket.asset}")
    if ticket.shot:
        paragraphs.append(f"shot: {ticket.shot}")
    paragraphs.append(f"description: {ticket.description}")

    paragraphs += ticket.screenshots
    if ticket.screenshots:
        send_html_to_clipboard(paragraphs)
    else:
        send_text_to_clipboard("\n".join(paragraphs))


def show_widget(ticket: TicketModel):
    app = get_qt_app()
    widget = InformationWidget(ticket)
    icon = qtawesome.icon("fa5s.hand-sparkles", scale_factor=1, color=get_theme()["ok"])
    container = ContainerWidget(widget, icon=icon, title="HelpMe Ticket")
    dialog = ContainerDialog(container=container)
    dialog.setFixedWidth(300)
    widget._accepted.connect(dialog.accept)
    dialog.exec()


def submit_ticket(ticket: TicketModel):
    send_ticket_content_to_clipboard(ticket)
    show_widget(ticket)


if __name__ == "__main__":
    ticket = TicketModel(
        name="my ticket",
        user="dev",
        computer="local",
        description="this is a test",
        screenshots=[root_dir / "bluepepper/gui/icons/console.png"],
    )
    submit_ticket(ticket)
