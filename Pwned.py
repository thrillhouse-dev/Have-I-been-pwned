import hashlib
import requests
import PySimpleGUI as sg


def getandencrypt(passw):
    """" get Password to test from user input and encrypt with sha1-Hash-Algorythm. Then split and
    return the first 5 chars from hash for use in Pwned-API. The rest is globally stored in tail """
    #global passw
    #passw = input("please input your desired password:  ")
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
        sg. Popup(f'Oh No! The Pass "{passw}" has been pwned {count} times!')
    else:
       sg. Popup(f'"{passw}" was NOT found in Database.So you are good to go!')
    return 'done!'


sg.change_look_and_feel('DarkBrown4')
# STEP 1 define the layout
layout = [
            [sg.Text('API-Password-Checker', size=(40, 2), font= ('Helvetica', 20))],
            [sg.Text('Just enter your Password below and click the Check-Button:', font= ('Helvetica', 16))],
            [sg.Input()],
            [sg.Button('Check'), sg.Button('Exit'), sg.Checkbox(' check to hide your Pass')]
         ]
# STEP 2 - create the window
window = sg.Window(';--)  Have I been Pwned?', layout, alpha_channel=.8,  grab_anywhere=True, font=("Helvetica", 12))

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
