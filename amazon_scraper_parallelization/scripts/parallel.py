from bs4 import BeautifulSoup
from selenium import webdriver
# import csv
import time
import pandas as pd
import concurrent.futures

# search term based url extraction
def fetch_link(product_keyword):
    base = 'https://www.amazon.com/s?k={}'
    product_keyword = product_keyword.replace(' ', '+')

    link = base.format(product_keyword)
    link += '&page={}'

    return link

# extraction fuction
def prod_extraction(product):
    
    tag = product.h2.a
    product_name = tag.text.strip()

    product_link = 'https://www.amazon.com' + tag.get('href')
    
    try:  
        price = product.find('span', 'a-offscreen').text
    except AttributeError:
        return

    try:
        rating = product.i.text
    except AttributeError:
        rating = ''

    result = (product_name, price, rating, product_link)
    return result

# main function
def main_func(product_keyword):
    # setup driver
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(executable_path="/Users/abhijotbedi/Desktop/hpsc_project/chromedriver", options=options)

    product_listing = []
    product_listings = []
    # results = 0

    # fetching link for a specific product search
    url = fetch_link(product_keyword)
    
    for page_num in range(1, 8):
        # driver is getting the link
        driver.get(url.format(page_num))
        
        # begin extraction for every product
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        # print(len(results))
        # time.sleep(5)
        for product in results:
            product_listing = prod_extraction(product)

            
            product_listings.append(product_listing)
    
    # print(len(product_listings))
    # after extraction closing the driver
    driver.close()

    
    df = pd.DataFrame(product_listings)
    df.to_csv(product_keyword + '.csv', header= ['Book Name', 'Price', 'Rating', 'Link'], index=False)
    
    # with open(product_keyword + '.csv', 'w', newline='', encoding='utf-8') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(['Book Name', 'Price', 'Rating', 'Link'])
    #     writer.writerows(product_listings)

if __name__ == '__main__':
    start_time = time.time()   
    keyword_list = ['spiritual books', 'computer books', 'lifestyle books', 'mindset books', 
            'fiction books', 'horror books', 'comic books', 'mystery books',
            'thriller books', 'romance books', 'western books', 'crime books',
            'cooking books', 'children books', 'drama books', 'history books',
            'fairytale books', 'graphic novel books', 'anthology books', 'travel books',
            'art books', 'architecture books', 'encyclopedia books', 'self help books',
            'politics books', 'satire books', 'chess books', 'math books',
            'business books', 'finance books', 'sports books', 'parenting books'
        ]

    # parallelising the extraction using ProcessPoolExtractor using concurrent.futures 
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
            result = executor.map(
                main_func,
                keyword_list,
            )

    # Recorded computational time
    print("Parallelising scraping of the book data for %d book genres from Amazon(dot)com." % len(keyword_list))
    print("\nComputational time taken by the program = %s" % (time.time() - start_time))