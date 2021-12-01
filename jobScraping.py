import requests
from bs4 import BeautifulSoup
import datetime as dt
import boto3
from urllib.parse import unquote_plus
s3 = boto3.client('s3')


def scraping():
    #Nombre de las paginas
    name_eltiempo = 'eltiempo'
    name_publimetro = 'publimetro'
    
    #Fecha
    today = dt.datetime.today()
    day_actual = today.day
    month_actual = today.month
    year_actual = today.year
 
    #Path
    download_path_eltiempo = 'pagina/headlines/raw/periodico=' + name_eltiempo + '/year=' + str(year_actual) + '/month=' + str(month_actual) + '/day=' + str(day_actual) + '/' + name_eltiempo + '.html'
    download_path_publimetro = 'pagina/headlines/raw/periodico=' + name_publimetro + '/year=' + str(year_actual) + '/month=' + str(month_actual) + '/day=' + str(day_actual) + '/' + name_publimetro + '.html'

    #Direccion
    key_eltiempo = download_path_eltiempo
    key_publimetro = download_path_publimetro

    #Nombre del bucket
    bucketName = 'parcial3bd'
 
    #Nombre del archivo a descargar
    download_path_eltiempo = '/tmp/{}.'.format(key_eltiempo.split('/')[-1])
    download_path_publimetro = '/tmp/{}.'.format(key_publimetro.split('/')[-1])

    #Descarga del archivo
    s3.download_file(bucketName, key_eltiempo, download_path_eltiempo)
    s3.download_file(bucketName, key_publimetro, download_path_publimetro)

    #scraping el tiempo
    with open(download_path_eltiempo) as file:
        content = file.read()
        soupET = BeautifulSoup(content,'html.parser')

    articleET = soupET.find_all('div', attrs={'class': 'article-details'})
 
    eltiempoCSV='{}; {}; {} \n'.format('categoria','titulo','link')

    for row in articleET:
        try:
            a = str(str(str(str(row.find_all('a', attrs={'class':'category'})).split('<')).split('>')).split(',')[2]).replace('"','').replace("'","")
            b = str(str(str(row.find_all('a', attrs={'class':'title'})).split('<')).split('>')[1]).replace('"','').replace("'","").replace(', /a','')
            c = 'https://www.eltiempo.com'+str(row.find_all('a', attrs={'class':'title'})).split('"')[3]
            eltiempoCSV = eltiempoCSV+'{}; {}; {} \n'.format(a,b,c)
        except:
            pass

    #Archivo resultante del scaping del tiempo
    archivo=open('/tmp/eltiempo.txt','w', encoding='utf-8') 
    archivo.write(''+eltiempoCSV)
    archivo.close()

    
    #scraping de publimetro
    with open(download_path_publimetro) as file:
        content = file.read()
        soupP = BeautifulSoup(content,'html.parser')

    articleP = soupP.find_all('article')

    publimetroCSV='{}; {}; {} \n'.format('categoria','titulo','link')
    for row in articleP:
        try:
            cat = row.find('span')
            if cat == None:
                cat1 = t
            else:
                cat1 = cat.get_text()
                t = cat1
            #print(cat1)
            tit = row.find('h3')
            if tit == None:
                tit = row.find('h2')
            tit1 = tit.get_text()
            #print(tit1)
            link = row.find('a') 
            link = link['href']
            if link[0] == '/':
                link = "https://www.publimetro.co"+str(link)
            #print(link)
            publimetroCSV = publimetroCSV+'{}; {}; {} \n'.format(cat1,tit1,link)    
        except:
            pass
        
    #Archivo resultante del scaping de publimetro
    archivo=open('/tmp/publimetro.txt','w', encoding='utf-8') 
    archivo.write(''+publimetroCSV)
    archivo.close()
    
    bucketName='parcial3bd'
    #Path de subida
    upload_path_eltiempo = 'scraping/headlines/final/periodico='+name_eltiempo+'/year='+str(year_actual)+'/month='+str(month_actual)+'/day='+str(day_actual)+'/'+name_eltiempo+'.csv'
    upload_path_publimetro = 'scraping/headlines/final/periodico='+name_publimetro+'/year='+str(year_actual)+'/month='+str(month_actual)+'/day='+str(day_actual)+'/'+name_publimetro+'.csv'
    #Subida del archivo 
    s3.upload_file('/tmp/eltiempo.txt', bucketName, upload_path_eltiempo)
    s3.upload_file('/tmp/publimetro.txt', bucketName, upload_path_publimetro)


scraping()
    
