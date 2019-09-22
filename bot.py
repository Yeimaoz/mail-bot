import smtplib
from email.mime.text import MIMEText
from argparse import ArgumentParser
from getpass import getpass
import sys
import re

Notice = '''
******************** Introduction to Computer Science Laboratory Notice ********************
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

def announce_lab_scores(sheet):
    receiver_list = []
    with open(sheet, 'r') as f:
        # format: student id, student name, score
        receiver_list = [re.sub(' ', '', line).split(',') for line in f.readlines()]
        f.close()
    
    Who = 'Li-Cheng Zheng'
    Subject = '[TEST] score of {}'.format('Lab. 1')
    From = ''
    To = '{}@{}'
    # {0}: receiver, {1}: lab name, {2}: score, {3}: sender
    Content = '''
    Hi {0}, 
    
    Your score of {1} is {2}.

    Best regards,
    {3}
    {4}
    '''
    account, sender = sender_login()
    if not sender:
        return
    for student_id, name, score, receiver_mail_server in receiver_list:
        print(student_id, name, score, receiver_mail_server)
        message = MIMEText(Content.format(name, Subject, score, Who, Notice))
        message['Subject'] = Subject
        message['From'] = account
        message['To'] = To.format(student_id, receiver_mail_server)
        sender.send_message(message)
    sender.quit()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-m", "--mode", dest="mode", required=True, 
        help='mode flag is required')
    parser.add_argument("-lss", "--lab-score-sheet", dest="lab_score_sheet", required='announce_lab_scores' in sys.argv,
        help='lab_score_sheet is required if the specified mode is announce_lab_scores ...')
    args = vars(parser.parse_args())
    if args['mode'] == 'announce_lab_scores':
        announce_lab_scores(args['lab_score_sheet'])
