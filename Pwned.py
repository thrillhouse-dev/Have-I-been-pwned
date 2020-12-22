import hashlib
import requests
import PySimpleGUI as sg


def getandencrypt(passw):
    """" get Password to test from user input and encrypt with sha1-Hash-Algorythm. Then split and
    return the first 5 chars from hash for use in Pwned-API. The rest is globally stored in tail """
    encrypted = hashlib.sha1(passw.encode('utf-8')).hexdigest()
    global tail
    first5_char, tail = encrypted[0:5].upper(), encrypted[5:].upper()
    return first5_char


def pwned_api_check(passw):
    url = 'https://api.pwnedpasswords.com/range/' + getandencrypt(passw)
    response = requests.get(url)
    all_hashes = response.text.splitlines()
    global hash_count
    hash_count = []
    for line in all_hashes:
        hash_count.append(line.split(':'))
    return([count for h, count in hash_count if tail in h])


def main(passw):
    count = pwned_api_check(passw)
    if count:
        count = int(count[0])
        sg.popup_ok(f'The entered Password has been pwned {count} times! Please change it right now!', font= ('Fixedsys', 10), text_color='red')
    else:
       sg.popup_ok(f'The entered Password was NOT found any Database!', font= ('Fixedsys', 10), text_color='green')
    return 'done!'


sg.change_look_and_feel('DarkBrown4')
# STEP 1 define the layout
layout = [
            [sg.Text('API-Password-Checker', size=(40, 2), justification='center', font= ('Fixedsys', 20), relief=sg.RELIEF_RIDGE)],
            [sg.Text('Just enter your Password below and click the Check-Button:', font= ('Fixedsys', 16))],
            [sg.Input('', password_char='*')],
            [sg.Button('Check'), sg.Button('Exit')]
         ]
# STEP 2 - create the window
window = sg.Window(';--)  Have I been Pwned?', layout, alpha_channel=.8, font=("Fixedsys", 12))

# STEP 3 - the event loop
while True:
    event, values = window.read()       # Read the event that happened and the values dictionary
    #print(event, values)
    if event == 'Check':
        #print('You pressed the button')
        text_input = values[0]
        passw = text_input
        main(passw)
    else:
        break
window.close()
