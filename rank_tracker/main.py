import requests
import warnings
import threading
import time, os, pickle
from time import gmtime, strftime
from requests.status_codes import codes


"""
You might want to check if your internet connection can access <username>.github.io/os212/
within a reasonable time. If you encounter a connection error from this script, you may need
to re-check your connection.
"""



# menghilangkan warning
warnings.filterwarnings("ignore")




def main():
    result = get_voted_multithreading()

    file_update = open(strftime("update %Y-%m-%d %H-%M.txt"), 'w')

    print()
    print()

    result_key_sorted = sorted(result.keys())
    for voted_acc in result_key_sorted:
        weeks = sorted(result[voted_acc].keys(), reverse=True)
        total_vote = 0

        for week in weeks:
            total_vote += len(result[voted_acc][week])
        
        print(f"{voted_acc} ({total_vote}):")
        print(f"{voted_acc} ({total_vote}):", file=file_update)
        
        for week in weeks:
            week_vote_count = len(result[voted_acc][week])
            print_msg = f"    W{week:02d} ({week_vote_count}) = {', '.join(result[voted_acc][week])}"
            print(print_msg)
            print(print_msg, file=file_update)
        print()
        print(file=file_update)


    print()
    print()
    print("DONE. The result also has been saved to your disk")







# credits: https://stackoverflow.com/a/6894023/7069108
class ThreadWithReturnValue(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
        
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return





with open("os_acc_list.txt", 'r') as f:
    account_list = f.read().strip().split("\n")



FIVETEEN_MINUTES = 60*5

# Membuka request cache asalkan tidak lebih dari 5 menit yang lalu
if (os.path.isfile("cache") and (time.time() - os.path.getmtime("cache")) < FIVETEEN_MINUTES):
    with open("cache", 'rb') as f:
        request_cache = pickle.load(f)
        reused_cache = request_cache.copy()
    did_reuse_cache = True
else:
    request_cache = {}
    did_reuse_cache = False


def save_request_cache():
    if not did_reuse_cache or len(request_cache) > len(reused_cache):
        with open("cache", 'wb') as f:
            pickle.dump(request_cache, f)

def make_a_request(url, verify, timeout):
    if url in request_cache:
        return request_cache[url]

    req = requests.get(url, verify=verify, timeout=timeout)
    request_cache[url] = req
    return req





# key: the voted person
# value:
#   Another dictionary:
#       key:   the number of week (int)
#       value: a list of the voter
voter = {}


def get_voted():  # return the voted account as the key and the voters as a the value

    # key: the voted account. value: another dictionary <week:int, voters:list>
    ret = {}
    
    for acc in account_list:
        votes = get_votes(acc)

        for week in votes:
            for voted_acc_dict in votes[week]:
                voted_acc = voted_acc_dict['voted']
                
                if voted_acc not in ret:
                    ret[voted_acc] = {}

                if week not in ret[voted_acc]:
                    ret[voted_acc][week] = []

                ret[voted_acc][week].append(f"{acc}[{voted_acc_dict['rank']}]")
    return ret



def get_voted_multithreading():
    # key: the voted account. value: another dictionary <week:int, voters:list>
    ret = {}
    MAX_NUM_OF_REQ_AT_A_TIME = 20

    threads = {}  # key: the voter account, value: the thread

    counter = 0
    for acc in account_list:
        thread = ThreadWithReturnValue(target=get_votes, args=(acc,))
        thread.start()
        threads[acc] = thread
        
        counter += 1
        if counter % MAX_NUM_OF_REQ_AT_A_TIME == 0:
            print(counter)

            try:
                process_the_threads(ret, threads)
            except Exception as e:
                save_request_cache()
                raise e
            
            time.sleep(1)

            if counter % (2*MAX_NUM_OF_REQ_AT_A_TIME) == 0:
                save_request_cache()
            
    process_the_threads(ret, threads)

    return ret


def process_the_threads(return_dict, threads_dict):
    ret = return_dict
    
    for acc, thread in threads_dict.items():
        print(f"getting {acc}")

        votes = thread.join()
        for i in range(2):  # up to 2 times retry
            if (votes is not None):
                break
            votes = get_votes(acc)
        
        # print(acc, thread, votes)

        for week in votes:
            for voted_acc_dict in votes[week]:
                voted_acc = voted_acc_dict['voted']
                voted_acc = voted_acc.lower()
                
                if voted_acc not in ret:
                    ret[voted_acc] = {}

                if week not in ret[voted_acc]:
                    ret[voted_acc][week] = []

                ret[voted_acc][week].append(f"{acc}[{voted_acc_dict['rank']}]")
    threads_dict.clear()

      

def get_votes(voter_account, max_try_count=4, connection_time_out=10):
    # returns a dict of <int, list<dict>>
    # where the key is the week, and the list
    # is a list a dict<string, string> that contains:
    #       'voted': the voted person
    #       'rank' : the voted person's rank

    url = f"http://{voter_account}.github.io/os212/TXT/myrank.txt"
    allowed_status = (codes.OK, codes.NOT_FOUND)

    req = None
    for i in range(max_try_count):
        try:
            if (req := make_a_request(url, False, connection_time_out)
                ).status_code in allowed_status:
                break
        except requests.exceptions.ReadTimeout:
            pass
    else:
        msg = ""
        if req is not None:
            msg = f"req status code: {req.status_code}"
        raise ConnectionError(msg)

    if req.status_code == codes.NOT_FOUND:
        return {}

    text = req.text
    lines = text.split("\n")
    ret = {}

    week_number_of_person = {}  # to track the rank of each week

    for line in lines:
        try:
            line = line.strip()
            
            if line.startswith("#"):
                continue
            if (line.lower().startswith("zczc")):
                split_line = line.split()
                
                week_num = int(split_line[1][1:])
                if week_num not in ret:
                    ret[week_num] = []
                    week_number_of_person[week_num] = 1

                voted = split_line[2]
                ret[week_num].append(
                    {
                        'voted': voted,
                        'rank': week_number_of_person[week_num]
                    }
                    )
                week_number_of_person[week_num] += 1
        except Exception as e:
            print()
            print("------------ ERROR ------------")
            print(url)
            print(line)
            print("-------------------------------")
            print()
    return ret



main()
