##Technical Issues

###Expiry Date -

This was the most complicated part to implment in superpy and has effected many differnet parts of the program. I decided to not just track the expiry date but to act upon it as well. I.E. The reporting function will take into account whether or not a product has expired and adjust its avaliablity. This blocks expired products from sale, and while the stock will remain on the system until it has been removed, using another fuction that has been added to record a sale with a 0 value. All these movements then also effect the reporting sections allowing reports of how much has been lost due to expiring products and its impact on the days revenue and profit. 

Using the inventory command super py will return a list of all current stock:

                     Stock Report
┏━━━━┳━━━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ ID ┃      NAME ┃ COUNT ┃ COST ┃ EXPIRY DATE ┃ VALUE ┃
┡━━━━╇━━━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│  3 │ cucumbers │     2 │ 1.20 │  2022-12-14 │   2.4 │
│  4 │   tomatos │    45 │  .35 │  2023-01-20 │ 15.75 │
│  6 │   cantalo │     5 │  .50 │  2099-12-12 │   2.5 │
│  7 │   tomatos │    10 │  .60 │  2022-12-01 │   6.0 │
└────┴───────────┴───────┴──────┴─────────────┴───────┘

This list was created at the start of 2023, so as you can see there are some expired products on that list! So use the expired command - 

"super.py report expired"


                Expired Products
┏━━━━┳━━━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ ID ┃      NAME ┃ COUNT ┃ COST ┃ EXPIRY DATE ┃ VALUE ┃
┡━━━━╇━━━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│  3 │ cucumbers │     2 │ 1.20 │  2022-12-14 │   2.4 │
│  7 │   tomatos │    10 │  .60 │  2022-12-01 │   6.0 │
└────┴───────────┴───────┴──────┴─────────────┴───────┘

Using this report you can take the products from sale then process a removal. Such as:

"super.py remove -pn cucumbers -a 1 -ex 2022-12-14"

Which records a sale at 0 value, meaning that the profit for the day will return a negative value, but the revenue report will still return only income.



###Stock Referencing - 

When a new sale is added to superpy it it looks for the stock in the purchase file. That process takes all the purchases and previous sales compares the two lists and removes any sales from the purchase file.  Once this list has been generated it is then checked for expired products which are then blocked from sale. The final list of saleable product is then parsed by and the sale lines added as stock is allocated. If there is unallocated sale left over it then reports the error with the quantity not allocated.

"super.py buy -pn Courgettes -a 4 -p 3.46 -ex 2023-01-15"      
**Purchase added**

"super.py sell -pn Courgettes -a 4 -p 4.67 -ex 2023-01-15"  
**Sale of 4 Courgettess added**

Or

"super.py sell -pn Courgettes -a 6 -p 4.67 -ex 2023-01-15"      
**Sale of 4 Courgettess added**
ERROR: 2 products not in stock, 4 have been allocated.

I have done it this way as you rarely purchase singles of items and it is very normal to sell multiples from different batches. This would be the begining of that implementation.


###Id gen - 

When ever a product is purchased or sold, it will be recorded in the relevant CSV files but I require s unique ID for comparisons later. Here I used a recursion becasue I wanted to practice with them but I could also have used a max on the lists of ID numbers and add one to it. But this way it will also back fill any missing numbers if the file is adjusted manually. (but that would mess up other things such as ordering and dates as it operates on a First in First Out system.)



