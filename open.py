import selenium
import time
from selenium import webdriver
from selenium import common
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv

#url = "https://www.scrum.org/open-assessments/product-owner-open"
url = "https://www.scrum.org/open-assessments/scrum-open"
driver = webdriver.Firefox()
wait = WebDriverWait(driver,100)

while True:
    try:
        driver.get(url)
        wait.until(EC.presence_of_all_elements_located)
        elem = driver.find_element_by_class_name('btn')
        elem.click()
        elem = driver.find_element_by_class_name('fade_content_btn')
        elem.click()
        elem = driver.find_element_by_class_name('fade_content_btn')
        elem.click()

        def clickthrough():
            try:
                try:
                    elem = driver.find_element_by_css_selector("input[type='radio']")
                except:
                    elem = driver.find_element_by_css_selector("input[type='checkbox']")

                elem.click()
                elem = driver.find_element_by_id('qnext')
                elem.click()
            except:
                try:
                    elem = driver.find_element_by_class_name('jqmClose')
                    elem.click()
                    clickthrough()
                except:
                    return

        # loop through quiz
        while True:
            try:
                time.sleep(1)
                elem = driver.find_element_by_class_name('finish2')
                #print(elem)
                break
            except:
                time.sleep(1)
                clickthrough()

        time.sleep(1)
        try:
            elem = driver.find_element_by_class_name('finish2')
            elem.click()

        except:
            time.sleep(0.5)
            elem = driver.find_element_by_class_name('jqmClose')
            elem.click()
            time.sleep(1)
            elem = driver.find_element_by_class_name('finish2')
            elem.click()

        try:
            time.sleep(0.5)
            elem = driver.find_element_by_class_name('confirmfinish2')
            elem.click()

        except:
            time.sleep(1)
            elem = driver.find_element_by_class_name('jqmClose')
            elem.click()
            time.sleep(1)
            try:
                elem = driver.find_element_by_css_selector("input[type='radio']")
            except:
                elem = driver.find_element_by_css_selector("input[type='checkbox']")
            elem.click()

            elem = driver.find_element_by_class_name('finish2')
            elem.click()
            time.sleep(1)
            elem = driver.find_element_by_class_name('confirmfinish2')
            elem.click()

        # ab hier beautifulsoup


        html = driver.page_source
        soup = BeautifulSoup(html)

        fragen = soup.findAll('div', {'class':'qsholder'})
        feedbacks = soup.findAll('p', {'class':'v3QuizHolder'})
        feedbacks.pop(0)

        Correct = soup.findAll('p', {'class':'chosen'})
        #print(len(Correct))
        i = 0
        for cor in Correct:
            #print(str(i) + str(cor))
            if 'You did not select all available correct options' in str(cor):
                #print('YES')
                Correct.pop(i)

            i = i + 1
        #rint("new" + str(len(Correct)))


        #antworten:
        containers = soup.findAll('div', {'class':'col600'})
        j = 0
        doublicatenr = 0;
        while j < len(containers)-1:
            container = containers[j]

            with open('scrawler.csv') as fd:
                csvReader = csv.reader(fd)
                doublicate = False
                for row in csvReader:
                    if len(row) > 0 and row[0].split('#')[0]==str(fragen[j].contents[0]).replace("\n", ''):
                        #print('dublicate')
                        #print('Row: ' + row[0].split('#')[0])
                        #print('Fragen:' + str(fragen[j].contents[0]).replace("\n", ''))
                        doublicate = True
            if doublicate:
                j = j + 1
                doublicatenr = doublicatenr + 1
                continue

            fragenset = str(fragen[j].contents[0]).replace("\n", '')


            antworten = container.findChildren('div',{'class':'saans editor'} )
            i = 0
            printantworten = []
            for antwort in antworten:
                printantworten.append(antwort.contents[0])
                i = i + 1
                #print(str(i) + ": " + antwort.text)

            #print(container.findChildren('div',{'class':'v3QuizHolder'}) )

            if len(container.findChildren('div',{'class':'v3QuizHolder'})) == 0:
                feedbackset = str(feedbacks[j].contents[0]).replace("\n", '').replace(";", ',')
                #feedbacks.insert(j, "")

            antwortset = str(printantworten)
            correctset = str(Correct[j].contents[1]).replace('<strong>','').replace('</strong>','').replace(";", ',')
            #print(len(correctset))
            row = [fragenset, feedbackset, antwortset, correctset]
            #print (str(fragenset))
           # print(Correct[j].contents)

            with open('scrawler.csv', 'a') as fd:
                writer = csv.writer(fd, delimiter='#', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                #writer = csv.writer(fd)
                writer.writerow(row)


            j = j + 1
        print('New Questions: ' + str(15 - doublicatenr))
    except:
        pass

   
