class DonationIDGenerator:
    def __init__(self, start=1000):
        self.counter = start

    def generate_donation_id(self):
        self.counter += 1
        return f"DONAT{self.counter}"
    
class CustomerIDGenerator:
    def __init__(self, start=1000):
        self.counter = start

    def generate_customer_id(self):
        self.counter += 1
        return f"CUST{self.counter}"