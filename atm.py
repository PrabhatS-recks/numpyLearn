class atm:
    def__init__(self)

    self.pin="";
self.balance=0;

self.menu()

def menu(self) :
    user_input=input("Welcome to the ATM\nPlease choose an option:\n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Exit\n")

    if user_input=="1":
        self.create_pin()
    elif user_input=="2":
        print("Deposit")
    elif user_input=="3":
        print("Withdraw")

        def create_pin(self):
            self.pin=input("Enter your pin: ")
            print("PIN CREATED SUCCESSFULLY")