'''import json
import boto3
from botocore.exceptions import ClientError
from boto3 import client
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
'''
'''
import smtplib
from email.mime.multipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.mime.text import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import os,datetime'''


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  
from email.mime.base import MIMEBase
from email import encoders as Encoders
import smtplib
import datetime
#from email.Utils import COMMASPACE, formatdate




#s3 = boto3.resource('s3')  
def send_email(sender, recipient, aws_region, subject, file_name):
    
    
    CRLF = "\r\n"
    
    attendees = ["ons-testaccount@networkbuilders-staging.onsumaye.com"]
    organizer = "ORGANIZER;CN=organiser:mailto:first"+CRLF+" @networkbuilders-staging.onsumaye.com"
    fro = "nickname <ons-testaccount@networkbuilders-staging.onsumaye.com>"
    
    ddtstart = datetime.datetime.now()
    dtoff = datetime.timedelta(days = 1)
    dur = datetime.timedelta(hours = 1)
    ddtstart = ddtstart +dtoff
    dtend = ddtstart + dur
    dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    dtstart = ddtstart.strftime("%Y%m%dT%H%M%SZ")
    dtend = dtend.strftime("%Y%m%dT%H%M%SZ")
    
    description = "DESCRIPTION: test invitation from pyICSParser"+CRLF
    attendee = ""
    for att in attendees:
        attendee += "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-    PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"+CRLF+" ;CN="+att+";X-NUM-GUESTS=0:"+CRLF+" mailto:"+att+CRLF
    ical = "BEGIN:VCALENDAR"+CRLF+"PRODID:pyICSParser"+CRLF+"VERSION:2.0"+CRLF+"CALSCALE:GREGORIAN"+CRLF
    ical+="METHOD:REQUEST"+CRLF+"BEGIN:VEVENT"+CRLF+"DTSTART:"+dtstart+CRLF+"DTEND:"+dtend+CRLF+"DTSTAMP:"+dtstamp+CRLF+organizer+CRLF
    ical+= "UID:FIXMEUID"+dtstamp+CRLF
    ical+= attendee+"CREATED:"+dtstamp+CRLF+description+"LAST-MODIFIED:"+dtstamp+CRLF+"LOCATION:"+CRLF+"SEQUENCE:0"+CRLF+"STATUS:CONFIRMED"+CRLF
    ical+= "SUMMARY:test "+ddtstart.strftime("%Y%m%d @ %H:%M")+CRLF+"TRANSP:OPAQUE"+CRLF+"END:VEVENT"+CRLF+"END:VCALENDAR"+CRLF
    
    eml_body = "Email body visible in the invite of outlook and outlook.com but not google calendar"
    eml_body_bin = "This is the email body in binary - two steps"
    msg = MIMEMultipart('mixed')
    msg['Reply-To']=fro
    #msg['Date'] = formatdate(localtime=True)
    msg['Date'] = '666'
    msg['Subject'] = "Test mail"+dtstart
    msg['From'] = fro
    msg['To'] = ",".join(attendees)
    
    part_email = MIMEText(eml_body,"html")
    part_cal = MIMEText(ical,'calendar;method=REQUEST')
    
    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)
    
    ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
    ical_atch.set_payload(ical)
    Encoders.encode_base64(ical_atch)
    ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))
    
    #eml_atch = MIMEBase('text/plain','')
    eml_atch = MIMEText('', 'plain')

    Encoders.encode_base64(eml_atch)
    eml_atch.add_header('Content-Transfer-Encoding', "")
    
    msgAlternative.attach(part_email)
    msgAlternative.attach(part_cal)
    
    login = "contact@networkbuilders-staging.onsumaye.com"
    password = "On$0St@g!1G"
    
    mailServer = smtplib.SMTP('networkbuilders-staging.onsumaye.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(login, password)
    #mailServer.sendmail(fro, attendees, 'Neeraj Maurya')
    mailServer.sendmail(fro, attendees, msg.as_string())
    mailServer.close()
    
    
def lambda_handler(event, context):
    # TODO implement
    send_email('contact@networkbuilders-staging.onsumaye.com', 'ons-testaccount@onsumaye.com', 'us-east-2', 'AWS LAMBDA TEST','https://s3.console.aws.amazon.com/s3/buckets/intel-virtuallab?region=us-east-2&tab=objects/invite.ics?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEAYaCmFwLXNvdXRoLTEiRjBEAiBVSaktH34gK9tTWwFCPBQ09VzepnfnLY9ted%2BwrYwKKgIgOKO4%2BoONewzTmNMGh7fc6aqGcakFqgdFXlzQrFmP1AsqhAMI%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw0NDgyNzY5ODE0MTIiDNtJAkNsF0eiUcAEEirYArMT8EUYtAOsYcofB0AyHKLrHygnLU6qFUleWZHgmj27ce2NbrfKjkRHTn1yiz8ecmSdTH4qtuBk%2B64fE9DjZ2Xe1psh%2FcBBgACUHzWcyM32LHya0K%2FPaYupQZpH2Rw8lQX%2B1WcTGE8UVLn5iQK29pq1075Hp8nT2Z%2FHCb3oUUxFfLYygo46Tw3%2Be7pRksCiH0V4ioVG%2FqfG4aeCoW6oKjKEH8AQDcFRg%2FNoDtT%2Bey2C%2Bun9rYAzgrycL5Xy2U135bl9JVl1XRYksVJkk99MQtdVF8SBeFJj%2Bj5pWtSFtd6BDz2L1f5HlRkqr%2Fos9S5r%2F0mUZ135dGw%2FKh%2BLYMYFsFG3foJ7w%2Ft8DVI6LvXrKntEH0xGu96BgTXWhnD9eOBiIRjNqco4woAGOa6DE%2FyG9FM5248aR02mBrp4IeipFufyN424WkiiLuYb3ud%2FY5IAvsZ5tst9461DMOSMhpUGOrQClqEQhA7L1pbjRabgYZPP4qsJ0CgtSz%2FRx%2FrMiTwZnmKOOGhC8nkd8r0XYOv0oJxmLEXLE%2F49e5Aeq1idAplDJXQvkNoFes0inqLLQlyL%2FLW9ATGfI%2FXVNvcs3iWzeB4N%2BOQaOIHLVYVl4Xy7oq0pzhGILVVFkvYV1sKq2zHAQ4C90x2NKWBRaoV9qJJO8kBRNZbijfGfj9OYeZg1Lfp5%2BA%2BMAzcH3Ue%2FcQ%2B6u0OFWX7fvuHwlfcR7DM97QsO6fgbCFzVxgGjGtu7UbVLlmimpASS8q%2FZi4ao1GBlAhAA6z3WwaGwcLbQI57mlCmPK%2B%2FWmYJ%2BNdqBv5Hx0UtWWUM%2F4Kj8xxSDPPIXV6t3858YQMeVi%2BFztfIOdERzxYR5ROcR6T7KXNSrmEDiu0Ca6qlfqkkVtUw%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220609T062342Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAWQX3D42SIDDOU6RB%2F20220609%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=f2359c9d08bcf1cf6d9ca563f6a9c68179a07a4c06e49c246bd202343d1bb5be')
    print("deep",event)
    print(context)