from bluepepper.tools.helpme.ticket_model import TicketModel


def main(ticket: TicketModel):
    """
    The code below calls bluepepper's default method for handling tickets.
    feel free to replace it with whatever fits your needs
    """
    from bluepepper.tools.helpme.ticket_submission import submit_ticket

    submit_ticket(ticket)
