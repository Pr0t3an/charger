import email.utils
import calendar
import datetime
import os
import sys
from charmods import chargenerator as cro


try:
    import pypff
except ImportError:
    print("[+] Install the pypff...exiting")
    sys.exit(1)


messages = 0
emailproccessor = {}
nummess = 0
attachments = []


def email_time_to_utc_datetime(s):
    tt = email.utils.parsedate_tz(s)
    if tt is None: return None
    timestamp = calendar.timegm(tt) - tt[9]
    return datetime.datetime.utcfromtimestamp(timestamp)


def getmessages(folder):
    global messages
    global nummess
    nummess += folder.number_of_sub_messages
    if folder.number_of_sub_messages == 0:
        return
    else:
        for message in folder.sub_messages:
            messages += 1
            m_unique = cro.id_generator()
            emailproccessor[m_unique] = {}
            try:
                emailproccessor[m_unique]['m_fullheader'] = message.get_transport_headers()
                headers = message.get_transport_headers().splitlines()
                for header in headers:
                    if header.strip().lower().startswith("from:"):
                        emailproccessor[m_unique]['m_from'] = header.strip().lower().strip('from:').lstrip(' ')
                    elif header.strip().lower().startswith("reply-to:"):
                        emailproccessor[m_unique]['m_replyto'] = header.strip().lower().strip('reply-to:').lstrip(' ')
                    elif header.strip().lower().startswith("to:"):
                        emailproccessor[m_unique]['m_to'] = header.strip().lower().strip('to:').lstrip(' ')
                    elif header.strip().lower().startswith("cc:"):
                        emailproccessor[m_unique]['m_cc'] = header.strip().lower().strip('cc:').lstrip(' ')
                    elif header.strip().lower().startswith("subject:"):
                        emailproccessor[m_unique]['m_subject'] = header.strip().lower().strip('subject:').lstrip(' ')
                    elif header.strip().lower().startswith("content-type:"):
                        emailproccessor[m_unique]['m_contenttype'] = header.strip().lower().strip('content-type:').lstrip(' ')
                    elif header.strip().lower().startswith("importance:"):
                        emailproccessor[m_unique]['m_importance'] = header.strip().lower().strip('content-type:').lstrip(' ')
                    elif header.strip().lower().startswith("x-mailer:"):
                        emailproccessor[m_unique]['m_xmailer'] = header.strip().lower().strip('x-mailer:').lstrip(' ')
                    elif header.strip().lower().startswith("x-originating-client"):
                        emailproccessor[m_unique]['m_client'] = header.strip().lower().strip('x-originating-client:').lstrip(' ')
                    elif header.strip().lower().startswith("message-id:"):
                        emailproccessor[m_unique]['m_id'] = header.strip().lower().strip('message-id:').lstrip(' ')
                    elif header.strip().lower().startswith("date:"):
                         datetest = header.strip().lower().strip('date:').lstrip(' ')
                         emailproccessor[m_unique]['m_date'] = datetest
                         emailproccessor[m_unique]['m_date_utc'] = email_time_to_utc_datetime(datetest)
                    elif header.strip().lower().startswith("return-path:"):
                        emailproccessor[m_unique]['m_returnpath'] = header.strip().lower().strip('return-path:').lstrip(' ')

                    try:
                        x = emailproccessor[m_unique]['m_replyto']
                    except KeyError:
                        emailproccessor[m_unique]['m_replyto'] = "null"
                        continue

                    try:
                        x = emailproccessor[m_unique]['m_importance']
                    except KeyError:
                        emailproccessor[m_unique]['m_importance'] = "null"
                        continue
                    try:
                        x = emailproccessor[m_unique]['m_xmailer']
                    except KeyError:
                        emailproccessor[m_unique]['m_xmailer'] = "null"
                        continue
                    try:
                        x = emailproccessor[m_unique]['m_client']
                    except KeyError:
                        emailproccessor[m_unique]['m_client'] = "null"
                        continue
                    try:
                        x = emailproccessor[m_unique]['m_returnpath']
                    except KeyError:
                        emailproccessor[m_unique]['m_returnpath'] = "null"
                        continue




            except AttributeError:
                # No email header
                continue
            try:
                temp = message.plain_text_body.replace(",", "','")
                emailproccessor[m_unique]['m_body'] = temp
                if message.number_of_attachments > 0:
                    emailproccessor[m_unique]['m_attachment_count'] = message.number_of_attachments
                else:
                    emailproccessor[m_unique]['m_attachment_count'] = "0"
                attachmentcount = message.number_of_attachments
            except AttributeError:
                # No email header
                continue


def iteratefolder(rootfolder):
    for folder in rootfolder.sub_folders:
        if folder.number_of_sub_folders:
            iteratefolder(folder)
        getmessages(folder)


def launchstuff(pstfile):
    if os.path.isfile(pstfile):
            print "\n\n[+] Begining to Process PST: {}\n".format(pstfile)
            pst = pypff.file()
            pst.open(pstfile)
            rootfolder = pst.get_root_folder()
            iteratefolder(rootfolder)
            pst.close()
            counter = 0
            for p_id, p_info in emailproccessor.items():
                print "[+] Email ID: {}" .format(p_id)
                counter += 1
            if counter == nummess:
                print "\n[+] Complete: Meta Extracted for all {} messages\n\n".format(counter)
            else:
                print "[*] Error in Extraction only {} message of {} were extracted\n".format(counter, nummess)
    else:
        print "[*] PST file does not exist"
    return emailproccessor
