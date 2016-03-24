import urllib3
import time
import praw
from bs4 import BeautifulSoup
import time


class TankBot(object):
    def __init__(self):
        # Grab the important stuff.
        self.username = input('Reddit Username: ')
        self.password = input('Reddit Password: ')
        self.subreddit = input('Subreddit(without the /r/): ')
        self.userAgent = 'TankBot 1.0 by /u/schlaBAM'

    @staticmethod
    def scrape():
        http = urllib3.PoolManager()
        r = http.request('GET', 'http://canucks.nhl.com/club/standings.htm?type=LEA')
        soup = BeautifulSoup(r.data, "html5lib")
        tank_list = []

        rawdata_list = [tr.findAll('td') for tr in soup.table.findAll('tr')]

        # Make the list all nice and only text.
        for row in rawdata_list:
            tank_list.append([cell.text for cell in row])

        # Remove accents. God damn Montreal.
        stupid_french_team = "MontrÃ©al"

        tank_list = [[x.replace(stupid_french_team, 'Montreal') for x in i] for i in tank_list]

        return tank_list

    @staticmethod
    def generate_tables(tank_list):

        standings = "\nLast Updated: " + time.strftime("%b %d %Y %I:%M:%S", time.localtime()) + " PST\n"
        standings += "\n|Team|GP|W|L|OTL|PTS|L10|"
        standings += "\n|:--:|:--:|:--:|:--:|:--:|:--:|:--:|"

        for i in range(20, 31):
            standings += "\n|{0}|{1}|{2}|{3}|{4}|{5}|{6}|".format(tank_list[i][1], tank_list[i][2], tank_list[i][3],
                                                                  tank_list[i][4], tank_list[i][5], tank_list[i][6],
                                                                  tank_list[i][12])
        return standings

    def create_sidebar(self):
        # To fix character glitch when grabbing the sidebar
        # Initialize PRAW and login
        r = praw.Reddit(user_agent='TankBot 1.0 by /u/schlaBAM')
        r.login(self.username, self.password)
        # Grab the sidebar template from the wiki
        sidebar = r.get_subreddit(self.subreddit).get_wiki_page('edit_sidebar').content_md
        # Create list from sidebar by splitting at ***
        sidebar_list = sidebar.split('***')
        # Sidebar with updated tables - +lucky_guess+sidebar_list[6]
        sidebar = (sidebar_list[0] + step1 + sidebar_list[2])

        return sidebar

    def update_reddit(self):
        # Initialize Reddit API, login
        r = praw.Reddit(user_agent=self.userAgent)
        r.login(self.username, self.password)
        # Grab the current settings
        settings = r.get_subreddit(self.subreddit).get_settings()
        # Update the sidebar
        settings['description'] = sidebar
        settings = r.get_subreddit(self.subreddit).update_settings(description=settings['description'])

    # Connecting images to names. Code taken from HockeyBot. Thanks, /u/TeroTheTerror!
    @staticmethod
    def fix_standings(text):
        # Use dictionary to replace team names with sub names
        my_dict = {'Columbus': '[](/r/bluejackets)', 'Pittsburgh': '[](/r/penguins)',
                   'NY Islanders': '[](/r/newyorkislanders)', 'Washington': '[](/r/caps)',
                   'Philadelphia': '[](/r/flyers)', 'NY Rangers': '[](/r/rangers)', 'New Jersey': '[](/r/devils)',
                   'Carolina': '[](/r/canes)',
                   'Boston': '[](/r/bostonbruins)', 'Tampa Bay': '[](/r/tampabaylightning)', 'Montreal': '[](/r/habs)',
                   'Detroit': '[](/r/detroitredwings)', 'Toronto': '[](/r/leafs)', 'Ottawa': '[](/r/ottawasenators)',
                   'Florida': '[](/r/floridapanthers)', 'Buffalo': '[](/r/sabres)', 'Chicago': '[](/r/hawks)',
                   'St. Louis': '[](/r/stlouisblues)', 'Colorado': '[](/r/coloradoavalanche)',
                   'Minnesota': '[](/r/wildhockey)', 'Dallas': '[](/r/dallasstars)', 'Winnipeg': '[](/r/winnipegjets)',
                   'Nashville': '[](/r/predators)', 'Anaheim': '[](/r/anaheimducks)',
                   'San Jose': '[](/r/sanjosesharks)', 'Los Angeles': '[](/r/losangeleskings)',
                   'Vancouver': '[](/r/canucks)', 'Phoenix': '[](/r/coyotes)',
                   'Calgary': '[](/r/calgaryflames)', 'Edmonton': '[](/r/edmontonoilers)'}

        for x, y in my_dict.items():
            text = text.replace(x, y)
        return text

init_tank = TankBot()

while True:
    print('Scraping Standings...')
    lst = init_tank.scrape()
    print('Generating Table...')
    step1 = init_tank.generate_tables(lst)
    print('Fixing Table...')
    step2 = init_tank.fix_standings(step1)
    print('Grabbing Sidebar Template...')
    sidebar = init_tank.create_sidebar()
    print('Updating Sidebar...')
    init_tank.update_reddit()
    print('Sleeping... \n')
    time.sleep(600)
