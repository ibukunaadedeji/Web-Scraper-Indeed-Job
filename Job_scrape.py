from urllib.request import urlopen as uRequest
from bs4 import BeautifulSoup as soup
import pandas as pd
import time

my_url="https://ng.indeed.com/jobs?q=solar&l&vjk=9b861d63eaeecede"

#Opening connection and grabbing the page at the URL
uClient = uRequest(my_url)

#Read the downloaded page and storing it in a variable
page_html = uClient.read()

#close the connection so we don't leave it opened
uClient.close()

#page parser
page_soup = soup(page_html, "html.parser")


def extract_job_title_from_result(soup):
  jobs = []
    for div in soup.find_all(name=”div”, attrs={“class”:”row”}):
      for a in div.find_all(name=”a”, attrs={“data-tn-element”:”jobTitle”}):
      jobs.append(a[“title”])
  return(jobs)
extract_job_title_from_result(soup)



def extract_company_from_result(soup):
  companies = []
  for div in soup.find_all(name=”div”, attrs={“class”:”row”}):
    company = div.find_all(name=”span”, attrs={“class”:”company”})
    if len(company) > 0:
      for b in company:
        companies.append(b.text.strip())
    else:
      sec_try = div.find_all(name=”span”, attrs={“class”:”result-link-source”})
        for span in sec_try:
          companies.append(span.text.strip())
 return(companies)
extract_company_from_result(soup)



def extract_location_from_result(soup):
  locations = []
  spans = soup.findAll(‘span’, attrs={‘class’: ‘location’})
  for span in spans:
    locations.append(span.text)
  return(locations)
extract_location_from_result(soup)



def extract_salary_from_result(soup):
  salaries = []
  for div in soup.find_all(name=”div”, attrs={“class”:”row”}):
    try:
      salaries.append(div.find(‘nobr’).text)
    except:
      try:
        div_two = div.find(name=”div”, attrs={“class”:”sjcl”})
        div_three = div_two.find(“div”)
        salaries.append(div_three.text.strip())
      except:
        salaries.append(“Nothing_found”)
  return(salaries)
extract_salary_from_result(soup)

max_results_per_city = 100
city_set = [‘Lagos','Abuja', 'Ibadan']
columns = [“city”, “job_title”, ”company_name”, ”location”, , ”salary”]

sample_df = pd.DataFrame(columns=columns)

  # scraping code:
  for city in city_set:
      for start in range(0, max_results_per_city, 10):
          page = requests.get(‘http: // www.indeed.com / jobs?q = data + scientist + % 2420 % 2
          C000 & l = ' + str(city) + ‘&start=’ + str(start))
          time.sleep(1)  # ensuring at least 1 second between page grabs
          soup = BeautifulSoup(page.text, “lxml”, from_encoding =”utf - 8
          ")
          for div in soup.find_all(name=”div”, attrs={“class ”: ”row”}):
      # specifying row num for index of job posting in dataframe
      num = (len(sample_df) + 1)
      # creating an empty list to hold the data for each posting
      job_post = []
      # append city name
      job_post.append(city)
      # grabbing job title
 for a in div.find_all(name=”a”, attrs={“data-tn-element”:”
          jobTitle”}):
      job_post.append(a[“title”])
      # grabbing company name
      company = div.find_all(name=”span”, attrs = {“class ”:”company”})
      if len(company) > 0:
          for
      b in company:
      job_post.append(b.text.strip())
      else:
      sec_try = div.find_all(name= ”span”, attrs = {“class ”:”result - link - source”})
for span in sec_try:
          job_post.append(span.text)
      # grabbing location name
      c = div.findAll(‘span’, attrs = {‘class ’: ‘location’})
 for span in c:
          job_post.append(span.text)
      # grabbing summary text
      d = div.findAll(‘span’, attrs = {‘ class ’:‘

          summary’})
 for span in d:
          job_post.append(span.text.strip())
          # grabbing salary
      try:
          job_post.append(div.find(‘nobr’).text)
          except:
          try:
              div_two = div.find(name=”div”, attrs = {“ class ”: ”sjcl”})
              div_three = div_two.find(“div”)
              job_post.append(div_three.text.strip())
          except:
              job_post.append(“Nothing_found”)
              # appending list of job post info to dataframe at index num
              sample_df.loc[num] = job_post

          # saving sample_df as a local csv file — define your own local path to save contents
          sample_df.to_csv(“[filepath].csv”, encoding =’utf - 8')




#item-container holds all infomration about each product in the search results. We store all results in an array called container
#containers = page_soup.findAll("div",{"class":"post_item post_layout_list"})

filename = ""
f = open(filename, "w")

headers = ["city", "job_title", "company_name", "location", "summary", "salary" "\n"]
f.write(headers)

for container in containers:
    title_container = container.findAll("h2",{"class":"woocommerce-loop-product__title"})
    productName =  title_container[0].text

    #shipping_container = container.findAll("li",{"class":"price-ship"})
    #shipping = shipping_container[0].text.strip()

    price_container = container.findAll("span",{"price"})
    price = price_container[0].text.strip()


    #print("Product Name: " + productName)
    #print("Shipping: " + shipping)
    #print("Price: " + price)

    f.write(productName + "," + price.replace(",",".") + "\n")
f.close()