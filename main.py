import csv
from rich.console import Console
from install import Install, formatting
console = Console()

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Your code below this line
def main():
    pass

class Product():
    #Add products to brought file
    def buy(product_name, count, buy_price, expiry_date):
        #Write new purchase to brought file
            with open(Install.brought, 'a', newline='') as csvfile:
                file = csv.writer(csvfile)
                id = Product.id_gen(Install.load_data(Install.brought))
                file.writerow([str(id), str(product_name), str(count), str(buy_price), str(Install.load_data(Install.time)), str(expiry_date)])
                csvfile.close()
            console.print ("Purchase added", style="blue")
            return
    #Add sales to sale file
    def sell(product_name, count, sell_price):
            sold_data_dict = (Install.load_data(Install.sold))
            id = str(Product.id_gen(sold_data_dict))  
            stock = Reports.expiration_check()
            notallocated = int(count)
            offswitch = False
            #Find purchase to match
            while offswitch == False:
                if offswitch == True:
                    break
                else:
                    for item in stock:
                        if product_name == item[1]:
                            brought_id = item[0]
                            #Allocate Remaining Items then switch off.
                            if int(item[2]) >= notallocated:
                                with open(Install.sold, 'a', newline='') as csvfile:
                                    file = csv.writer(csvfile)
                                    file.writerow([str(id), str(brought_id), str(notallocated), str(sell_price), str(Install.load_data(Install.time)), str(product_name)])
                                    csvfile.close()
                                    console.print (f'Sale of {notallocated} {product_name}{"s" if notallocated > 1 else ""} added', style="blue")
                                    notallocated = 0
                                    offswitch = True
                            #Partially Allocate Items, then attempt to allocte rest.
                            elif int(item[2]) < notallocated:
                                with open(Install.sold, 'a', newline='') as csvfile:
                                    file = csv.writer(csvfile)
                                    file.writerow([str(id), str(brought_id), str(item[2]), str(sell_price), str(Install.load_data(Install.time)), str(product_name)])
                                    csvfile.close()
                                    console.print (f"Sale of {item[2]} {product_name}{'s' if int(item[2]) > 1 else ''} added", style="blue")
                                    notallocated -= int(item[2])
                    #If item has been checked against all stock switch off and report not in stock.
                    offswitch = True
            if notallocated > 0:
                x = int(count) - notallocated
                console.print (f"ERROR: {notallocated} products not in stock, {x} {'have' if x > 1 else 'has'} been allocated.", style='red bold')
            return
    #Remove Expired product from stock
    def remove(product_name, count, expiry_date):
            sold_data_dict = (Install.load_data(Install.sold))
            id = str(Product.id_gen(sold_data_dict))  
            stock = Reports.expiration_check(True)
            print (stock)
            notallocated = int(count)
            offswitch = False
            #Find purchase to match
            while offswitch == False:
                if offswitch == True:
                    break
                else:
                    for item in stock:
                        if (product_name == item[1]):
                            if (formatting.str2date(expiry_date) == item[5]):
                                brought_id = item[0]
                                #Allocate Remaining items then switch off.
                                if int(item[2]) >= notallocated:
                                    with open(Install.sold, 'a', newline='') as csvfile:
                                        file = csv.writer(csvfile)
                                        file.writerow([str(id), str(brought_id), str(notallocated), str(0-float(item[3])), str(Install.load_data(Install.time)), str(product_name)])
                                        csvfile.close()
                                        console.print (f'Removal of {notallocated} {product_name}{"s" if notallocated > 1 else ""} added', style="blue")
                                        notallocated = 0
                                        offswitch = True
                                #Partially Allocate Items, then attempt to allocte rest.
                                elif int(item[2]) < notallocated:
                                    with open(Install.sold, 'a', newline='') as csvfile:
                                        file = csv.writer(csvfile)
                                        file.writerow([str(id), str(brought_id), str(item[2]), str(0-float(item[3])), str(Install.load_data(Install.time)), str(product_name)])
                                        csvfile.close()
                                        console.print (f"Removal of {item[2]} {product_name}{'s' if int(item[2]) > 1 else ''} added", style="blue")
                                        notallocated -= int(item[2])
                    #If item has been checked against all stock switch off and report not in stock.
                    offswitch = True
            if notallocated > 0:
                x = int(count) - notallocated
                console.print (f"ERROR: {notallocated} products not in stock, {x} {'have' if x > 1 else 'has'} been removed.", style='red bold')
            return

        
    #Get a list of unique product names
    def product_list(products):
        uniqueproducts = [product[1] for product in products]
        list = []
        for row in uniqueproducts:
            if row not in  list:
                list.append(row)               
        return list
    #Generate ID (I just wanted to include a recursion otherwise I could change this to max(ids)+1 which is probabaly a lot faster)
    def id_gen(stock_movements, newid=1):
            newid = int(newid)
            ids = []
            for product in stock_movements:
                id = product.get('id')
                ids.append(int(id))
            if newid not in ids:
                return newid
            else:
                return Product.id_gen(stock_movements, (newid+1))

