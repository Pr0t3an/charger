# charger
PST Parser using pypff


Export all email headers and body to csv or json

----------------


               .      ..
       __..---/______//-----.      ((                      )
     .".--.```|    - /.--.  =:    ( CHARGER - PST Analysis! v1.0 ))  
    (.: {} :__L______: {} :__; __--( __- -_= __- -_=   __- -_=  ) 
       *--*           *--*                     
    
usage: charger.py [-h] [-c] [-i PST] [-j] [-o OUTPUT]

Extract Email Headers and Body from PST

optional arguments:
  -h, --help            show this help message and exit
  -c, --csv             Output to CSV.
  -i PST, --pst PST     PST input file
  -j, --json            Output to JSON
  -o OUTPUT, --output OUTPUT
                        Output Directory

e.g. to output csv and json

python charger.py -c - j -i ~/Desktop/sup.pst - o ~/Directory/
------------------------

Requires (or later)

libpff-python==20161119
unicodecsv==0.14.1

pip install -r requirements.txt
touch charmods/__init__.py
