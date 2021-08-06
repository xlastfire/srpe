import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = 'https://www.penpalsnow.com/do/search.html'


def scrape(s=None, ads_from=0, ads_to=0, gender='male', age_group='19-22', country='', language='', only_emails=False,
           mail_obj=None, total_obj=None):
    if s is None:
        login_data = {
            'sex': gender,
            'agegroup': age_group,
            'hobbies': '',
            'country': country,
            'city': '',
            'language': language,
            'search': 'Find penpals!',
            'numb': '0',
            'search': 'Find penpals!'
        }
        with requests.Session() as s:
            r = s.get(url)
            r = s.post(url, data=login_data)
        ads_from += 5
    else:
        login_data = {
            'numb': ads_from,
            'transfer': gender + '||X||' + age_group + '||X||||X||||X||||X||||X||||X||',
            'search': 'Next + 5 + pen + pal + ads'
        }
        r = s.post(url, data=login_data)
        ads_from += 5
    soup = BeautifulSoup(r.content, 'html5lib')

    uu = 'https://www.penpalsnow.com/_api/showemail.php?e='
    ids = []
    for word in r.text.split(" "):
        if 'id="' in word:
            ids.append(word.split('"')[1])

    if only_emails:
        for id in ids:
            email = requests.get(uu + id).text

    paragraphs = soup.find_all('p')
    paras = []
    for para in paragraphs:
        paras.append(para)
    found = 0
    for i in range(2, len(paras)):
        if only_emails:
            break
        vals = paras[i].find_all('span', class_='ppadvaluebold')
        if len(vals) != 3:
            continue
        # print(paras[i])
        name = str(vals[0].text).strip()
        gender = str(vals[1].text).strip()
        age = str(vals[2].text).strip()
        address = str(paras[i].find('address').find('span', class_='ppadvalue').text).strip().replace("\n",
                                                                                                      ',').replace(
            '       ', ' ')

        email = requests.get(uu + ids[found]).text
        if mail_obj is not None:
            mail_obj.write(email + '\n')

        para = str(paras[i].find('span', class_='ppadvaluemsg').text).strip().replace("\n\n", '\n')
        date = str(paras[i].find('span', class_='ppaddatevalue').text).strip()

        out = f'Name - {name} Age - {age} Gender - {gender} Email - {email}\n Address - {address} Last Modified - {date[:4]}/{date[4:6]}/{date[6:]} \n Msg - {para}\n'
        if total_obj is not None:
            try:
                total_obj.write(out+'\n\n')
            except:
                total_obj.write('UNICODE ERROR\n\n')

        print(out)
        print('-------------------------------------------------------------------')
        found += 1

    if ads_to <= ads_from:
        return
    else:
        scrape(s, ads_from, ads_to, gender, age_group, country, language, only_emails, mail_obj=mail_obj,
               total_obj=total_obj)