class Reports():
    #Remove already sold items from stock list
    def current_stock(purchases=Install.load_data(Install.brought, True), sales=Install.load_data(Install.sold, True)):
        current_stock = []
        #Take a list
        for product in purchases: 
            id1 = product[0]
            stockCounter = int(product[2])
            #For each product check if it has been sold, if it has update quantity or ignore line if none left
            for sale in sales:
                if id1 == sale[1]:
                    stockCounter -= int(sale[2])
                    if stockCounter == 0:
                        break
            else:
                product[2] = str(stockCounter)
                current_stock.append(product)
        return current_stock
    #Check and remove expired products
    def expiration_check(Report=False, List=current_stock(), sysdate=Install.load_data(Install.time), specificdate=False):
        Reportlist = []
        #Take two lists
        for purchase in List:
            #Create list of matching dates
            if specificdate == True:
                if formatting.str2date(purchase[5]) == sysdate:
                    Reportlist.append(purchase) 
            #Or create list of still valid dates
            else:
                if formatting.str2date(purchase[5]) <= sysdate:
                    Reportlist.append(purchase) 
                    List.remove(purchase)
        if Report == True:
            return Reportlist 
        else: 
            return List
    #Correct list for previous dates
    def Remove_dates(products, date, specificdate=False):
        list = []
        #Return a list of products expired on a date
        if specificdate == True:
            for row in products:
                if formatting.str2date(row[4]) == date:
                    list.append(row)
        #Otherwise return list of products that have expired
        else:
            for row in products:
                if formatting.str2date(row[4]) <= date:
                    list.append(row)
        return list
    #Stock reporting tables
    def stock_table(type, reportdate, specificdate=False):
        #Information for formatting tables
        Headers = ['ID', 'NAME', 'COUNT', 'COST', 'EXPIRY DATE', 'VALUE']
        if type == 'Purchases':
            Name = 'Purchases'
            products = Reports.Remove_dates(Install.load_data(Install.brought, True), reportdate, specificdate)
        if type == 'Current Stock':
            Name = 'Stock Report'
            products = Reports.current_stock(Reports.Remove_dates(Install.load_data(Install.brought, True), reportdate), Reports.Remove_dates(Install.load_data(Install.sold, True), reportdate))
        if type == 'Sales':
            Name = 'Sales Report'
            Headers = ['ID', 'PURCHASE ID', 'NAME', 'COUNT', 'COST', 'EXPIRY DATE', 'VALUE']
            products = Reports.Remove_dates(Install.load_data(Install.sold, True), reportdate, specificdate)
        if type == 'Expired':
            Name = 'Expired Products'
            products = Reports.expiration_check(True, Reports.current_stock(Reports.Remove_dates(Install.load_data(Install.brought, True), reportdate), Reports.Remove_dates(Install.load_data(Install.sold, True), reportdate)), reportdate, specificdate)
        if type == 'Products':
            Name = 'Products'
            products = Product.product_list(Reports.expiration_check())
            Headers = ['NAME']
        formatting.table_gen(Name, Headers, products)
    #Non Table reports
    def stock_reports(type, reportdate, specificdate=False):
        if type == 'expenses':
            Outgoing = Reports.Remove_dates(Install.load_data(Install.brought, True), reportdate, specificdate)                
            subtotal_outgoings = 0
            for row in Outgoing:
                subtotal_outgoings += int(row[2]) * float(row[3])
            return subtotal_outgoings                    
        if type == 'revenue':            
            Income = Reports.Remove_dates(Install.load_data(Install.sold, True), reportdate, specificdate)
            subtotal_incoming = 0
            for row in Income:
                subtotal_incoming += int(row[2]) * float(row[3])
            return subtotal_incoming
        if type == 'profit':
            purchase_data = Install.load_data(Install.brought, True)
            sales = Reports.Remove_dates(Install.load_data(Install.sold, True), reportdate, specificdate)
            profit = 0
            for row in sales:
                purchase_id = row[1]
                for product in purchase_data:
                    if purchase_id == product[0]:
                        profit += ((int(row[2])*float(row[3])) - (int(row[2])*float(product[3])))
            profit_2SF = round(profit,2)
            return profit_2SF


if __name__ == "__main__":
    main()