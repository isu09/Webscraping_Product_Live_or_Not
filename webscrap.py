
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options





csv_file = r"C:\Users\Arun\Desktop\Python\kohls_items.csv"  # Update this with your actual CSV filename
df = pd.read_csv(csv_file)
print(df)



def check_item_status(item_id):
    # Set up Chrome options to run headless (no browser window)





    url = f"https://www.walmart.com/search/?query={item_id}"
    #url= f"https://www.kohls.com/search.jsp?submit-search=web-regular&search={item_id}"
    #https: // www.kohls.com / product / prd - 4229045 / stupell - home - decor - take - chances - inspirational - canvas - wall - art.jsp?skuId = 76207265 & search = 4229045 & submit - search = web - regular
    print(url)


    response = requests.get(url)
    print(response.text)




    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")





        if "There were no search results for abcdef" in response.text:
            return "Not Live"
        return "Live"
    elif response.status_code in [301, 302]:  # Redirection detected
        return "Live"
    else:

        return "Unknown Error"



# Iterate through the list of items
results = []
for index, row in df.iterrows():
    item_id = row["Kohls_Internal_ID"]
    status = check_item_status(item_id)


    results.append({"Item ID": item_id, "Status": status})
    time.sleep(2)  # To avoid getting blocked

# Save results to a new CSV file
results_df = pd.DataFrame(results)
results_df.to_csv(r"C:\Users\Arun\Desktop\Python\kohls_item_status.csv", index=False)

print("Check complete! Results saved in 'walmart_item_status.csv'.")
