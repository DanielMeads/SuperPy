import csv
import os
from datetime import timedelta, date, datetime
from rich.table import Table
from rich.console import Console
console = Console()

class Install():
    #Globals for file and data management
    data = os.path.join((os.getcwd()), "data")
    brought = os.path.join((os.getcwd()), "data", "brought.csv")
    sold = os.path.join((os.getcwd()), "data", "sold.csv")
    time = os.path.join((os.getcwd()), "data", "time.csv")
    console = Console()
    #Install start up files.
    def install():
        console.print("This will Install or Reinstall Superpy and will delete all previous data and records please type CONFIRM to continue or cancel to return", style="red bold")
        confirm = input()
        if confirm == "CONFIRM":     
            #Create files and directory for data.
            try:
                os.mkdir(Install.data)
            except FileExistsError:
                pass   
            #Create files, write headers and set current time. Will delete all previous information!
            with open(Install.brought, 'w', newline='') as csvfile:
                file = csv.writer(csvfile)
                file.writerow(['id','product_name','count','buy_price','buy_date','expiry_date'])
                file.writerow(['1', 'example', '4', '3.99', '2022-12-12','2056-12-03'])
                csvfile.close()
            with open(Install.sold, 'w', newline='') as csvfile:
                file = csv.writer(csvfile)
                file.writerow(['id', 'brought_id', 'count', 'sell_price','sell_date', 'product_name'])
                file.writerow(['1', '1', '4', '2.99', '2022-10-12', 'example'])
                csvfile.close()
            with open(Install.time, 'w', newline='') as csvfile:
                file = csv.writer(csvfile)
                file.writerow([date.today()])
                csvfile.close()
            console.print("Superpy has been Initialized", style="green bold")
            return
        elif confirm == "cancel":
            return
        else:
            console.print ("Unrecognised Input", style="magenta")
            Install.install()
    #To reset the date file.
    def reset_date():
        with open(Install.time, 'w', newline='') as csvfile:
            x = csv.writer(csvfile)
            x.writerow([date.today()])
        csvfile.close()
        console.print ("Date Reset", style='green bold')
        return
    #To advance the date file.       
    def advance_time(count=0):
        current_date = Install.load_data(Install.time)
        new_date = current_date + timedelta(days=count)
        with open(Install.time, 'w', newline='') as csvfile:
            file = csv.writer(csvfile)
            file.writerow([new_date])
        csvfile.close()
        console.print (f"Date set to: {new_date}", style='magenta bold')
        return
    #To read the date file.       
    def temporary_date(count=0):
        current_date = Install.load_data(Install.time)
        new_date = current_date + timedelta(days=count)
        return new_date
    #Data fetch
    def load_data(file, list=False):
        data = []
        with open(file, "r", newline='') as csvfile:
            read = csv.reader(csvfile)
            if file == Install.time:
                for row in read:
                    data = formatting.str2date(row[0])  
            else:
                next(read, None)
                for row in read:
                    if list == False:
                        if file == Install.brought:
                            towrite = {'id': int(row[0]), 'product_name': str(row[1]), 'count': int(row[2]), 'buy_price': float(row[3]), 'buy_date': formatting.str2date(row[4]), 'expiration_date': formatting.str2date(row[5])}
                        if file == Install.sold:    
                            towrite = {'id': int(row[0]), 'brought_id': str(row[1]), 'count': int(row[2]), 'sell_price': float(row[3]), 'sell_date': formatting.str2date(row[4]), 'product_name': str(row[5])}
                        data.append(towrite)                       
                    else:
                        data.append(row) 
        csvfile.close()   
        return data

class formatting():
    #Convert strings to date format
    def str2date(string, bymonth=False):
        try:
            if bymonth == False:
                date = datetime.strptime(string, '%Y-%m-%d')
                day = date.date()
                return day
            elif bymonth == True:
                month = datetime.strptime(string, '%Y-%m')
                return month
        except:
            console.print ("Date incorrect Set to 2999-12-12", style="red bold")
            return formatting.str2date('2999-12-12', bymonth)

    #Generate tables
    def table_gen(Name, Headers, products):
            table = Table(title=Name)
            for value in Headers:
                table.add_column(value, justify="right", style="cyan", no_wrap=True)
            if Name == 'Sales Report':
                for product in products:
                    table.add_row(product[0], product[1], product[5], product[2], product[3], product[4], str(int(product[2])*float(product[3])))
            elif Name == 'Products':
                for row in products:
                    table.add_row(row)
            else:
                for product in products:
                    table.add_row(product[0], product[1], product[2], product[3], product[5], str(round(int(product[2])*float(product[3]),2)))
            console.print(table)