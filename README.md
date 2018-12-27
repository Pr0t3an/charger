# charger
PST Parser using pypff


Export all email headers and body to csv or json

----------------

usage

python chargerSRT.py -h

               .      ..
       __..---/______//-----.      ((                      )
     .".--.```|    - /.--.  =:    ( CHARGER - PST Analysis! ))  
    (.: {} :__L______: {} :__; __--( __- -_= __- -_=   __- -_=  ) 
       *--*           *--*                     
    
usage: chargerSRT.py [-h] [-j] [-c] pst output_dir

Extract Email Headers and Body from PST

positional arguments:
  pst         PST input file
  output_dir  Output Directory

optional arguments:
  -h, --help  show this help message and exit
  -j, --json  Output to JSON
  -c, --csv   Output to CSV.


------------------------

Requires (or later)

libpff-python==20161119
unicodecsv==0.14.1

pip install -r requirements.txt