countries = {"afghanistan": "AF",
             "albania": "AL",
             "algeria": "DZ",
             "american samoa": "AS",
             "andorra": "AD",
             "angola": "AO",
             "anguilla": "AI",
             "antarctica": "AQ",
             "antigua and barbuda": "AG",
             "argentina": "AR",
             "armenia": "AM",
             "aruba": "AW",
             "australia": "AU",
             "austria": "AT",
             "azerbaijan": "AZ",
             "bahamas": "BS",
             "bahrain": "BH",
             "bangladesh": "BD",
             "barbados": "BB",
             "belarus": "BY",
             "belgium": "BE",
             "belize": "BZ",
             "benin": "BJ",
             "bermuda": "BM",
             "bhutan": "BT",
             "bolivia": "BO",
             "bosnia and herzegovina": "BA",
             "botswana": "BW",
             "bouvet island": "BV",
             "brazil": "BR",
             "british indian ocean territory": "IO",
             "brunei darussalam": "BN",
             "bulgaria": "BG",
             "burkina faso": "BF",
             "burundi": "BI",
             "cambodia": "KH",
             "cameroon": "CM",
             "canada": "CA",
             "cape verde": "CV",
             "cayman islands": "KY",
             "central african republic": "CF",
             "chad": "TD",
             "chile": "CL",
             "china": "CN",
             "christmas island": "CX",
             "cocos (keeling) islands": "CC",
             "colombia": "CO",
             "comoros": "KM",
             "congo": "CG",
             "cook islands": "CK",
             "costa rica": "CR",
             "cote d'ivoire (ivory coast)": "CI",
             "croatia (hrvatska)": "HR",
             "cuba": "CU",
             "cyprus": "CY",
             "czech republic": "CZ",
             "czechoslovakia (former)": "CS",
             "denmark": "DK",
             "djibouti": "DJ",
             "dominica": "DM",
             "dominican republic": "DO",
             "east timor": "TP",
             "ecuador": "EC",
             "egypt": "EG",
             "el salvador": "SV",
             "equatorial guinea": "GQ",
             "eritrea": "ER",
             "estonia": "EE",
             "ethiopia": "ET",
             "falkland islands (malvinas)": "FK",
             "faroe islands": "FO",
             "fiji": "FJ",
             "finland": "FI",
             "france": "FR",
             "france, metropolitan": "FX",
             "french guiana": "GF",
             "french polynesia": "PF",
             "french southern territories": "TF",
             "gabon": "GA",
             "gambia": "GM",
             "georgia (sakartvelo) - not us state!": "GE",
             "germany": "DE",
             "ghana": "GH",
             "gibraltar": "GI",
             "great britain (uk)": "GB",
             "greece": "GR",
             "greenland": "GL",
             "grenada": "GD",
             "guadeloupe": "GP",
             "guam": "GU",
             "guatemala": "GT",
             "guinea": "GN",
             "guinea-bissau": "GW",
             "guyana": "GY",
             "haiti": "HT",
             "heard and mcdonald islands": "HM",
             "honduras": "HN",
             "hong kong": "HK",
             "hungary": "HU",
             "iceland": "IS",
             "india": "IN",
             "indonesia": "ID",
             "iran": "IR",
             "iraq": "IQ",
             "ireland": "IE",
             "israel": "IL",
             "italy": "IT",
             "jamaica": "JM",
             "japan": "JP",
             "jordan": "JO",
             "kazakhstan": "KZ",
             "kenya": "KE",
             "kiribati": "KI",
             "korea (north)": "KP",
             "korea (south)": "KR",
             "kuwait": "KW",
             "kyrgyzstan": "KG",
             "laos": "LA",
             "latvia": "LV",
             "lebanon": "LB",
             "lesotho": "LS",
             "liberia": "LR",
             "libya": "LY",
             "liechtenstein": "LI",
             "lithuania": "LT",
             "luxembourg": "LU",
             "macau": "MO",
             "macedonia": "MK",
             "madagascar": "MG",
             "malawi": "MW",
             "malaysia": "MY",
             "maldives": "MV",
             "mali": "ML",
             "malta": "MT",
             "marshall islands": "MH",
             "martinique": "MQ",
             "mauritania": "MR",
             "mauritius": "MU",
             "mayotte": "YT",
             "mexico": "MX",
             "micronesia": "FM",
             "moldova": "MD",
             "monaco": "MC",
             "mongolia": "MN",
             "montenegro": "ME",
             "montserrat": "MS",
             "morocco": "MA",
             "mozambique": "MZ",
             "myanmar": "MM",
             "namibia": "NA",
             "nauru": "NR",
             "nepal": "NP",
             "netherlands": "NL",
             "netherlands antilles": "AN",
             "neutral zone": "NT",
             "new caledonia": "NC",
             "new zealand (aotearoa)": "NZ",
             "nicaragua": "NI",
             "niger": "NE",
             "nigeria": "NG",
             "niue": "NU",
             "norfolk island": "NF",
             "northern mariana islands": "MP",
             "norway": "NO",
             "oman": "OM",
             "pakistan": "PK",
             "palau": "PW",
             "panama": "PA",
             "papua new guinea": "PG",
             "paraguay": "PY",
             "peru": "PE",
             "philippines": "PH",
             "pitcairn": "PN",
             "poland": "PL",
             "portugal": "PT",
             "puerto rico": "PR",
             "qatar": "QA",
             "reunion": "RE",
             "romania": "RO",
             "russian federation": "RU",
             "rwanda": "RW",
             "s. georgia and s. sandwich isls.": "GS",
             "saint kitts and nevis": "KN",
             "saint lucia": "LC",
             "saint vincent and the grenadines": "VC",
             "samoa": "WS",
             "san marino": "SM",
             "sao tome and principe": "ST",
             "saudi arabia": "SA",
             "senegal": "SN",
             "serbia": "RS",
             "seychelles": "SC",
             "sierra leone": "SL",
             "singapore": "SG",
             "slovak republic": "SK",
             "slovenia": "SI",
             "solomon islands": "Sb",
             "somalia": "SO",
             "south africa": "ZA",
             "spain": "ES",
             "sri lanka": "LK",
             "st. helena": "SH",
             "st. pierre and miquelon": "PM",
             "sudan": "SD",
             "suriname": "SR",
             "svalbard and jan mayen islands": "SJ",
             "swaziland": "SZ",
             "sweden": "SE",
             "switzerland": "CH",
             "syria": "SY",
             "taiwan": "TW",
             "tajikistan": "TJ",
             "tanzania": "TZ",
             "thailand": "TH",
             "togo": "TG",
             "tokelau": "TK",
             "tonga": "TO",
             "trinidad and tobago": "TT",
             "tunisia": "TN",
             "turkey": "TR",
             "turkmenistan": "TM",
             "turks and caicos islands": "TC",
             "tuvalu": "TV",
             "us minor outlying islands": "UM",
             "ussr (former)": "SU",
             "uganda": "UG",
             "ukraine": "UA",
             "united arab emirates": "AE",
             "united kingdom": "UK",
             "united states": "US",
             "uruguay": "UY",
             "uzbekistan": "UZ",
             "vanuatu": "VU",
             "vatican city state (holy see)": "VA",
             "venezuela": "VE",
             "viet nam": "VN",
             "virgin islands (british)": "VG",
             "virgin islands (u.s.)": "VI",
             "wallis and futuna islands": "WF",
             "western sahara": "EH",
             "yemen": "YE",
             "yugoslavia (former)": "YU",
             "zaire": "ZR",
             "zambia": "ZM",
             "zimbabwe": "ZW"
             }


