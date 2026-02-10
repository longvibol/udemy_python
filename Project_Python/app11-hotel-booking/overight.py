class Ticket:
    def __init__(self):
        pass
    def generate(self):
        print("Generating Ticket")

class DigitalTicket(Ticket):
    def generate(self):
        print("Generating DigitalTicket")

t1= DigitalTicket().generate()
t2= Ticket().generate()