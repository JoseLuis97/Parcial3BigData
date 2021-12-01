import requests
from bs4 import BeautifulSoup
import datetime as dt
import boto3
from urllib.parse import unquote_plus
s3 = boto3.client('s3')


def news():
    #Nombre de las paginas
    name_eltiempo = 'eltiempo'
    name_publimetro = 'publimetro'
    
    #Fecha
    today = dt.datetime.today()
    day_actual = today.day
    month_actual = today.month
    year_actual = today.year
 
    #Path
    download_path_eltiempo = 'scraping/headlines/final/periodico=' + name_eltiempo + '/year=' + str(year_actual) + '/month=' + str(month_actual) + '/day=' + str(day_actual) + '/' + name_eltiempo + '.csv'
    download_path_publimetro = 'scraping/headlines/final/periodico=' + name_publimetro + '/year=' + str(year_actual) + '/month=' + str(month_actual) + '/day=' + str(day_actual) + '/' + name_publimetro + '.csv'
    
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
    
    
    with open(download_path_eltiempo) as file:
        content = file.read()
        
    #Archivo resultante del scaping del tiempo
    archivo=open('/tmp/eltiempo.txt','w', encoding='utf-8') 
    archivo.write(''+content)
    archivo.close()
    
    with open(download_path_publimetro) as file:
        content = file.read()
        
    #Archivo resultante del scaping de oublimetro
    archivo=open('/tmp/publimetro.txt','w', encoding='utf-8') 
    archivo.write(''+content)
    archivo.close()
    
    bucketName='parcial3bd'
    #Path de subida
    upload_path_eltiempo = 'news/raw/periodico='+name_eltiempo+'/year='+str(year_actual)+'/month='+str(month_actual)+'/day='+str(day_actual)+'/'+name_eltiempo + '.csv'
    upload_path_publimetro = 'news/raw/periodico='+name_publimetro+'/year='+str(year_actual)+'/month='+str(month_actual)+'/day='+str(day_actual)+'/'+ name_publimetro + '.csv'
    #Subida del archivo 
    s3.upload_file('/tmp/eltiempo.txt', bucketName, upload_path_eltiempo)
    s3.upload_file('/tmp/publimetro.txt', bucketName, upload_path_publimetro)
   
   
news()
    
