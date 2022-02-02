import selenium
from selenium import webdriver
import time
import requests
import os
from PIL import Image
import io
import hashlib
import xlwt
# All in same directory
DRIVER_PATH = 'chromedriver.exe'

def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:int=1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)        
    
    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    error_clicks = 0
    while (image_count < max_links_to_fetch) & (error_clicks < 20): # error clicks to stop when there are no more results to show by Google Images. You can tune the number
        scroll_to_end(wd)

        print('Starting search for Images')

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)
        
        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            print("Total Errors till now:", error_clicks)
            try:
                print('Trying to Click the Image')
                img.click()
                time.sleep(sleep_between_interactions)
                print('Image Click Successful!')
            except Exception:
                error_clicks = error_clicks + 1
                print('ERROR: Unable to Click the Image')
                if(results_start < number_results):
                	continue
                else:
                	break
                	
            results_start = results_start + 1

            # extract image urls    
            print('Extracting of Image URLs')
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            print('Current Total Image Count:', image_count)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
            else:
                load_more_button = wd.find_element_by_css_selector(".mye4qd")
                if load_more_button:
                    wd.execute_script("document.querySelector('.mye4qd').click();")
            	        
        results_start = len(thumbnail_results)

    return image_urls

def persist_image(folder_path:str,file_name:str,url:str,count):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        folder_path = os.path.join(folder_path,file_name)
        if os.path.exists(folder_path):
            file_path = os.path.join(folder_path,str(count) + '.jpg')
        else:
            os.mkdir(folder_path)
            file_path = os.path.join(folder_path,str(count) + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=300)
        print(f"SUCCESS - saved {url} - as {file_path}")
        
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

if __name__ == '__main__':
    wd = webdriver.Chrome(executable_path=DRIVER_PATH)

    queries = [
# "František Kupka",
# "Piet Mondrian", 
# "Jean Arp",
# "Sophie Taeuber-Arp",
# "Sonia Robert Delaunay",
# "Naum Gabo",
# "László Moholy-Nagy",
# "Amédée Ozenfant",
# "Antoine Pevsner",
# "Luigi Russolo",
# "Jean Hélion",
# "Otto Freundlich",
# "Georges Vantongerloo",
# "Theo van Doesburg",
# "César Baldaccini",
# "César Domela",
# "Jean Gorin",
# "Josef Albers",
# "Harry Holtzman",
# "Charmion Von Wiegand",
# "Leon Polk Smith",
# "Auguste Herbin",
# "Étienne Béothy",
# "Alberto Magnelli",
# "Félix Del Marle",
# "Ellsworth Kelly",
# "François Morellet",
# "Henry Lhotellier",
# "Yves Klein",
# "Piero Manzoni",
# "Lucio Fontana",
# "Victor Vasarely",
# "Ad Reinhardt",
# "Franz Kline",
# "Mark Rothko",
# "Vassily Kandinsky",
# "Jean Fautrier",
# "Jean Dubuffet",
# "Emilio Vedova",
# "Pierre Soulages",
# "Maria Helena Vieira da Silva",
# "Hans Hartung",
# "Jean Degottex",
# "Georges Mathieu",
# "Fernand Léger",
# "Berto Lardera",
# "Aurélie Nemours",
# "Richard Paul Lohse",
# "Olle Bærtling",
# "Max Bill"
# "Alfred Manessier",
# "Jean Bazaine",
# "Charles Lapicque",
# "Gustave Singier",
# "Léon Gischia",
# "Pierre Tal Coat",
# "Roger Bissière",
# "Kenneth Noland",
# "Morris Louis",
# "Sam Francis",
"Anthony Caro",
"Joan Mitchell"]  #change your set of queries here

    for query in queries:
        wd.get('https://google.com')
        # search_box = wd.find_element_by_css_selector('input.gLFyf')
        # search_box.send_keys(query)
        links = fetch_image_urls(query,500,wd) # 200 denotes no. of images you want to download
        images_path = 'dataset/'
        book = xlwt.Workbook(encoding="utf-8")
        sheet1 = book.add_sheet("Sheet 1")
        idx = 0
        for i in links:            
            sheet1.write(idx,0,str(i))
            idx += 1
        book.save(str(query + ".xls"))
        count = 1
        for i in links:
            persist_image(images_path,query,i,count)
            count += 1
    wd.quit()
