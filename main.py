"""Module docstring.

This serves as a long usage message
"""
import csv
import ast
import urllib.error as error
import urllib.request as request

IMPORT = 'data/srdr_user_desc_stats_20131025.csv'
EXPORT = 'output/sample.csv'

def _get_location(row):
    current_ip = row['current_login_ip']
    last_ip = row['last_login_ip']

    if current_ip == "":
        json_current = {'country_name': "", 'region_name': ""}
    else:
        json_current = _fetch_json(current_ip)
    if last_ip == "":
        json_last = {'country_name': "", 'region_name': ""}
    else:
        json_last = _fetch_json(last_ip)

    return json_current['country_name'], json_current['region_name'],\
      json_last['country_name'], json_last['region_name']

def _fetch_json(ip):
    url_str = "http://freegeoip.net/json/%s" % ip

    try:
        # Get response object
        response = request.urlopen(url_str)
    except error.HTTPError as err:
        json = {'country_name': '--not found--',
                'region_name': '--not found--'}
    else:
        response = response.readline()
        # Convert byte reponse to string
        response_string = response.decode(encoding='UTF-8')
        json = _string_into_dict(response_string)
    return json

def _string_into_dict(s):
    return ast.literal_eval(s)

def main():
    export = []
    fieldnames = ['login', 'email', 'fname', 'lname', 'user_type',
                  'login_count', 'current_login_ip', 'last_login_ip',
                  'created_at', 'organization', 'Organization Type',
                  'current_country', 'current_region', 'last_country',
                  'last_region', 'Repeat']

    with open(IMPORT, newline='') as csvfile:
        csvdict = csv.DictReader(csvfile)
        for row in csvdict:
            current_country, current_region,\
              last_country, last_region = _get_location(row)

            #print(_get_location(row))
            row.update({'current_country': current_country,
                        'current_region': current_region,
                        'last_country': last_country,
                        'last_region': last_region})
            export.append(row)

    with open(EXPORT, 'w', newline='') as csvfile:
        csvwriter = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames, extrasaction='ignore')
        csvwriter.writeheader()
        csvwriter.writerows(export)

if __name__ == "__main__":
    main()
    print("Done.")
