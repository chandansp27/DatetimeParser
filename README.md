# DatetimeParser
Custom date parsing module made combining various open source libraries and regex

## Libraries used

- Dateparser
- datefinder
- timefhuman
- relativedelta
- datetime

## Tests

3 days ago ---> ['03-Mar-2024 13 51 49', '03-Mar-2024 19 31 49'] 

now ---> ['06-Mar-2024 13 51 49', '06-Mar-2024 13 51 49'] 

last 2 weeks ---> ['21-Feb-2024 13 51 49', '06-Mar-2024 13 51 49'] 

past 3 months ---> ['06-Dec-2023 13 51 49', '06-Mar-2024 13 51 49'] 

next Monday to yesterday ---> ['05-Mar-2024 00 00 00', '05-Mar-2024 23 59 59'] 

yesterday 3pm UTC ---> ['05-Mar-2024 00 00 00', '05-Mar-2024 23 59 59'] 

5 years ago ---> ['06-Mar-2019 13 51 49', '06-Mar-2019 19 31 49'] 

tomorrow at noon ---> ['06-Mar-2024 13 51 49', '06-Mar-2024 13 51 49'] 

10th February 2023 ---> ['10-Feb-2023 00 00 00', '10-Feb-2023 23 59 59'] 

3rd of March 2024 ---> ['03-Mar-2024 00 00 00', '03-Mar-2024 23 59 59'] 

today ---> ['06-Mar-2024 00 00 00', '06-Mar-2024 13 51 49'] 

2 weeks 5 days ago ---> ['16-Feb-2024 13 51 49', '16-Feb-2024 19 31 49'] 

this Sunday to yesterday 6:45 am ---> ['05-Mar-2024 06 45 00', '05-Mar-2024 23 59 59'] 

3 days ago ---> ['03-Mar-2024 13 51 49', '03-Mar-2024 19 31 49'] 

today to next Sunday ---> ['06-Mar-2024 00 00 00', '06-Mar-2024 13 51 49'] 

3 days ago to yesterday ---> ['05-Mar-2024 00 00 00', '05-Mar-2024 23 59 59'] 

from 10th January 2023 to 15th January 2023 ---> ['10-Jan-2023 00 00 00', '15-Jan-2023 00 00 00'] 

from 1st of March 2024 to 5th of March 2024 ---> ['01-Mar-2024 00 00 00', '05-Mar-2024 00 00 00'] 

from 1st of January 2023 10:30 AM to 3rd of February 2023 5:45 PM ---> ['01-Jan-2023 10 30 00', '03-Feb-2023 17 45 00'] 

from last month to 10th of March 2024 12:00 PM UTC ---> ['06-Mar-2024 13 51 49', '06-Mar-2024 13 51 49'] 

from 5 days ago to today 6pm UTC ---> ['06-Mar-2024 00 00 00', '06-Mar-2024 13 51 49'] 

from 1st of March 2024 to last Thursday 8:45 AM ---> ['01-Mar-2024 00 00 00', '01-Mar-2024 23 59 59'] 

## Usage instructions

DateParser [folder]
- datetime_parser.py
- __init__.py

in the same directory as DatetimeParser [folder]

from DatetimeParser.datetime_parser import datetime_parser

datetime_parser(' *datetime string* ')
