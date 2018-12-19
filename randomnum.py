import random
import csv
list=[]
for i in range(1000):
          r=random.randint(1000,2000)
          if r not in list: 
                list.append(r)
print(list)                
                #with open("C:\myanmar-website-crawlers\data.csv", "a", encoding='utf-8') as WR:
                    #writer = csv.writer(WR)
                    #temp="https://myanmar.mmtimes.com/news/118"+str(r)+".html"
                    #temp=str(temp)
                    #writer.writerow([temp])  # Need t