#!/usr/bin/env python
"""WIP Parse  PST"""
import sys
import argparse
import random
import string
import os
import json


messages = 0
emailproccessor = {}
nummess = 0
attachments = []
fields = ['m_unique', 'm_fullheader','m_from','m_replyto','m_to','m_cc','m_subject','m_contenttype','m_importance','m_xmailer', 'm_returnpath', 'm_client','m_id','m_date', 'm_body', 'm_attachment_count']

try:
    import pypff
except ImportError:
    print("[+] Install the pypff...exiting")
    sys.exit(1)

try:
    import unicodecsv
except ImportError:
    print("[+] Install the unicodecsv...exiting")
    sys.exit(1)

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def getMessages(folder):
    global messages
    global nummess
    nummess += folder.number_of_sub_messages
    if folder.number_of_sub_messages == 0:
        return
    else:
        for message in folder.sub_messages:
            messages += 1
            m_unique = id_generator()
            emailproccessor[m_unique] = {}
            try:
                emailproccessor[m_unique]['m_fullheader'] = message.get_transport_headers()
                headers = message.get_transport_headers().splitlines()
                for header in headers:
                    if header.strip().lower().startswith("from:"):
                        emailproccessor[m_unique]['m_from'] = header.strip().lower()
                    elif header.strip().lower().startswith("reply-to:"):
                        emailproccessor[m_unique]['m_replyto'] = header.strip().lower()
                    elif header.strip().lower().startswith("to:"):
                        emailproccessor[m_unique]['m_to'] = header.strip().lower()
                    elif header.strip().lower().startswith("cc:"):
                        emailproccessor[m_unique]['m_cc'] = header.strip().lower()
                    elif header.strip().lower().startswith("subject:"):
                        emailproccessor[m_unique]['m_subject'] = header.strip().lower()
                    elif header.strip().lower().startswith("content-type:"):
                        emailproccessor[m_unique]['m_contenttype'] = header.strip().lower()
                    elif header.strip().lower().startswith("importance:"):
                        emailproccessor[m_unique]['m_importance'] = header.strip().lower()
                    elif header.strip().lower().startswith("x-mailer:"):
                        emailproccessor[m_unique]['m_xmailer'] = header.strip().lower()
                    elif header.strip().lower().startswith("x-originating-client"):
                        emailproccessor[m_unique]['m_client'] = header.strip().lower()
                    elif header.strip().lower().startswith("message-id:"):
                        emailproccessor[m_unique]['m_id'] = header.strip().lower()
                    elif header.strip().lower().startswith("date:"):
                        emailproccessor[m_unique]['m_date'] = header.strip().lower()
                    elif header.strip().lower().startswith("return-path:"):
                        emailproccessor[m_unique]['m_returnpath'] = header.strip().lower()

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
                emailproccessor[m_unique]['m_body'] = message.plain_text_body
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
        getMessages(folder)


def main():
    """Run main function."""
    parser = argparse.ArgumentParser(description='Extract Email Headers and Body from PST')
    parser.add_argument('pst', help='PST input file')
    parser.add_argument('-j', '--json', help='Output to JSON', action='store_true')
    parser.add_argument('-c', '--csv', help='Output to CSV.', action='store_true')
    parser.add_argument('output_dir', help='Output Directory')
    args, _ = parser.parse_known_args()



    if os.path.isfile(args.pst):
            print "\n\n[+] Begining to Process PST: {}\n".format(args.pst)
            pst = pypff.file()
            pst.open(args.pst)
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

    if os.path.isdir(args.output_dir):
        genv = id_generator()
        jfilepath = os.path.join(args.output_dir, "pst_" + genv + ".json")
        cfilepath = os.path.join(args.output_dir, "pst_" + genv + ".csv")
        if args.json:
            with open(jfilepath, "w") as f:
                json.dump(emailproccessor, f)
                print "\n[+] Export Complete: JSON file written to {}\n".format(jfilepath)
        if args.csv:
            with open(cfilepath, "wb") as cpath:
                wr = unicodecsv.DictWriter(cpath, fields)
                wr.writeheader()
                for k in emailproccessor:
                    wr.writerow({field: emailproccessor[k].get(field) or k for field in fields})
            print "\n[+] Export Complete: CSV file written to {}\n".format(cfilepath)


def important():
    print """
               .      ..
       __..---/______//-----.      ((                      )
     .".--.```|    - /.--.  =:    ( CHARGER - PST Analysis! v1.0 ))  
    (.: {} :__L______: {} :__; __--( __- -_= __- -_=   __- -_=  ) 
       *--*           *--*                     
    """

if __name__ == "__main__":
    important()
    main()
