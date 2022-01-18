# Parallelizing Web Scraping to Extract Books Data from Amazon(dot)com
 This project aims to parallelize a web scraper programmed to extract book listing from the popular e-commerce website, Amazon(dot)com, performing an automated genre search and webpage navigation designed in Python programming language.
 
 Although the program is scraping the book data (prices, ratings, and webpage links) from one website, it deals with multiple URLs when navigating through the website fetching items.
 
 This project uses Selenium and BeautifulSoup4 for scraping data and Concurrent.futures for parallelizing the program to utilize mor workers (cores on the system).
