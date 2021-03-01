from random import randint
import sqlite3

class Bank:

    def __init__(self):
        self.id = []
        self.number = []
        self.pin = []
        self.balance = []

    def luhn(number):
        checksum = 0
        for i in range(len(number)):
            if i % 2 == 0:
                if int(number[i]) * 2 > 9:
                    checksum += (int(number[i]) * 2 - 9)
                else:
                    checksum += (int(number[i]) * 2)
            else:
                checksum += int(number[i])
        last_digit = (10 - (checksum % 10)) % 10
        return str(last_digit)

    def generate_card(self):
        self.id.append(len(self.id) + 1)

        number = str(400000000000000 + randint(100000000, 999999999))
        number += Bank.luhn(number)
        self.number.append(number)

        print('\nYour card has been created')
        print(f'Your card number:\n{self.number[-1]}')

        self.pin.append(str(randint(1000, 9999)))
        print(f'Your PIN:\n{self.pin[-1]}')
        self.balance.append(0)
        cur.execute(f"insert or replace into card (id, number, pin, balance) values ({self.id[-1]}, {self.number[-1]}, {self.pin[-1]}, {self.balance[-1]});")
        conn.commit()

    def read_card(self):
        number = input('Enter Your card number:')
        pin = input('Enter Your PIN:')
        if number in self.number and pin in self.pin and self.number.index(number) == self.pin.index(pin):
            return self.number.index(number) + 1
        else:
            print('Wrong card number or PIN!')
            return 0

    def transfer(self, idout):
        numberin = input('Where to? ')
        if numberin != (numberin[:-1] + Bank.luhn(numberin[:-1])) and numberin[0]=='4':
            print('Probably you made a mistake in the card number. Please try again!')
        elif numberin in self.number:
            money = int(input('How much? $'))
            if money > self.balance[idout]:
                print('Not enough money!')
            else:
                self.balance[idout] -= money
                idin = self.number.index(numberin)
                self.balance[idin] += money
                print(f'${money} delivered to {numberin} successfully.')
        elif numberin == self.number[idout]:
            print("You can't transfer money to the same account!")
        else:
            print('Such a card does not exist.')

    def close(self, id):
        self.id.pop(id)
        self.number.pop(id)
        self.pin.pop(id)
        self.balance.pop(id)
        print('The account is closed.')

    def dataimport(self, cur):
        cur.execute('select id, number, pin, balance from card;')
        for id1, number1, pin1, balance1 in cur.fetchall():
            self.id.append(id1)
            self.number.append(number1)
            self.pin.append(pin1)
            self.balance.append(balance1)

    def dataexport(self, cur):
        cur.execute('delete from card;')
        for i in range(len(self.id)):
            cur.execute(f"insert or replace into card (id, number, pin, balance) values ({self.id[i]}, {self.number[i]}, {self.pin[i]}, {self.balance[i]});")
        conn.commit()


# Start of the program:

print("Welcome!")

conn = sqlite3.connect('./card.s3db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')

menu1 = True
card = Bank()
card.dataimport(cur)

while menu1:
    option = int(input('\nMenu:\n1. Create an account\n2. Log into account\n0. Exit\nYour Choice:'))
    if option == 1:
        card.generate_card()
    elif option == 2:
        idlog = card.read_card()
        if idlog:
            print('\nYou have successfully logged\n')
        while idlog:
            print('\nMenu\n1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit')
            option = int(input('Your choice:'))
            if option == 1:
                print(f'\nBalance: ${card.balance[idlog - 1]}')
            elif option == 2:
                card.balance[idlog - 1] += int(input('How much? $'))
                card.dataexport(cur)
            elif option == 3:
                card.transfer(idlog - 1)
                card.dataexport(cur)
            elif option == 4:
                card.close(idlog - 1)
                idlog = 0
                card.dataexport(cur)
            elif option == 5:
                idlog = 0
            elif option == 0:
                menu1, idlog = False, 0
            else:
                print('Wrong input. Repeat, please!')
    elif option == 0:
        menu1 = False
    else:
        print('Wrong input. Repeat, please!')
card.dataexport(cur)
conn.commit()
print('Bye!')