# from pathlib import Path 
# import json
# import random
# import string

# class Bank:
#     database = 'database.json'
#     data = []

#     try:
#         if Path(database).exists():
#             with open (database) as fs:
#                 data = json.loads(fs.read())
#         else:
#             print("Sorry we are facing some issues")

#     except Exception as err:
#         print(f"An error occurred: {err} ")

#     @classmethod
#     def __update(cls):
#         with open (cls.database, 'w') as fs:
#             fs.write(json.dumps(cls.data))

#     @staticmethod
#     def __accountno():
#         alpha = random.choices(string.ascii_letters,k = 5)
#         digits = random.choices(string.digits,k = 4)
#         id = alpha + digits
#         random.shuffle(id)
#         return "".join(id)

#     def createaccount(self):
#         d = {
#             "name": input("plese tell your name:- "),
#             "email": input("plese tell your email:- "),
#             "phone no": int(input("plese tell your phone no:- ")),
#             "pin": int(input("plese tell your pin (4 digit):- ")),
#             "Account No.":Bank.__accountno(),
#             "balance":0
#             }
#         print(f"please note down your account number:- {d['Account No.']}")
#         if len(str(d["pin"])) != 4:
#             print("plese enter a valid pin")

#         elif len(str(d["phone no"])) != 10:
#             print("plese enter a valid phone no")

#         else:
#             Bank.data.append(d)
#             Bank.__update()

#     def deposite_money(self):
#         accNo = input("Tell your account number:- ")
#         pin = input("Enter your pin:- ")
#         user_data = [i for i in Bank.data if i["Account No."] == accNo and str(i["pin"]) == pin]
#         print(user)

#         if not user_data:
#             print("user not found")
#         else:
#             amount = int(input("Enter amount to be deposited:- "))
#             if amount <= 0:
#                 print("Enter a valid amount")
#             elif amount > 10000:
#                 print("greater than 10000")
#             else:
#                 user_data[0]["balance"] += amount
#                 Bank.__update()
#                 print("Amount credeited successfully")

#     def withdraw_money(self):
#         accNo = input("Tell your account number:- ")
#         pin = input("Enter your pin:- ")
#         user_data = [i for i in Bank.data if i["Account No."] == accNo and str(i["pin"]) == pin]

#         if not user_data:
#             print("user not found")
#         else:
#             amount = int(input("Enter amount to be deposited:- "))
#             if amount <= 0:
#                 print("Enter a valid amount")
#             elif amount > 10000:
#                 print("greater than 10000")
#             else:
#                 if user_data[0]["Balance"] < amount:
#                     print("insufficient balance")
#                 else:
#                     user_data[0]["Balance"] -= amount
#                     Bank.__update()
#                     print("Amount withdraw successfully")

#     def details(self):
#         accNo = input("Tell your account number:- ")
#         pin = input("Enter your pin:- ")
#         user_data = [i for i in Bank.data if i["Account No."] == accNo and str(i["pin"]) == pin]

#         if not user_data:
#             print("user not found")
#         else:
#             for i in user_data[0]:
#                 if i == "pin":          #we are hiding the pin details here with the use of continue
#                     continue
#                 else:
#                     print(i, user_data[0][i])

#     def update_details(self):
#         accNo = input("Tell your account number:- ")
#         pin = input("Enter your pin:- ")
#         user_data = [i for i in Bank.data if i["Account No."] == accNo and str(i["pin"]) == pin]
#         if not user_data:
#             print("user not found")
#         else:
#             print("you cannot change Account Number")
#             print("Now update your details and skip it if you don't want to update")
#             # name,email,pin,phone
#             new_data = {
#                 'name' : input("Enter your new name:- "),
#                 'email' : input("Enter your new email:- "),
#                 'phone no' :input("Enter your new Phone number:- "),
#                 'pin' : input("Enter your new pin:- ")
#             }
#             if new_data["name"] == "":
#                 new_data["name"] = user_data[0]['name']
#             if new_data["email"] == "":
#                 new_data["email"] = user_data[0]['email']
#             if new_data["phone no"] == "":
#                 new_data["phone no"] = user_data[0]['phone no']
#             if new_data["pin"] == "":
#                 new_data["pin"] = user_data[0]['pin']
                
#             new_data['Account No.'] = user_data[0]['Account No.']
#             new_data['Balance'] = user_data[0]['Balance']
            
#             if type(new_data['pin']) == str:
#                 new_data['pin'] = int(new_data['pin'])
#             #Handal the skipped value
#             for i in new_data:
#                 if new_data[i] == user_data[0][i]:
#                     continue
#                 else:
#                     user_data[0][i] = new_data[i]
#             Bank.__update()
#             print("Details updated successfully...........")
            
            
#     def delete_account(self):
#         accNo = input("Tell your account number:- ")
#         pin = input("Enter your pin:- ")
#         user_data = [i for i in Bank.data if i["Account No."] == accNo and str(i["pin"]) == pin]

#         if user_data == False:
#             print("user not found")
#         else:
#             check = input("press y to confirm deletion or deletion cancelled press n:- ")
#             if check == 'n' or check == 'N':
#                 print("byepassed deletion")
#             elif check == 'y' or check == 'Y':
#                 Bank.data.remove(user_data[0])
#                 Bank.__update()
#                 print("Account deleted successfully.........")
                
        

        
                                
                
# user = Bank()
# print("press 1 for creating  a account")
# print("press 2 to deposit money")
# print("press 3 to withdraw money")
# print("press 4 for details")
# print("press 5 for updating the details")
# print("press 6 for deleting the account")

# check = int(input("tell your choice:- "))

# if check == 1:
#     user.createaccount()
# elif check == 2:
#     user.deposite_money()
# elif check == 3:
#     user.withdraw_money()
# elif check == 4:
#     user.details()
# elif check == 5:    
#     user.update_details()
# elif check == 6:
#     user.delete_account()





