import unittest
import requests
import json

class TestProtei(unittest.TestCase):

		#получение координат по адресу
		def test_get_coordinate(self):
			print ('\n====================== START address -> coordinate START ======================\n')
			
			#считывание эталонной базы адреса и соответсвующих ему координат //набор тестов
			with open("jsonfile_for_search.json", "r", encoding="utf-8") as data_file:
				data = json.load(data_file)
				
				#проверили что мы считали из файла
				#print ('\n- - - - - - - - - - \n', data, '\n- - - - - - - - - - \n') 

				test_num = data["tests"]

				#смотрим потестово
				for test_num in data["tests"]:

					#выводим номер теста
					print ('----------------* Test #: ', test_num["test_id"], '*----------------')

					#выводим адрес, который будем отправлять на openstreetmap
					print ('[*] Address:', test_num["address"])

					#выводим ожидаемые координаты 
					Lat_expect = test_num["expected coordinate"]["latitude"]
					Lon_expect = test_num["expected coordinate"]["longitude"]

					print ('\n[*] Expected Coordinate \n\t Lat:', Lat_expect, '\n\t Lon:', Lon_expect)

					#формируем данные для запроса
					payload = {'q': test_num["address"], 'format': 'json'} 

					#отправляем запрос
					r = requests.get('https://nominatim.openstreetmap.org/search', payload)

					#выводим запрос, ктр получился
					#print ('\n URL: ', r.url) 

					status = r.status_code #смотрим код состояния ответа

					if status == 200:
						print ('\n[*] OK') #если всё успешно
					else:
						print ('\n[!!!]', r.raise_for_status()) #если запрос неудачный (ошибка 4xx or 5xx), то вызовется исключение
					
					a = r.text

					#print (type(a)) #тип а str
					#print (a) #вывод содержимого ответа
					#print (r.content)

					if a == '[]' :  #если ничего не вернуло. дословно на странице :"Ничего не найдено"

						Lat_reciev = ''
						Lon_reciev = ''
						print ("\n[!!!] Nothing Found - Please, check your request!")
						#continue
					else:	

						'''убираем первый и последний символ '[' и ']', мешающие нормально работать с данными 
						(а именно, чтоб не было проблем парсить данные как json) // возможно это костыль??''' 
						a = a[:-1]
						a = a.replace('[', '',1)
						
						a = json.loads(a) #переводим данные в json // заполняем словарь (dict)

						#print (type(a)) #тип a dict

						Lat_reciev = a['lat']
						Lon_reciev = a['lon']

					print ('\n[*] Recieved Coordinate \n\t Lat:',  Lat_reciev, '\n\t Lon:', Lon_reciev)

					Data_expect = Lat_expect + ' ' + Lon_expect
					#print (Data_expect)

					Data_reciev = Lat_reciev + ' ' + Lon_reciev
					#print (Data_reciev)

					#сравниваем полученный результат с ожидаемым
					try:
						result = self.assertEqual(Data_expect, Data_reciev)

					#обработака исключения в случае несоответствия полученного ожидаемому
					except AssertionError:
						print('\n[*] Test', test_num["test_id"], ' - !FAILED!')

					#если всё ОК и тест прошёл	
					else:
						print('\n[*] Test', test_num["test_id"], ' - !SUCCESS!')
					
					print ('--------------------* END *--------------------\n\n')	
			
			print ('\n======================== END address -> coordinate END ========================\n')
		
		def test_get_addres(self):
		
			print ('\n====================== START coordinate -> address START ======================\n')
			
			#считывание эталонной базы адреса и соответсвующих ему координат //набор тестов
			with open("jsonfile_for_reverse.json", "r", encoding="utf-8") as data_file:
				data = json.load(data_file)
				
				#проверили что мы считали из файла
				#print ('\n- - - - - - - - - - \n', data, '\n- - - - - - - - - - \n') 

				test_num = data["tests"]

				#смотрим потестово
				for test_num in data["tests"]:

					#выводим номер теста
					print ('----------------* Test #: ', test_num["test_id"], '*----------------')

					#координаты, которые будем отправлять на openstreetmap		
					Lat_from_file = test_num["coordinate"]["latitude"]
					Lon_from_file = test_num["coordinate"]["longitude"]

					print ('\n[*] Coordinate \n\t Lat:', Lat_from_file, '\n\t Lon:', Lon_from_file)

					#выводим ожидаемый адрес
					Add_expect = test_num["expected address"]
					print ('\n[*] Expected Address:', Add_expect)

					#формируем данные для запроса
					payload = {'lat': Lat_from_file, 'lon': Lon_from_file, 'format': 'json'} 

					#отправляем запрос
					r = requests.get('https://nominatim.openstreetmap.org/reverse', payload)

					#выводим запрос, ктр получился
					#print ('\n URL: ', r.url) 

					status = r.status_code #смотрим код состояния ответа
					#print (status)

					a = r.text
					#print (type(a)) #тип а str
					#print (a) #вывод содержимого ответа
					#print (r.content)
					#print (type(r.content)) #bytes
					
					a = json.loads(a) #переводим данные в json // заполняем словарь (dict)
					#print (type(a)) #тип a dict
					
					if status == 200:
						print ('\n[*] OK') #


					if "error" in a: #если вернуло error (например lat lon вне диапазона)

						if "message" in a['error']: #eсли в error есть ключ message
							print ('\n[!!!]', a['error']['message'], '- Please, check your request!')
						else: 
							print ('\n[!!!]', a['error'], '- Please, check your request!')
						Add_reciev = ''						
						#continue
					else:
						if 'country' and 'state' and 'town' and 'road' and 'building' in a['address']:
							print (a['address']['town'])
							Add_reciev = a['address']['country'] + ', ' + a['address']['state'] + ', ' + a['address']['town'] + ', ' + a['address']['road'] + ', ' + a['address']['building']
							print(Add_reciev)
						else:
							Add_reciev = ''	#адрес может быть, но если мы здесь, то он не соответствует ожидаемому шаблону		
							

					print ('\n[*] Recieved Address:', Add_reciev)
					
					#сравниваем полученный результат с ожидаемым
					try:
						result = self.assertEqual(Add_expect, Add_reciev)

					#обработака исключения в случае несоответствия полученного ожидаемому
					except AssertionError:
						print('\n[*] Test', test_num["test_id"], ' - !FAILED!')

					#если всё ОК и тест прошёл	
					else:
						print('\n[*] Test', test_num["test_id"], ' - !SUCCESS!')
					
					print ('--------------------* END *--------------------\n\n')				
								
			print ('\n======================== END coordinate -> address END ========================\n')

if __name__ == '__main__':
    unittest.main()