import argparse
import time
import re
from datetime import datetime
import sys

""" Background Color """
On_Black = '\033[40m'
On_Red = '\033[41m'
On_Cyan = '\033[46m'
On_Yellow = '\033[43m'
On_Purple='\033[45m'


class LogWatcher():
    """ Main class for log watcher """

    def __init__(self, verbose, interval, logfile, address):
        """ Init the variable with creating the class.
        :param verbose:     is a switch to print IDs that are older than 1 day, default is False
        :param interval:    intervals in second for tailf function
        :param logfile:     log file name with full path
        """
        self.data = {}
        self.print_all = verbose
        self.interval = interval
        self.logfile = logfile
        self.address = address

    def cls(self):
        """ Clears the screen and prints the headers with current time on top of the screen """
        print "\033[H\033[J"
        print time.strftime('%d/%b/%Y:%H:%M:%S')
        if self.address:
            headers = "|  ID  | STATUS |        FIRST         |        LAST          |{0:^32}|{1:^17}|".format("DELTA","IP")
            header_line = "+======+========+======================+======================+================================+=================+"
        else:
            headers = "|  ID  | STATUS |        FIRST         |        LAST          |{0:^32}|".format("DELTA")
            header_line = "+======+========+======================+======================+================================+"

        print header_line
        print headers
        print header_line

    @staticmethod
    def time_diff(first_seen, last_seen):
        """
        :param first_seen:  datetime string
        :param last_seen:   datetime string
        :return:            difference in time between the two variables above
        """
        fmt = '%d/%b/%Y:%H:%M:%S'
        d1 = datetime.strptime(first_seen, fmt)
        d2 = datetime.strptime(last_seen, fmt)
        return d2 - d1

    def read_initial_log(self):
        """
        :return: nothing, it updates the main Data dataframe with most up to date time per ID
        """
        with open(self.logfile, "r") as fd:
            f = fd.read()
            for line in f.split("\n"):
                parts = self.matcher(line)
                if parts:
                    self.update_data(parts)
        self.cls()
        self.status()

    def tailf_log(self):
        """
        Main tailf function to clear the screen and writes the status.

        <<< TO BE FIXED WITH REAL TAILF >>>

        :return: Nothing
        """

        # Start editing part
        with open(self.logfile, "r") as fd:
            f = fd.read()
            for line in f.split("\n"):

            # End editing part
            # Could be replaced with the other log watcher but instead of printing the lines
            # it can run the matcher and update_data methods on it.
            # Warning: this suggestion is not tested

                parts = self.matcher(line)
                if parts:
                    self.update_data(parts)
        time.sleep(self.interval)

        self.cls()
        self.status()


    def how_old(self, delta):
        """
        :param delta:   How old/time difference; it adds coloring char depending on how old.
        0 - 5 min:      Purple background
        6 - 10 min:     Yellow background
        11 - 30 min:    Cyan background
        31+ min:        No color, default of system terminal color
        1+ days:        Red backgound
        :return: delta with color padding
        """
        delta = str(delta)

        if "day" in delta:
            if self.print_all:
                # Sometimes the diff is 1 second based on the time that the log file was read,
                # if so it will print purple
                if "-1 day" not in delta:
                    delta = "{}{}{}".format(On_Red, delta, On_Black)
                else:
                    delta = "{}{}{}".format(On_Purple, delta, On_Black)
            else:
                return False
        else:
            p = delta.split(":")
            h = p[0].strip()
            m = p[1].strip()

            if int(h) == 0:
                if 0 <= int(m) <= 5:
                    delta = "{}{}{}".format(On_Purple, delta, On_Black)
                elif 5 < int(m) <= 10:
                    delta = "{}{}{}".format(On_Yellow, delta, On_Black)
                elif 10 < int(m) <= 30:
                    delta = "{}{}{}".format(On_Cyan, delta, On_Black)
        return delta

    def status(self):
        """
        Main status printer, sorts per delta prints most recent ones on top
        :return: nothing
        """
        sorted_data = sorted(self.data.items(), key=lambda k: k[1][4], reverse=False)

        for k in sorted_data:
            line = k[1]
            delta = self.how_old(line[4])
            if delta:
                if self.address:
                    print "| {} |  {}  | {} | {} | {} |{}|".format(line[0], line[1], line[2], line[3], delta, line[5])
                else:
                    print "| {} |  {}  | {} | {} | {} |".format(line[0], line[1], line[2], line[3], delta)

    def update_data(self, parts):
        """
        :param parts:   given the parts of a log line, it updates the main dataframe per ID
        :return: nothing
        """
        ip = parts[0]
        uniq_id = parts[1]
        status = parts[3]
        last_seen = parts[2]
        now = time.strftime('%d/%b/%Y:%H:%M:%S')

        if self.data.get(parts[1]):
            first_seen = self.data.get(parts[1])[2]
            delta = self.time_diff(last_seen, now)
        else:
            first_seen = last_seen
            delta = self.time_diff(first_seen, last_seen)
        if self.address:
            info = [uniq_id, "{0:^4}".format(status), first_seen, last_seen, "{0:^30}".format(delta), "{0:^17}".format(ip)]
        else:
            info = [uniq_id, "{0:^4}".format(status), first_seen, last_seen, "{0:^30}".format(delta)]

        self.data.update({info[0]: info})

    @staticmethod
    def matcher(line):
        """ Function to extract parts of the log line by regex.
            For future releases this could be imported from multiple
            matching group that can be specified per cmd switch

            good_parts = [ip, uniq_id, dtg, status]

            is the final line that should be there.
            All edits must result this list in that specific order of elements.
        """

        # Start custom matcher/extractor
        # If this used, comment out the default matcher/extractor
        """
        if <either 200, 400, GET, or POST in line>:
            if <extra match, .png, .xml, etc... in line>:            
                parts list from <split or regex>
                ip      = <IP address ex. 1.1.1.1>
                uniq_id = <Uniq 4 char ID ex. ABCD>
                dtg     = <Timestamp of the log line ex. 22/Sep/2018:12:34:12
                status  = <Status code 4 char, could be anything. Recommanded GET or POST ex. GET  
        """
        # End custom matcher/extractor

        # Start default matcher/extractor
        if "GET" or "POST" in line:
            if ".png" in line:
                # Example line
                # 127.0.0.1 - ABCD [22/Sep/2018:12:34:12 -0700] "GET /sample-image.png HTTP/2" 200 1479
                # regex below has 4 () aka matching groups [IP, ID, DTG, STATUS]
                #    IP        ID           DTG                  STATUS
                regex = '([(\d\.)]+) - ([A-Z0-9]+) \[(.*?)\] \"(GET|POST)'

                if re.match(regex, line):
                    parts = re.match(regex, line).groups()
                    ip = parts[0]
                    uniq_id = parts[1]
                    dtg = parts[2].split(" -")[0]
                    status = parts[3]

        # End default matcher/extractor

                    good_parts = [ip, uniq_id, dtg, status]
                    return good_parts

if __name__ == '__main__':
    """ Run the main program """
    parser = argparse.ArgumentParser(""" Generic Log Watcher """)
    parser.add_argument("-a", "--address", help="Prints the IP address of last log line per ID", action="store_true")
    parser.add_argument("-f", "--file", type=str, help="Log file full path and name")
    parser.add_argument("-i", "--interval", type=int, default=5, help="Interval in N seconds to re-read the log file")
    parser.add_argument("-v", "--verbose", help="Prints all the IDs no matter how old", action="store_true")

    args = parser.parse_args()

    if not args.file:
        print "No log file provided"
        sys.exit(0)

    lw = LogWatcher(args.verbose, args.interval, args.file, args.address)
    lw.read_initial_log()

    try:
        while True:
            try:
                lw.tailf_log()
            except:
                "Print might found error in a log file line."
    except KeyboardInterrupt:
        print('interrupted!')
