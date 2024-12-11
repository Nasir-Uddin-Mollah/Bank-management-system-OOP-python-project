class Bank:
    def __init__(self, name):
        self.name = name
        self.users = []
    
    def add_user(self, user):
        self.users.append(user)
    
    def remove_user(self, account_no):
        for user in self.users:
            if user.account_no == account_no:
                self.users.remove(user)
                return True
        return False
    
    def find_account(self, account_no):
        for user in self.users:
            if user.account_no == account_no:
                return user
        return None


class User:
    def __init__(self, name, email, address, account_type):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.account_no = email+name
        self.transaction_history = []
        self.loan_limit = 2
        self.total_loan_taken = 0

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited amount {amount} to {self.account_no}")
        self.transaction_history.append(f"deposited amount {amount}")
    
    def withdraw(self, amount):
        if admin.bankrupt:
            print(f"The bank is bankrupt")
        elif amount > self.balance:
            print(f"Withdrawal amount exceeded")
        else:
            self.balance -= amount
            print(f"Amount {amount} withdrew successfully")
            self.transaction_history.append(f"Withdrew amount {amount}")

    def check_balance(self):
        print(f"Current balance is {self.balance}")
    
    def check_transaction_history(self):
        for transaction in self.transaction_history: 
            print(transaction)

    def take_loan(self, amount):
        if not admin.can_take_loan:
            print(f"Loan is not available now")
        elif admin.bankrupt:
            print(f"The bank is bankrupt")
        elif self.loan_limit > 0:
            self.balance += amount
            self.total_loan_taken += amount
            self.loan_limit -= 1
            print(f"Loan amount {amount} added successfully")
            self.transaction_history.append(f"Loan taken amount {amount}")
        else:
            print("Loan limit exceeded")
    
    def transfer_money(self, amount, receiver_account):
        if admin.bankrupt:
            print(f"The bank is bankrupt")
        elif amount > self.balance:
            print("Insufficient balance")
        else:
            receiver = bank.find_account(receiver_account)
            if receiver:
                self.balance -= amount
                receiver.balance += amount
                self.transaction_history.append(f"Transfered amount {amount} to {receiver_account}")
                receiver.transaction_history.append(f"Received amount {amount} from {self.account_no}")
                print(f"Amount {amount} transfered successfully")
            else:
                print(f"Account {receiver_account} does not exist")


class Admin:
    def __init__(self, name):
        self.name = name
        self.can_take_loan = True
        self.bankrupt = False
    
    def create_account(self, name, email, address, account_type):
        user = User(name, email, address, account_type)
        bank.add_user(user)
        print(f"Account created for {name}")

    def delete_account(self, account_no):
        if bank.remove_user(account_no):
            print(f"Account {account_no} deleted.")
        else:
            print(f"Account {account_no} doesn't exist.")

    def view_accounts_list(self):
        if not bank.users:
            print(f"No account exist")
            return
        for user in bank.users:
            print(f"Name: {user.name} Account No: {user.account_no} Balance: {user.balance}")

    def total_balance_of_bank(self):
        total_balance = sum(user.balance for user in bank.users)
        print(f"Total balance of the bank is {total_balance}")

    def total_loan_amount(self):
        total_loan = sum(user.total_loan_taken for user in bank.users)
        print(f"Total loan amount is {total_loan}")

    def loan_feature(self):
        if self.can_take_loan:
            self.can_take_loan = False
            print(f"Loan feature disabled.")
        else:
            self.can_take_loan = True
            print(f"Loan feature enabled.")

    def bankrupt_status(self):
        if not self.bankrupt:
            self.bankrupt = True
            print(f"Users can not withdraw, transfer money or take loan now")
        else:
            self.bankrupt = False
            print(f"Users can withdraw, transfer money and take loans now")
            

bank = Bank("Jonota bank")
admin = Admin("admin")

def user_menu(me):
    while True:
        print("\nUser Menu:") 
        print("1. Deposit") 
        print("2. Withdraw") 
        print("3. Check Balance")
        print("4. Check Transaction History") 
        print("5. Take Loan") 
        print("6. Transfer Money") 
        print("7. Exit")

        choice = int(input("Enter your choice : "))
        if choice == 1:
            amount = int(input("Enter your amount : "))
            me.deposit(amount)
        elif choice == 2:
            amount = int(input("Enter your amount : "))
            me.withdraw(amount)
        elif choice == 3:
            me.check_balance()
        elif choice == 4:
            me.check_transaction_history()
        elif choice == 5:
            amount = int(input("Enter your amount : "))
            me.take_loan(amount)
        elif choice == 6:
            amount = int(input("Enter your amount : "))
            account_no = input("Enter Receiver Account No : ")
            me.transfer_money(amount, account_no)
        elif choice == 7:
            break
        else:
            print(f"Invalid Input")

def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. Create Account") 
        print("2. Delete Account") 
        print("3. View Accounts List")
        print("4. Check Total Balance OF Bank") 
        print("5. Check Total Loan Amount") 
        print("6. Loan Feature") 
        print("7. Bankrupt Status") 
        print("8. Exit")

        choice = int(input("Enter your choice : "))
        if choice == 1:
            name = input("Enter your name : ")
            email = input("Enter your email : ")
            address = input("Enter your address : ")
            account_type = input("Enter your account_type : ")
            admin.create_account(name, email, address, account_type)
        elif choice == 2:
            account_no = input("Enter Account No : ")
            admin.delete_account(account_no)
        elif choice == 3:
            admin.view_accounts_list()
        elif choice == 4:
            admin.total_balance_of_bank()
        elif choice == 5:
            admin.total_loan_amount()
        elif choice == 6:
            admin.loan_feature()
        elif choice == 7:
            admin.bankrupt_status()
        elif choice == 8:
            break
        else:
            print(f"Invalid Input")


while True:
    print("\nWelcome!!")
    print("1. User")
    print("2. Admin")
    print("3. Exit")

    choice = int(input("Enter your choice : "))
    if choice == 1:
        account_no = input("Enter Account No : ")
        me = bank.find_account(account_no)
        if me:
            user_menu(me)
        else:
            print(f"Account {account_no} does not exist")
    elif choice == 2:
        admin_menu()
    elif choice == 3:
        break
    else:
        print("Invalid input")
