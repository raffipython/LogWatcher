# LogWatcher
Generic Log Watcher
NAME
    LogWatcher

FILE
    LogWatcher.py

CLASSES
    LogWatcher
    
    class LogWatcher
     |  Main class for log watcher
     |  
     |  Methods defined here:
     |  
     |  __init__(self, verbose, interval, logfile, address)
     |      Init the variable with creating the class.
     |      :param verbose:     is a switch to print IDs that are older than 1 day, default is False
     |      :param interval:    intervals in second for tailf function
     |      :param logfile:     log file name with full path
     |  
     |  cls(self)
     |      Clears the screen and prints the headers with current time on top of the screen
     |  
     |  how_old(self, delta)
     |      :param delta:   How old/time difference; it adds coloring char depending on how old.
     |      0 - 5 min:      Purple background
     |      6 - 10 min:     Yellow background
     |      11 - 30 min:    Cyan background
     |      31+ min:        No color, default of system terminal color
     |      1+ days:        Red backgound
     |      :return: delta with color padding
     |  
     |  read_initial_log(self)
     |      :return: nothing, it updates the main Data dataframe with most up to date time per ID
     |  
     |  status(self)
     |      Main status printer, sorts per delta prints most recent ones on top
     |      :return: nothing
     |  
     |  tailf_log(self)
     |      Main tailf function to clear the screen and writes the status.
     |      
     |      <<< TO BE FIXED WITH REAL TAILF >>>
     |      
     |      :return: Nothing
     |  
     |  update_data(self, parts)
     |      :param parts:   given the parts of a log line, it updates the main dataframe per ID
     |      :return: nothing
     |  
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |  
     |  matcher(line)
     |      Function to extract parts of the log line by regex.
     |      For future releases this could be imported from multiple
     |      matching group that can be specified per cmd switch
     |      
     |      good_parts = [ip, uniq_id, dtg, status]
     |      
     |      is the final line that should be there.
     |      All edits must result this list in that specific order of elements.
     |  
     |  time_diff(first_seen, last_seen)
     |      :param first_seen:  datetime string
     |      :param last_seen:   datetime string
     |      :return:            difference in time between the two variables above

DATA
    On_Black = '\x1b[40m'
    On_Cyan = '\x1b[46m'
    On_Purple = '\x1b[45m'
    On_Red = '\x1b[41m'
    On_Yellow = '\x1b[43m'
