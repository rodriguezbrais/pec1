import requests
from bs4 import BeautifulSoup
import random
from random import randint
from time import sleep

mainLink = "https://www.tripadvisor.es"
ourense = "/Hotels-g644337-Ourense_Province_of_Ourense_Galicia-Hotels.html"
user_agent_list = [
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
cityHotelsLink = mainLink + ourense
nHotels = 1
nReviews = 50

user_agent = random.choice(user_agent_list)
headers = {'User-Agent': user_agent}
print(user_agent)
response = requests.get(cityHotelsLink, headers = headers)

html = BeautifulSoup(response.content, "html.parser")

hotelsHtml = html.find_all("div", {"class": "listItem"})

for hotelHtml in hotelsHtml[:nHotels]:
    hotelRef = hotelHtml.find("a", {"class": "property_title"})
    hotelName = hotelRef.get_text()
    hotelLink = hotelRef.get("href")
    hotelPoints = hotelHtml.find("a", {"class": "ui_bubble_rating"}).get("alt")
    hotelReviewCount = hotelHtml.find("a", {"class": "review_count"}).get_text()
    print(hotelName)
    print(hotelLink)
    print(hotelPoints)
    print(hotelReviewCount)

    link = mainLink + hotelLink
    paginatedLink = link[:(link.find('Reviews') + 7)] + '-or{}' + link[(link.find('Reviews') + 7):]

    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    print(user_agent)

    for i in range(0, nReviews, 5):
        responseReviews = requests.get(paginatedLink.format(i), headers=headers)
        sleep(randint(1, 5))
        reviewsHtml = BeautifulSoup(responseReviews.content, "html.parser")
        if reviewsHtml:
            reviewsHtml = reviewsHtml.find_all("div", {"data-test-target": "HR_CC_CARD"})
            for review in reviewsHtml:
                reviewRef = review.find("q")
                reviewText = reviewRef.get_text()
                print(reviewText)
