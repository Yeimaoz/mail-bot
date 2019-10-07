import smtplib
from email.mime.text import MIMEText
from argparse import ArgumentParser
from getpass import getpass
import sys
import re

Notice = '''
******************** Introduction to Computer Science Laboratory Notice ********************
Please do not reply to this email. 
This email address, ncuedalab.andy@gmail.com, is used only for sending email to you, so you will not receive a response.
This mail is sent by the mail-bot.
The bot won't leak any information about your scores in this class to others.
The implementation of the mail-bot is avaliable on https://github.com/Yeimaoz/mail-bot.
If you have any questions or concerns, please feel free to contact me.
Author: Li-Cheng Zheng
Office: E1-359
Office hour: 
Email: lczheng.official@gmail.com 
'''

def sender_login(sender_mail_server='gmail.com'):
    account = input('Enter your account: ')
    password = getpass('Enter your password: ')
    sender = smtplib.SMTP_SSL('smtp.'+sender_mail_server, 465)
    sender.ehlo()
    try:
        sender.login(account, password)
    except smtplib.SMTPException:
        sender = None
        print('Login error ...')
    return account, sender

def mail_template_loader(mail_template):
    Subject, From, Content = '', '', ''
    with open(mail_template, 'r') as f:
        # format: student id, student name, score, receiver mail server
        content = f.read()
        Subject = re.search('Subject *= *(.*)', content).group(1)
        From =  re.search('From *= *(.*)', content).group(1)
        Content = '\n'.join(content.splitlines()[4:])
        f.close()
    return Subject, From, Content

def score_sheet_loader(sheet):
    receiver_list = []
    with open(sheet, 'r') as f:
        # format: student id, student name, score, receiver mail server
        receiver_list = [re.sub(' ', '', line).split(',') for line in f.readlines()]
        f.close()
    return receiver_list

def announce_lab_scores(sheet, mail):
    lab_name = sheet.split('/')[-1][:-4].split('_')[-1]
    receiver_list = score_sheet_loader(sheet)
    Subject, From, Content = mail_template_loader(mail)
    account, sender = sender_login()
    if not sender:
        return
    for student_id, student, *scores, receiver_mail_server in receiver_list:
        parts = '{0} and {1}'.format(', '.join(scores[:-2]), scores[-2])
        number_of_parts = [lab_name+'.'+str(i) for i in range(1, len(scores[:-1])+1)]
        labs = '{0} and {1}'.format(', '.join(number_of_parts[:-1]), number_of_parts[-1])
        total = scores[-1]
        message = MIMEText(Content.format(student, parts, labs, total, lab_name, Notice))
        message['Subject'] = Subject.format(lab_name)
        message['From'] = From if From else account
        message['To'] = '{}@{}'.format(student_id, receiver_mail_server)
        sender.send_message(message)
        print('Send to {} ...'.format(student))
    sender.quit()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-m", "--mode", dest="mode", required=True, 
        help='mode flag is required')
    parser.add_argument("-lss", "--lab-score-sheet", dest="lab_score_sheet", required='announce_lab_scores' in sys.argv,
        help='lab_score_sheet is required if the specified mode is announce_lab_scores ...')
    parser.add_argument("-mt", "--mail-template", dest="mail_template", required='announce_lab_scores' in sys.argv,
        help='mail_template is required if you want to send mail to anyone ...')
    args = vars(parser.parse_args())
    if args['mode'] == 'announce_lab_scores':
        announce_lab_scores(args['lab_score_sheet'], args['mail_template'])
