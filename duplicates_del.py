import pandas as pd 
import numpy as np
import csv

file = pd.read_csv("C:\myanmar-website-crawlers\mizzima_urls_opinion.csv", usecols=range(0,1), header=None)
file = np.array(file)

file = np.unique(file)
print(file.shape)
file = file.tolist()

with open("C:\myanmar-website-crawlers\mizzima_urls_opinion.csv", "w", encoding='utf-8') as WR:
        writer = csv.writer(WR)
        for item in file:
            writer.writerow([item])  # Need to add [] for item because without it,
            # the writer function will store each charaters and syllables as a column