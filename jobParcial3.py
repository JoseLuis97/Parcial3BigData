import requests
from bs4 import BeautifulSoup
import boto3
import datetime as dt

s3 = boto3.client('s3')

def descarga(url, url2):
    #descargar publimetro
    r = requests.get(url, stream=True)
    name_publimetro='publimetro'
    
    archivo=open('/tmp/'+name_publimetro+'.html','w', encoding='utf-8') 
    archivo.write(r.text)
    archivo.close()
    #descargar el tiempo
    t = requests.get(url2, stream=True)
    name_eltiempo='eltiempo'
    
    archivo=open('/tmp/'+name_eltiempo+'.html','w', encoding='utf-8') 
    archivo.write(t.text)
    archivo.close()
    
    #fecha
    today = dt.datetime.today()
    day_actual = today.day
    month_actual = today.month
    year_actual = today.year
    
    #direccion 
    newBucket = 'parcial3bd'
    upload_path_eltiempo = 'pagina/headlines/raw/periodico='+name_eltiempo+'/year='+str(year_actual)+'/month='+str(month_actual)+'/day='+str(day_actual)+'/'+name_eltiempo+'.html'
    upload_path_publimetro = 'pagina/headlines/raw/periodico='+name_publimetro+'/year='+str(year_actual)+'/month='+str(month_actual)+'/day='+str(day_actual)+'/'+name_publimetro+'.html'
    #subir el archivo
    s3.upload_file('/tmp/'+name_eltiempo+'.html', newBucket, upload_path_eltiempo)
    s3.upload_file('/tmp/'+name_publimetro+'.html', newBucket, upload_path_publimetro)
    
descarga('https://www.publimetro.co/', 'https://www.eltiempo.com/')
    
