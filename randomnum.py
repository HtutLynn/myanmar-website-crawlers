import random
import csv
list=[]
count = 0
for i in range(5000):
      r=random.randint(0,5000)
      if r not in list: 
            list.append(r)
      count += 1
      print(count)
print(list)                
                #with open("C:\myanmar-website-crawlers\data.csv", "a", encoding='utf-8') as WR:
                    #writer = csv.writer(WR)
                    #temp="https://myanmar.mmtimes.com/news/118"+str(r)+".html"
                    #temp=str(temp)
                    #writer.writerow([temp])  # Need t