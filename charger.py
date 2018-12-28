#!/usr/bin/env python

import sys
try:
    from charmods import psthandler as cpar, important as ip, chargenerator as cro
except ImportError:
    print("[*] Missing dependencies (charmods folder) - use git clone")
    sys.exit(1)
import argparse
import os
import json
try:
    import unicodecsv
except ImportError:
    print("[*] Install unicodecsv from requirements.txt")
    sys.exit(1)

fields = ['m_unique', 'm_date_utc', 'm_fullheader','m_from','m_replyto','m_to','m_cc','m_subject','m_contenttype','m_importance','m_xmailer', 'm_returnpath', 'm_client','m_id','m_date', 'm_body', 'm_attachment_count']
temailproccessor = {}

def outputjson(jfilepath, temailproccessor):
    with open(jfilepath, "w") as f:
        json.dump(temailproccessor, f, default=str)
        print "\n[+] Export Complete: JSON file written to {}\n".format(jfilepath)


def outputcsv(cfilepath, temailproccessor):
    with open(cfilepath, "wb") as cpath:
        wr = unicodecsv.DictWriter(cpath, fields)
        wr.writeheader()
        for k in temailproccessor:
            wr.writerow({field: temailproccessor[k].get(field) or k for field in fields})
    print "\n[+] Export Complete: CSV file written to {}\n".format(cfilepath)

def main():
    """Run main function."""
    parser = argparse.ArgumentParser(description='Extract Email Headers and Body from PST')
    parser.add_argument('-c', '--csv', help='Output to CSV.', action='store_true')
    parser.add_argument('-i', '--pst', help='PST input file')
    parser.add_argument('-j', '--json', help='Output to JSON', action='store_true')
    parser.add_argument('-o', '--output', help='Output Directory')
    args, _ = parser.parse_known_args()

    if os.path.isdir(args.output):
        genv = cro.id_generator()
        jfilepath = os.path.join(args.output, "pst_" + genv + ".json")
        cfilepath = os.path.join(args.output, "pst_" + genv + ".csv")
        temailproccessor = cpar.launchstuff(args.pst)
        if args.json:
            outputjson(jfilepath, temailproccessor)
        if args.csv:
            outputcsv(cfilepath, temailproccessor)


if __name__ == "__main__":
    ip.important()
    main()
