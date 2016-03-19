import urllib3
# import HTMLParser
# import praw
from bs4 import BeautifulSoup

class TankBot(object):
    def __init__(self):
        # Grab the important stuff.
        self.username = input('Reddit Username: ')
        self.password = input('Reddit Password: ')
        self.subreddit = input('Subreddit(without the /r/): ')
        self.userAgent = 'TankBot 1.0 by /u/schlaBAM'


http = urllib3.PoolManager()
r = http.request('GET', 'http://canucks.nhl.com/club/standings.htm?type=LEA')

soup = BeautifulSoup(r.data, "html5lib")
table = soup.find_all(class_='data')
rows = soup.table.find_all('tr')
tank_list = []

rawdata_list = [tr.findAll('td') for tr in soup.table.findAll('tr')]

# Text only version of rawdata_list
for row in rawdata_list:
    tank_list.append([cell.text for cell in row])

# Remove accents. God damn Montreal.
stupid_french_team = "MontrÃ©al"
fixed_frenchies = "Montreal"

tank_list = [[x.replace(stupid_french_team, 'Montreal') for x in i] for i in tank_list]

standings = "\n|Team|GP|W|L|OTL|Points|L10|"
standings += "\n|:--:|:--:|:--:|:--:|:--:|:--:|:--:|"
for i in range(20, 31):
    standings += "\n|{0}|{1}|{2}|{3}|{4}|{5}|{6}|".format(tank_list[i][1], tank_list[i][2], tank_list[i][3],
                                                          tank_list[i][4], tank_list[i][5], tank_list[i][6],
                                                          tank_list[i][12])
print(standings)

r.close()


# Connecting images to names. Code taken from HockeyBot. Thanks, /u/TeroTheTerror!


def fix_standings(self, text):
    # Use dictionary to replace team names with sub names
    my_dict = {'Columbus': '[](/r/bluejackets)', 'Pittsburgh': '[](/r/penguins)',
               'NY Islanders': '[](/r/newyorkislanders)', 'Washington': '[](/r/caps)', 'Philadelphia': '[](/r/flyers)',
               'NY Rangers': '[](/r/rangers)', 'New Jersey': '[](/r/devils)', 'Carolina': '[](/r/canes)',
               'Boston': '[](/r/bostonbruins)', 'Tampa Bay': '[](/r/tampabaylightning)', 'Montreal': '[](/r/habs)',
               'Detroit': '[](/r/detroitredwings)', 'Toronto': '[](/r/leafs)', 'Ottawa': '[](/r/ottawasenators)',
               'Florida': '[](/r/floridapanthers)', 'Buffalo': '[](/r/sabres)', 'Chicago': '[](/r/hawks)',
               'St. Louis': '[](/r/stlouisblues)', 'Colorado': '[](/r/coloradoavalanche)',
               'Minnesota': '[](/r/wildhockey)', 'Dallas': '[](/r/dallasstars)', 'Winnipeg': '[](/r/winnipegjets)',
               'Nashville': '[](/r/predators)', 'Anaheim': '[](/r/anaheimducks)', 'San Jose': '[](/r/sanjosesharks)',
               'Los Angeles': '[](/r/losangeleskings)', 'Vancouver': '[](/r/canucks)', 'Phoenix': '[](/r/coyotes)',
               'Calgary': '[](/r/calgaryflames)', 'Edmonton': '[](/r/edmontonoilers)'}

    for x, y in my_dict.iteritems():
        text = text.replace(x, y)
    return text
