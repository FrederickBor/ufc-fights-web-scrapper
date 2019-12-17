import requests
import datetime
import csv
from bs4 import BeautifulSoup
import threading

def getMonthNumber(month):
    """
    Change the months from string to int.
    """
    months = {
        "Jan":1,
        "Feb":2,
        "Mar":3,
        "Apr":4,
        "May":5,
        "Jun":6,
        "Jul":7,
        "Aug":8,
        "Sep":9,
        "Oct":10,
        "Nov":11,
        "Dec":12
    }
    return months[month]

def writeInFile(fights, file_out):
    """
    Generates a .csv file with the given name (file_out) and saves in it the list of fights (fights).
    """
    with open(file_out, 'w',newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Date", "Fighter1", "Fighter2", "classFighter1", "classFighter2", "Winner", "Method", "Referee", "Rounds", "Time"])
        writer.writerows(fights)

def getFighterClass(url):
    """
    Searchs, on the given url, the weight class.
    If not exists writes "N/A".
    """
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    f_class = soup.find("h6",{"class": "item wclass"}).find("a")
    if (f_class != None):
        return f_class.text
    return "N/A"

def getfights(date, url, thread):
    """
    Obtains all the fights info on given url.
    There are some pages that doesn't contains information, for those this fuction returns an empty list.
    """
    counter = 0
    fights = list()
    # Send the request to the url to have its HTML
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    try:
        first_fight =  soup.find("div", {"class": "module fight_card"})
        table = soup.find("div", {"class": "module event_match"}).find("table")
    except:
        return fights
    
    # The first fight is structured in a diferent way than the others.
    try:
        fighters = first_fight.find("div", {"class": "fight"}).find_all("h3")
        fighter1 = fighters[0].find("span").string
        fighter2 = fighters[1].find("span").string
        whoWins = first_fight.find("div", {"class": "fight"}).find_all("span", {"class": "final_result"})
        
        if (whoWins[0].string == "win"):
            winner = fighter1
        elif (whoWins[1].string == "win"): 
            winner = fighter2
        else:
            winner = "Draw"
        
        aux = first_fight.find("div", {"class": "footer"}).find_all("td")
        method = " ".join(aux[1].text.split()[1::])
        referee = " ".join(aux[2].text.split()[1::])
        rounds = " ".join(aux[3].text.split()[1::])
        time = " ".join(aux[4].text.split()[1::])
        fighter1Url = "https://www.sherdog.com" + fighters[0].find("a")["href"]
        fighter2Url = "https://www.sherdog.com" + fighters[1].find("a")["href"]
        classFighter1 = getFighterClass(fighter1Url)
        classFighter2 = getFighterClass(fighter2Url)

        fight = [date,fighter1,fighter2,classFighter1,classFighter2,winner,method,referee,rounds,time]
        fights.append(fight)
        counter += 1
        print("Thread #{}".format(thread),counter)
    except Exception as e:
        print("Thread #{}".format(thread), date, e, "First Fight Error")
        pass

    # The other fights are on a table
    for tr in table.find_all("tr"):
        if (tr != table.find_all("tr")[0]):
            try:
                aux = tr.find_all("td")
                fighter1 = aux[1].find("a").find("span").text
                fighter2 = aux[3].find("a").find("span").text
                fighter1Result = aux[1].find("span", {"class": "final_result"})
                fighter2Result = aux[3].find("span", {"class": "final_result"})
                if (fighter1Result.string == "win"):
                    winner = fighter1
                elif (fighter2Result.string == "win"): 
                    winner = fighter2
                else:
                    winner = "Draw"
                method = " ".join(aux[4].text.split()[:1:])
                referee = " ".join(aux[4].text.split()[2::])
                rounds = aux[5].text
                time = aux[6].text
                fighter1Url = "https://www.sherdog.com" + aux[1].find("div", {"class": "fighter_result_data"}).find("a")["href"]
                fighter2Url = "https://www.sherdog.com" + aux[3].find("div", {"class": "fighter_result_data"}).find("a")["href"]
                classFighter1 = getFighterClass(fighter1Url)
                classFighter2 = getFighterClass(fighter2Url)
                fight = [date,fighter1,fighter2,classFighter1,classFighter2,winner,method,referee,rounds,time]
                fights.append(fight)
                counter += 1
                print("Thread #{}".format(thread),counter)
            except Exception as e:
                print("Thread #{}".format(thread), date, e, "Table Fights Error")
                pass
    
    return fights

def tableLoop(table, thread):
    """
    This function obtains all the urls for the fights sites,
    saves the date and gets all the fights on the generated url.

    Returns a list with all the fights on each row of the table.
    """
    fights = list()
    for tr in table.find_all("tr"):
        if (tr != table.find_all("tr")[0]):
            year = int(tr.find("span", {"class": "year"}).string)
            month = getMonthNumber(tr.find("span", {"class": "month"}).string)
            day = int(tr.find("span", {"class": "day"}).string)
            date = datetime.datetime(year, month, day)
            fights_url = tr.find("a")["href"]
            url = "https://www.sherdog.com" + fights_url
            # Let's obtain the fights on the url
            fights += getfights(date, url, thread)
    return fights
    
def multimain(url,file_out,thread):
    """
    Main program (Multithread).

    This is in charge to initiate the data scrapping and to generate a .csv file.
    """
    fights = list()
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    table = soup.find("div", {"id": "recent_tab"}).find("table", {"class": "event"})
    fights += tableLoop(table,thread)
    number = url.split("/")[-1]
    file_out = "UFC_Fights_{}.csv".format(number)
    # Write the fights on the .csv file.
    writeInFile(fights,file_out)

if __name__ == "__main__":
    url = "https://www.sherdog.com/organizations/Ultimate-Fighting-Championship-UFC-2/recent-events/{PAGE}"
    file_out = "UFC_Fights_{PAGE}.csv"
    threads = list()

    x = 7
    
    # Creates a list with "x-1" number of threads (one per page)
    for i in range(1,x):
        threads.append(threading.Thread(target=multimain,args=(url.format(PAGE=i),file_out.format(PAGE=i),i)))
    
    # Start all the threads
    for t in threads:
        t.start()

    # Wait for all threads end
    for t in threads:
        t.join()
