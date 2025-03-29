# Webscraping_Product_Live_or_Not

Perfect! Here’s the step-by-step plan for a **local Python script** that will automate this for you:

### **1. Requirements**
You will need:
- `requests` (for sending HTTP requests)
- `BeautifulSoup` (for parsing HTML)
- `selenium` (for capturing screenshots, optional)
- `pandas` (for handling lists of SKUs)

You can install them with:
```sh
pip install requests beautifulsoup4 selenium pandas
```

---

### **2. Python Script**
Here’s a simple script to check if an item is live:

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver

# Load list of Kohl's Internal IDs from a CSV file
csv_file = "kohls_items.csv"  # Update this with your actual CSV filename
df = pd.read_csv(csv_file)

# Define the function to check if an item is live
def check_item_status(item_id):
    url = f"https://www.kohls.com/search.jsp?submit-search=web-regular&search={item_id}"
    response = requests.get(url, allow_redirects=False)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        if "Sorry, we can’t find any results" in response.text:
            return "Not Live"
        return "Live"
    elif response.status_code in [301, 302]:  # Redirection detected
        return "Live"
    else:
        return "Unknown Error"

# Optional: Capture a screenshot using Selenium if the item is live
def capture_screenshot(item_id):
    url = f"https://www.kohls.com/search.jsp?submit-search=web-regular&search={item_id}"
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=options)
    
    driver.get(url)
    screenshot_path = f"screenshots/{item_id}.png"
    driver.save_screenshot(screenshot_path)
    driver.quit()
    
    return screenshot_path

# Iterate through the list of items
results = []
for index, row in df.iterrows():
    item_id = row["Kohls_Internal_ID"]
    status = check_item_status(item_id)
    
    screenshot = None
    if status == "Live":
        screenshot = capture_screenshot(item_id)
    
    results.append({"Item ID": item_id, "Status": status, "Screenshot": screenshot})
    time.sleep(2)  # To avoid getting blocked

# Save results to a new CSV file
results_df = pd.DataFrame(results)
results_df.to_csv("kohls_item_status.csv", index=False)

print("Check complete! Results saved in 'kohls_item_status.csv'.")
```

---

### **3. Explanation**
- **Reads a list of Kohls Internal IDs** from a CSV file.
- **Checks the item’s status** by sending a request to the Kohls search URL.
- **Determines if it’s live** based on response behavior (redirection = live, “Sorry” message = not live).
- **(Optional) Captures a screenshot** using Selenium if the item is live.
- **Saves results to a CSV file** for easy tracking.

---

### **4. Running the Script**
1. **Create a CSV file (`kohls_items.csv`)** with a column `Kohls_Internal_ID` like:
   ```
   Kohls_Internal_ID
   76207265
   49318754
   12345678
   ```
2. Run the script:
   ```sh
   python check_kohls_items.py
   ```
3. Check the output in `kohls_item_status.csv`.
