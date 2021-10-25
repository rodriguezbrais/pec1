import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
from random import randint
from time import sleep, time
import traceback
import logging
import sys

nHotels         = 30
nReviews        = 1000
nReviewsPerPage = 5

main_link = "https://www.tripadvisor.es"
ourense   = "/Hotels-g644337-Ourense_Province_of_Ourense_Galicia-Hotels.html"

opiniones_string = ' opiniones'

enero_string      = 'enero de '
febrero_string    = 'febrero de '
marzo_string      = 'marzo de '
abril_string      = 'abril de '
mayo_string       = 'mayo de '
junio_string      = 'junio de '
julio_string      = 'julio de '
agosto_string     = 'agosto de '
septiembre_string = 'septiembre de '
octubre_string    = 'octubre de '
noviembre_string  = 'noviembre de '
diciembre_string  = 'diciembre de '

user_agent_list = [
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

hotel_list  = []
review_list = []

hotel_list_columns  = ["id", "name", "review_count"]
review_list_columns = ["hotel_id", "date", "review", "points"]

city_hotels_link = main_link + ourense

logging.basicConfig(filename='hotel_scraping.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def get_points_from_class(review_element):
    review_class = review_element['class']
    if 'bubble_00' in review_class:
        return 0
    elif 'bubble_05' in review_class:
        return 0.5
    elif 'bubble_10' in review_class:
        return 1
    elif 'bubble_15' in review_class:
        return 1.5
    elif 'bubble_20' in review_class:
        return 2
    elif 'bubble_25' in review_class:
        return 2.5
    elif 'bubble_30' in review_class:
        return 3
    elif 'bubble_35' in review_class:
        return 3.5
    elif 'bubble_40' in review_class:
        return 4
    elif 'bubble_45' in review_class:
        return 4.5
    elif 'bubble_50' in review_class:
        return 5
    else:
        return None

def format_date(date):
    if date is None:
        return None

    date = date.get_text()
    date = date.replace('Fecha de la estancia: ', '')
    if enero_string in date:
        date = date.replace(enero_string, '01-')
    elif febrero_string in date:
        date = date.replace(febrero_string, '02-')
    elif marzo_string in date:
        date = date.replace(marzo_string, '03-')
    elif abril_string in date:
        date = date.replace(abril_string, '04-')
    elif mayo_string in date:
        date = date.replace(mayo_string, '05-')
    elif junio_string in date:
        date = date.replace(junio_string, '06-')
    elif julio_string in date:
        date = date.replace(julio_string, '07-')
    elif agosto_string in date:
        date = date.replace(agosto_string, '08-')
    elif septiembre_string in date:
        date = date.replace(septiembre_string, '09-')
    elif octubre_string in date:
        date = date.replace(octubre_string, '10-')
    elif noviembre_string in date:
        date = date.replace(noviembre_string, '11-')
    elif diciembre_string in date:
        date = date.replace(diciembre_string, '12-')
    return date

def format_review_count(hotel_review_count):
    hotel_review_count = hotel_review_count.replace('.', '')
    return int(hotel_review_count.replace(opiniones_string, ''))

def extract_hotels():
    try:
        hotel_id = 0
        for hotel_html in hotels_html[:nHotels]:
            hotel_reference = hotel_html.find("a", {"class": "property_title"})
            hotel_name = hotel_reference.get_text()
            hotel_link = hotel_reference.get("href")
            hotel_review_count = hotel_html.find("a", {"class": "review_count"}).get_text()
            hotel_review_count = format_review_count(hotel_review_count)

            print("Recogiendo datos de {}".format(hotel_name))
            hotel_list.append([hotel_id, hotel_name, hotel_review_count])

            link = main_link + hotel_link
            paginated_link = link[:(link.find('Reviews') + 7)] + '-or{}' + link[(link.find('Reviews') + 7):]

            request_headers = set_user_agent()

            # print("Recogiendo {} de las {} totales.".format(nReviews, hotel_review_count))
            for i in range(0, hotel_review_count, nReviewsPerPage):
                response_reviews = requests.get(paginated_link.format(i), headers=request_headers)
                sleep(randint(1, 5))
                reviews_html = BeautifulSoup(response_reviews.content, "html.parser")
                # if reviews_html:
                print("Extraídas {} reviews de {}".format(i + nReviewsPerPage, hotel_review_count))
                reviews_html = reviews_html.find_all("div", {"data-test-target": "HR_CC_CARD"})
                for review in reviews_html:
                    review_reference = review.find("q")
                    review_text = review_reference.get_text()
                    review_date = review.find("span", {"class": "euPKI"})
                    if review_date is not None:
                        review_date_text = format_date(review_date)
                    else:
                        review_date_text = None
                    review_points_element = review.find("span", {"class": "ui_bubble_rating"})
                    review_points_text = get_points_from_class(review_points_element)
                    # print(review_date_text)
                    print(hotel_name)
                    print(review_points_text)
                    print(review_text + "\n")
                    review_list.append([hotel_id, review_date_text, review_text, review_points_text])

            hotel_id += 1
    except Exception:
        print("Se ha producido un problema en la extracción, se han generado los csv con lo extraído hasta el momento. "
              "Revise el archivo de log para más información")
        logging.error("Se ha producido un problema en la extracción, se han generado los csv con lo extraído hasta el "
                      "momento.", exc_info="True")
        generate_csv()
        sys.exit()


def set_user_agent():
    user_agent = random.choice(user_agent_list)
    return {'User-Agent': user_agent}

def generate_csv():
    current_time = str(time())

    df_hotel = pd.DataFrame(hotel_list, columns=hotel_list_columns)
    df_reviews = pd.DataFrame(review_list, columns=review_list_columns)

    df_hotel.to_csv(r'C:\Users\rachi\Desktop\hotel_dataframe_' + current_time + '.csv',
                    index=False, header=True, sep=';', encoding="utf-8")
    df_reviews.to_csv(r'C:\Users\rachi\Desktop\review_dataframe_' + current_time + '.csv',
                      index=False, header=True, sep=';', encoding="utf-8")

def check_reviews_number(hotel_review_count):
    if nReviews == 0:
        return hotel_review_count
    return nReviews


headers = set_user_agent()

response = requests.get(city_hotels_link, headers = headers)
html = BeautifulSoup(response.content, "html.parser")
hotels_html = html.find_all("div", {"class": "listItem"})

extract_hotels()

generate_csv()
