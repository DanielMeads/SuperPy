import argparse
from install import Install, formatting
from rich.console import Console
from main import Product, Reports
console = Console()

#Program Information
Superpy = argparse.ArgumentParser(
                prog = "Superpy",
                description = "Command line stock tracking software.",
)

#Defining command line arguments
Superpy.add_argument('-i', '--Install', help='Install or reinstall the required files for Superpy', action="store_true")
Superpy.add_argument('-sd', '--SetDate', help='Reset the date file to today.', action="store_true")
Superpy.add_argument('-ad', '--AdvanceDate', type=int, help="Advance or regress the date by a number of days")
Superpy.add_argument('-pn', '--Productname', type=str, help="Product Name")
Superpy.add_argument('-p', '--Price', type=float, help="Product Price")
Superpy.add_argument('-a', '--Amount', type=float, help="Amount of Product", default=1)
Superpy.add_argument('-ex', '--Expirationdate', type=str, help="Expiration date in 'YYYY-MM-DD' format", default="2999-12-31")
Superpy.add_argument('action', nargs='?', type=str, default='')
Superpy.add_argument('type', nargs='?', type=str, default='')

#Defining date arguments for reporting
temp_date_arguments = Superpy.add_mutually_exclusive_group()
temp_date_arguments.add_argument('-n', '--Now', help='Uses the current date', action="store_true")
temp_date_arguments.add_argument('-t', '--Today', help='Uses the current date', action="store_true")
temp_date_arguments.add_argument('-y', '--Yesterday', help='Set temporary date to yesterday', action="store_true")
temp_date_arguments.add_argument('-m', '--Month', help='Select a year and month (YYYY-MM)', type=str)
temp_date_arguments.add_argument('-d', '--Date', help='Select a date to report on. (YYYY-MM-DD)', type=str)

#Turning command line in to arguments
args = Superpy.parse_args()

#Superpy Actions
if args.Install:
    Install.install()
elif args.SetDate:
    Install.reset_date()
elif args.AdvanceDate:
    Install.advance_time(args.AdvanceDate)
elif args.action == "buy":
    Product.buy(args.Productname, args.Amount, args.Price, args.Expirationdate)
elif args.action == "sell":
    Product.sell(args.Productname, args.Amount, args.Price)
elif args.action == "remove":
    Product.remove(args.Productname, args.Amount, args.Expirationdate)

#Report date arguments
if args.Yesterday:
    temp_date = Install.temporary_date(-1)
    specificdate = True
    datename = "Yesterday's"
elif args.Date:
    temp_date = formatting.str2date(args.Date)
    specificdate = True
    datename = args.Date
elif args.Now or args.Today:
    temp_date = Install.temporary_date()
    specificdate = True
    datename = "Today's"
elif args.Month:
    temp_date = formatting.str2date(args.Month, True)
    specificdate = True
    datename = temp_date
else:
    temp_date = Install.temporary_date()
    specificdate = False
    datename = "Total"

#Report actions
if args.action == "report":
    if args.type == "inventory":
        Reports.stock_table('Current Stock', temp_date, specificdate)
    elif args.type == "expired":
        Reports.stock_table('Expired', temp_date, specificdate)
    elif args.type == "purchases":
        Reports.stock_table('Purchases', temp_date, specificdate)
    elif args.type == "sales":
        Reports.stock_table('Sales', temp_date, specificdate)
    elif args.type == 'products':
        Reports.stock_table('Products',temp_date, specificdate)
    elif args.type == 'revenue':
        console.print(f"{datename} revenue: {Reports.stock_reports('revenue',temp_date, specificdate)}")
    elif args.type == 'expenses':
        console.print(f"{datename} expenses: {Reports.stock_reports('expenses',temp_date, specificdate)}") 
    elif args.type == 'profit':
        console.print(f"{datename} profit: {Reports.stock_reports('profit',temp_date, specificdate)}") 
    else:
        console.print('Please spcify a type of report.', style='red bold')