import datefinder
import dateparser
from timefhuman import timefhuman
import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from word2number import w2n
import warnings


def datetime_parser(cleaned_query):
    # XML file datetime format
    datetime_format = '%d-%b-%Y %H %M %S'

    # empty list for appending the parsed datetime values
    datetime_parsed = []

    # convert words to numbers
    def word_to_number(query):
        temp_string = ''
        for word in query.split():
            temp_var = None
            try:
                temp_var = w2n.word_to_num(word)
                if temp_var is not None:
                    temp_string += str(temp_var)
            except Exception:
                temp_string += f' {word} '
        return temp_string

    # apply word_to_number function to cleaned_query
    datetime_text = word_to_number(cleaned_query)

    # add space between datetime and UTC timezone for parsing
    add_space_regex = r'\b(\d+)(ut)\b'
    datetime_text = re.sub(add_space_regex, r'\1 \2', datetime_text)

    # replace '.' with ':' in datetime
    datetime_text = re.sub(r'\b(\d+\.\d+)\b', lambda match: str(match.group(1)).replace('.', ':'), datetime_text)

    # regex patterns to convert utc datetimes from the transcribed text
    utc_pattern1 = re.compile(r'\b(\d{1,2}) (UTC|UT)\b', re.IGNORECASE)
    utc_pattern2 = re.compile(r'\b(\d{3}) (UTC|UT)\b', re.IGNORECASE)
    utc_pattern3 = re.compile(r'\b(\d{4}) (UTC|UT)\b', re.IGNORECASE)
    datetime_text = re.sub(utc_pattern1, r'\1:00 UTC', datetime_text)
    datetime_text = re.sub(utc_pattern2, lambda match: match.group(1)[0] + ":" + match.group(1)[1:] + ' UTC',
                           datetime_text)
    datetime_text = re.sub(utc_pattern3, lambda match: match.group(1)[0] + ":" + match.group(1)[2:] + ' UTC',
                           datetime_text)
    datetime_text = re.sub(r'\s+', ' ', datetime_text.strip())
    datetime_text = datetime_text.replace('utc', 'UTC')
    datetime_text = datetime_text.replace('ut', 'UTC')

    # check if the dt_text matches months_ago_regex pattern and pass it through dateparser
    def parse_datetime(dt_text):

        # pattern to match years/months/weeks/days/hours/minutes ago
        datetime_ago_pattern = r'\b\d+\s*(years?|months?|weeks?|days?|hours?|minutes?)\s*(\d+\s*(years?|months?|weeks?|days?|hours?|minutes?)\s*)*ago\b'
        dateparser_pattern1 = r'\bnow(?:\s\w+)?\b'

        # pattern to match last_n_years/months/weeks/days
        last_n_dates = [
            r'\b(?:last|past)\s(\d{1,2})\sday(?:s)?\b',  # day_regex
            r'\b(?:last|past)\s(\d{1,2})\sweek(?:s)?\b',  # week_regex
            r'\b(?:last|past)\s(\d{1,2})\smonth(?:s)?\b',  # month_regex
            r'\b(?:last|past)\s(\d{1,2})\syear(?:s)?\b'  # year_regex
        ]

        # pattern to match datetime with days of week
        timefhuman_patterns = [
            r'(?:(?:last|past|this|next|coming|upcoming)\s)?(?:mon(?:day)?|tue(?:sday)?|wed(?:nesday)?|thu(?:rsday)?|fri(?:day)?|sat(?:urday)?|sun(?:day)?)(?:\s\d{1,2}(?::\d{2})?(?:\sUTC)?)?(?:\sfrom\s\d{1,2}(?::\d{2})?(?:\sUTC)?)?(?:\sto\s\d{1,2}(?::\d{2})?(?:\sUTC)?)?\b',
            r'\b(?:yesterday|today|tomorrow)(?:\s\d{1,2}(?::\d{2})?(?:\sUTC)?(?:\sto\s\d{1,2}(?::\d{2})?(?:\sUTC)?)?)?\b',
            r'\b((last|past|coming|next|upcoming)\s(mon|tue|wed|thu|fri|sat|sun|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\s(noon|afternoon|midnight))\b'
        ]

        # dateparser.parse
        if re.findall(datetime_ago_pattern, dt_text):
            try:
                datetime_parsed.append(dateparser.parse(datetime_text,
                                                        settings={'TIMEZONE': 'UTC', 'PREFER_DATES_FROM': 'past',
                                                                  'RELATIVE_BASE': datetime.utcnow()}).strftime(
                    datetime_format))
                datetime_obj = (dateparser.parse(dt_text) + timedelta(minutes=10))
                datetime_parsed.append(datetime_obj.strftime(datetime_format))
            except AttributeError:
                pass

        if re.findall(dateparser_pattern1, dt_text):
            try:
                datetime_parsed.append(dateparser.parse(dt_text).strftime(datetime_format))
                datetime_obj = (dateparser.parse(dt_text) - timedelta(minutes=10))
                datetime_parsed.append(datetime_obj.strftime(datetime_format))
            except AttributeError:
                pass

        # relative delta
        elif any(re.search(pattern, dt_text) for pattern in last_n_dates):
            def extract_value(matches_list):
                return int(matches_list.group(1)) if matches_list else 0

            # Find matches_list for day, week, month, and year using regex
            days = extract_value(re.search(last_n_dates[0], dt_text))
            weeks = extract_value(re.search(last_n_dates[1], dt_text))
            months = extract_value(re.search(last_n_dates[2], dt_text))
            years = extract_value(re.search(last_n_dates[3], dt_text))

            # Calculate the start and end dates based on the number of days, weeks, months, and years
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            start_date -= relativedelta(weeks=weeks)
            start_date -= relativedelta(months=months)
            start_date -= relativedelta(years=years)

            # Format the start and end dates
            datetime_parsed.append(start_date.strftime(datetime_format))
            datetime_parsed.append(end_date.strftime(datetime_format))

        # timefhuman
        elif any(re.search(pattern, datetime_text) for pattern in timefhuman_patterns):
            for pattern in timefhuman_patterns:
                matches = re.findall(pattern, datetime_text)

                if pattern == timefhuman_patterns[0] or pattern == timefhuman_patterns[2]:
                    for match in matches:
                        temp_dt = timefhuman(match, now=datetime.utcnow())

                        try:
                            for temp_d in temp_dt:
                                if temp_d > datetime.utcnow():
                                    temp_d -= relativedelta(weeks=1)
                                else:
                                    temp_d = temp_d

                                try:
                                    datetime_parsed.append(temp_d.strftime(datetime_format))

                                except TypeError:
                                    datetime_parsed.append(temp_dt.strftime(datetime_format))
                        except TypeError:
                            if temp_dt > datetime.utcnow():
                                temp_dt -= relativedelta(weeks=1)
                                datetime_parsed.append(temp_dt.strftime(datetime_format))
                            else:
                                datetime_parsed.append(temp_dt.strftime(datetime_format))

                elif pattern == timefhuman_patterns[1]:
                    for match in matches:
                        temp_dt = timefhuman(match, now=datetime.utcnow())
                        try:
                            for temp_d in temp_dt:
                                datetime_parsed.append(temp_d.strftime(datetime_format))
                        except TypeError:
                            datetime_parsed.append(temp_dt.strftime(datetime_format))

        # datefinder
        elif not datetime_parsed:
            datetimes = [dates for dates in datefinder.find_dates('from ' + dt_text)]
            if datetimes:
                datetime_parsed.extend([date_.strftime(datetime_format) for date_ in datetimes])

        # Add 10 minutes to a single datetime object, if only one was found
        if len(datetime_parsed) == 1:
            datetime_obj = datetime.strptime(datetime_parsed[0], datetime_format) + timedelta(minutes=10)
            datetime_parsed.append(datetime_obj.strftime(datetime_format))
        else:
            pass

        def sort_datetime(datetime_parsed_list, datetime_format_string):
            datetime_checked = []
            datetime_parsed_sorted = sorted([datetime.strptime(datetime_parsed_list[0], datetime_format_string),
                                             datetime.strptime(datetime_parsed_list[1], datetime_format_string)])
            for date_time in datetime_parsed_sorted:
                if date_time > datetime.utcnow():
                    warnings.warn('Future date detected, defaulting to current datetime', category=UserWarning)
                    date_time = datetime.utcnow()
                    datetime_checked.append(date_time.strftime(datetime_format_string))
                else:
                    datetime_checked.append(date_time.strftime(datetime_format_string))

            return datetime_checked

        # return sorted datetime
        return sort_datetime(datetime_parsed, datetime_format)

    return parse_datetime(datetime_text)


"""

Usage instructions

DateParser [folder]
- datetime_parser.py
- __init__.py

in the same directory as DatetimeParser [folder]

from DatetimeParser.datetime_parser import datetime_parser

datetime_parser(' *datetime string* ')

"""
