from fake_useragent import UserAgent
import requests
import json
import time

from bs4 import BeautifulSoup



def send_telegram(text: str):
    token = "5417607726:AAHF3D2EQ36RWFcr-yF9dSI2qUoCRtWaB50"
    url = "https://api.telegram.org/bot"
    channel_id = "-869517573"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })

    if r.status_code != 200:
        raise Exception("post_text error")



def get_first_data(external_url, external_referer):
    ua = UserAgent()
    header = {
        "authority": "module.sletat.ru",
        "method": "GET",
        "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "referer": external_referer
    }
    url = external_url
    htmlContent = requests.get(url, headers=header)
    json_str = json.loads(htmlContent.text)
    time.sleep(1.0)
    return(json_str['GetToursResult']['Data']['requestId'])



def get_calculate(id):
    ua = UserAgent()
    header = {
        "authority": "module.sletat.ru",
        "method": "GET",
        "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",

    }
    url = 'https://module.sletat.ru/slt/Main.svc/GetLoadState?requestId='+ id
    htmlContent = requests.get(url, headers=header)
    json_str = json.loads(htmlContent.text)
    time.sleep(1.0)
    if (json_str['GetLoadStateResult']['Data'][0]['MinPrice']) == 0 or (json_str['GetLoadStateResult']['Data'][0]['MinPrice']) is None :
        print("No Price - Retry")
        return get_calculate(id)
    else:
        return(json_str['GetLoadStateResult']['Data'][0]['MinPrice'])

# Основной класс по курсу валют
class Currency:
	# Ссылка на нужную страницу
	DOLLAR_RUB = 'https://www.google.com/search?sxsrf=ALeKk01NWm6viYijAo3HXYOEQUyDEDtFEw%3A1584716087546&source=hp&ei=N9l0XtDXHs716QTcuaXoAg&q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+&gs_l=psy-ab.3.0.35i39i70i258j0i131l4j0j0i131l4.3044.4178..5294...1.0..0.83.544.7......0....1..gws-wiz.......35i39.5QL6Ev1Kfk4'
	# Заголовки для передачи вместе с URL
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

	current_converted_price = 0
	difference = 5 # Разница после которой будет отправлено сообщение на почту

	def __init__(self):
		# Установка курса валюты при создании объекта
		self.current_converted_price = float(self.get_currency_price().replace(",", "."))

	# Метод для получения курса валюты
	def get_currency_price(self):
		# Парсим всю страницу
		full_page = requests.get(self.DOLLAR_RUB, headers=self.headers)

		# Разбираем через BeautifulSoup
		soup = BeautifulSoup(full_page.content, 'html.parser')

		# Получаем нужное для нас значение и возвращаем его
		convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
		return convert[0].text
    
    
if __name__ == '__main__':
   send_telegram('!!!!!!!!!!!!!!!!!!!!!! Текущие цены 2+1 !!!!!!!!!!!!!!!!!!!!!!' + '\n' + '---------------------- Египет -----------------------')
   tour1 = (str(get_first_data(
       'https://module.sletat.ru/slt/Main.svc/GetTours?requestId=0&pageSize=10&pageNumber=1&countryId=40&cityFromId=832&cities=1592&meals=115&stars=&s_nightsMin=10&s_nightsMax=10&currencyAlias=RUB&groupBy=&includeDescriptions=1&includeOilTaxesAndVisa=1&minHotelRating=&s_showcase=false&templateName=&filterToursForType=0&excludeToursForType=0&filterToursForTransportType=0&filter=1&f_to_id=380&s_hotelIsNotInStop=true&s_hasTickets=true&s_ticketsIncluded=true&updateResult=1&hotels=40581&s_adults=2&s_kids=1&s_kids_ages=5&s_departFrom=15%2F04%2F2023&s_departTo=15%2F04%2F2023&calcFullPrice=1&showHotelFacilities=1&requestSource=8',
       'https://sletat.ru/tour/380-1497125986-1861190411/')))
   send_telegram('Sentido Mamlouk Palace Resort Egypt ' + (str(get_calculate(tour1))))


   tour2 = (str(get_first_data(
       'https://module.sletat.ru/slt/Main.svc/GetTours?requestId=0&pageSize=10&pageNumber=1&countryId=40&cityFromId=832&cities=1592&meals=115&stars=&s_nightsMin=10&s_nightsMax=10&currencyAlias=RUB&groupBy=&includeDescriptions=1&includeOilTaxesAndVisa=1&minHotelRating=&s_showcase=false&templateName=&filterToursForType=0&excludeToursForType=0&filterToursForTransportType=0&filter=1&f_to_id=380&s_hotelIsNotInStop=true&s_hasTickets=true&s_ticketsIncluded=true&updateResult=1&hotels=36454&s_adults=2&s_kids=1&s_kids_ages=5&s_departFrom=15%2F04%2F2023&s_departTo=15%2F04%2F2023&calcFullPrice=1&showHotelFacilities=1&requestSource=8',
       'https://sletat.ru/tour/380-1497246628-1861200441/')))
   send_telegram('Albatros White Beach Egypt ' + (str(get_calculate(tour2))))

   send_telegram('---------------------- Эмираты -----------------------')
   tour3 = (str(get_first_data(
       'https://module.sletat.ru/slt/Main.svc/GetTours?requestId=0&pageSize=10&pageNumber=1&countryId=90&cityFromId=832&cities=1194&meals=115&stars=&s_nightsMin=10&s_nightsMax=10&currencyAlias=RUB&groupBy=&includeDescriptions=1&includeOilTaxesAndVisa=1&minHotelRating=&s_showcase=false&templateName=&filterToursForType=0&excludeToursForType=0&filterToursForTransportType=0&filter=1&f_to_id=380&s_hotelIsNotInStop=true&s_hasTickets=true&s_ticketsIncluded=true&updateResult=1&hotels=82939&s_adults=2&s_kids=1&s_kids_ages=5&s_departFrom=16%2F04%2F2023&s_departTo=16%2F04%2F2023&calcFullPrice=1&showHotelFacilities=1&requestSource=8',
       'https://sletat.ru/tour/380-1860402775-1867235135/')))
   send_telegram('DoubleTree by Hilton Resort & Spa Marjan Island OAE ' + (str(get_calculate(tour3))))

   tour4 = (str(get_first_data(
       'https://module.sletat.ru/slt/Main.svc/GetTours?requestId=0&pageSize=10&pageNumber=1&countryId=90&cityFromId=832&cities=1194&meals=115&stars=&s_nightsMin=10&s_nightsMax=10&currencyAlias=RUB&groupBy=&includeDescriptions=1&includeOilTaxesAndVisa=1&minHotelRating=&s_showcase=false&templateName=&filterToursForType=0&excludeToursForType=0&filterToursForTransportType=0&filter=1&f_to_id=380&s_hotelIsNotInStop=true&s_hasTickets=true&s_ticketsIncluded=true&updateResult=1&hotels=41538&s_adults=2&s_kids=1&s_kids_ages=5&s_departFrom=14%2F04%2F2023&s_departTo=14%2F04%2F2023&calcFullPrice=1&showHotelFacilities=1&requestSource=8',
       'https://sletat.ru/tour/380-1860402811-1867235135/')))
   send_telegram('The Cove Rotana Resort OAE ' + (str(get_calculate(tour4))))
    
   currency = Currency()
   send_telegram('Сейчас курс: 1 доллар =' + currency.get_currency_price()) 
    
    
