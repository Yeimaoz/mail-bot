import smtplib
from email.mime.text import MIMEText
from argparse import ArgumentParser
import sys
import re

def announce_lab_scores(sheet, receiver_mail_server='cc.ncu.edu.tw'):
    receiver_list = []
    with open(sheet, 'r') as f:
        receiver_list = f.readlines()
    print(receiver_list)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-m", "--mode", dest="mode", required=True, 
        help='mode flag is required')
    parser.add_argument("-lss", "--lab-score-sheet", dest="lab_score_sheet", required='announce_lab_scores' in sys.argv,
        help='lab_score_sheet is required if the specified mode is announce_lab_scores ...')
    args = vars(parser.parse_args())
    if args['mode'] == 'announce_lab_scores':
        announce_lab_scores(args['lab_score_sheet'])
