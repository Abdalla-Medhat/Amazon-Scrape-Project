#Import Libraries.
from bs4 import BeautifulSoup
import csv 
from selenium import webdriver
from datetime import datetime
import time

#Count time(Starting point).
start =datetime.now()

#Count pages.
pag = 1
#Create lists.
title_list = []
price_list = []

#The main loop.
while True:
    
    #Create options for Webdriver.
    options = webdriver.ChromeOptions()
    #Use headless mode.
    options.add_argument("--headless=new")
    
    #Block Images and JavaScript.
    prefs = {"profile.managed_default_content_settings.images": 2,"profile.managed_default_content_settings.javascript": 2}
    options.add_experimental_option("prefs", prefs)    

    #Pass Options to Webdriver.
    driver = webdriver.Chrome(options=options)
    #Make a request.
    driver.get(f"https://www.amazon.eg/s?i=home&bbn=18021933031&rh=n%3A21863947031&fs=true&page={pag}&language=en&qid=1711754513&ref=sr_pg_1")
    time.sleep(1)
    #Get source code.
    src = driver.page_source
    #Parse source code.
    soup = BeautifulSoup(src, "lxml")

    #Find all products.    
    product = soup.find_all("div", {"class": "puis-card-container"})

    #Loop over products to get all data and store it in lists.
    for x in product:
        try:
            title = x.find("span", {"class": "a-size-medium a-color-base a-text-normal"}).text
            title_list.append(title)
        except:
            title_list.append("not found")
            
        try:
            price = x.find("span", {"class": "a-price-whole"}).text
            price_list.append(price)
            
        except :
            price_list.append("not found")
            continue

    #Close Webdriver.    
    driver.quit()

    #Count pages.
    pag += 1

    #Check if the last page is reached.
    if pag > 35:
        print("✔Project is done✔")
        break

#Create CSV file.
with open("Amazontest.csv", "w", newline='', encoding='utf-8') as file:
    wr = csv.writer(file)
    wr.writerow(["Title", "prices"])
    wr.writerows(zip(title_list, price_list))
    #Another method you can use instead of the line before:👇
    #for x in range(len(title_list)):
        #wr.writerow([title_list[x], size_list[x]])

#Create TXT file.
file =  open("Amazontest.txt", "w", newline='', encoding='utf-8')
file.write("Title" + "\t" + "prices" + "\n")
for x in range(len(title_list)):
    file.write(f"Title: {title_list[x]}\nSize: {price_list[x]}\n" +'*'*70 +'\n')
file.close()

#Count time(Ending point).
end = datetime.now()
print("excution taken: ", end - start)
#It's done.