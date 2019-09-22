import smtplib
from email.mime.text import MIMEText
from argparse import ArgumentParser

def announce_lab_scores(sheet):
    pass

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-m", "--mode", dest="mode")
    parser.add_argument("-lss", "--lab-score-sheet", dest="lab_score_sheet")
    args = vars(parser.parse_args())
    print(args)