def get_values():
    now = datetime.now()
    to_str = now.strftime("%H:%M:%S").replace(':', '.')
    mail_file = to_str + '_mails.txt'
    total_file = to_str + '_total.txt'
    mail_obj = open(mail_file, 'w')
    total_obj = open(total_file, 'w')

    gender = ''
    age_group = ''
    number_of_ads = 0
    country = ''
    only_emails = False

    print('Gender')
    print('1.Male\t2.Female')
    choice = input('Answer > ')
    if choice == '1':
        gender = 'male'
    elif choice == '2':
        gender = 'female'

    print('Age Group')
    print('1.(16-18) 2.(19-22) 3.(23-30) 4.(31-40) 5.(41-50) 6.(50+)')
    choice = input('Answer > ')
    if choice == '1':
        age_group = '16-18'
    elif choice == '2':
        age_group = '19-22'
    elif choice == '3':
        age_group = '23-30'
    elif choice == '4':
        age_group = '31-40'
    elif choice == '5':
        age_group = '41-50'
    elif choice == '6':
        age_group = '50+'

    print('Country')
    cou = input('Answer >')
    if cou.lower() in countries:
        country = countries[cou]
    else:
        print('Country not Found')

    print('Number of ads')
    try:
        number = int(input('Answer >'))
    except:
        print('Bad Input')
        return
    if number < 0 or number > 100:
        print('0-100 accepted')
        return
    else:
        number_of_ads = number

    print('Only emails')
    print('1.True')
    choice = input('Answer >')
    if choice == '1':
        only_emails = True

    scrape(ads_from=0, ads_to=number_of_ads, gender=gender, age_group=age_group, country=country,
           only_emails=only_emails, mail_obj=mail_obj, total_obj=total_obj)
    mail_obj.close()
    total_obj.close()


if __name__ == '__main__':
    get_values()

# TODO -> add skip first pages
