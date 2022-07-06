import datetime
import random
import smtplib
import pandas
import os, glob
import getpass

# 1. Update the birthdays.csv

# 2. Check if today matches a birthday in the birthdays.csv
today = datetime.datetime.now()
month = today.month
day = today.day
birthday = [month, day]
data = pandas.read_csv("birthdays.csv")
birthdays_dates = data.to_dict(orient="records")
birthday_names = []
os.mkdir("ready_to_send")

def check_birthday():
    for items in birthdays_dates:
        if birthday == [items['month'], items["day"]]:
            birthday_names.append(items["name"])
    return birthday_names

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual
# name from birthdays.csv


if check_birthday():
    word_to_replace = '[NAME]'
    random_letter = random.choice(os.listdir("letter_templates"))
    path_all_letters = 'letter_templates'
    path_to_random_letter = path_all_letters + "/" + random_letter
    with open(path_to_random_letter) as letter:
        content = letter.read()
        for name in birthday_names:
            new_letter = content.replace(word_to_replace, name)
            with open(f"ready_to_send/letter_for_{name}.txt", "w") as created:
                created.write(new_letter)
# 4. Send the letter generated in step 3 to that person's email address.
path = "./ready_to_send"
email = "your email address"
password_email = getpass.getpass("Password: ")
for filename in glob.glob(os.path.join(path, '*.txt')):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        letter_out = f.read()
        with smtplib.SMTP('smtp.gmail.com', 587) as connection:
            connection.starttls()
            connection.login(user=email, password=password_email)
            subject = "Happy Birthday to You"
            message = letter_out
            email_body = "Subject: " + subject + '\n' + message
            connection.sendmail(from_addr=email, to_addrs=email, msg=email_body)


