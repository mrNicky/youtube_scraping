#Youtube scraping, data visualisation

#Import lib
import requests
from bs4 import BeautifulSoup
import pandas as pd

#Import lib we need for bokeh
from math import pi
from bokeh.io import output_file, show
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
import bokeh.io


r = requests.get('https://www.youtube.com/feed/trending') #Use of requests librairie
r.text #To text format

soup = BeautifulSoup(r.text, 'html.parser') #Parse with BeautifulSoup
print(soup.prettify()) #Show more structured html

#Find all class we seek inside <a
results = soup.find_all('a',
attrs={'class':"yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link"})
print(results)

#Tri de nos titres
titre = [i.get('title') for i in results]

#Find and save in a list all youtubers
#Note: we use list because we need that for data visualisation
yt = soup.find_all('div', class_="yt-lockup-byline")
youtuber = [k.text for k in yt]

#We do the same with views convert 567 666 vues to an integer
#Note: we just need the last element of <li>
vue_brut = soup.find_all('ul', class_='yt-lockup-meta-info')
vue = []
for j in vue_brut:
    d = j.find_all('li')[1:]
    nb = str(d[0])[4:-10]
    n = int("".join(nb.split()))
    vue.append(n)


#Create the dataframe we need, we use a dictionnary with list values
d = {'titre': titre, 'vues': vue, 'youtuber': youtuber}
df = pd.DataFrame(d)
df = df.sort_values(by=['vues'], ascending=False)
df = df.head(5)
df = df[['youtuber','vues']]
df



#output_file("pie.html")
df.set_index(['youtuber', 'vues'])
df['percent'] = df['vues'] / sum(df['vues']) * 100
df['angle'] = df['vues']/df['vues'].sum() * 2*pi
df['color'] = Category20c[5]

p = figure(plot_height=350, title="Pie Chart", toolbar_location=None,
           tools="hover", tooltips="@youtuber:  @percent{0.2f} %")

p.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend='youtuber', source=df)

p.axis.axis_label=None
p.axis.visible=False
p.grid.grid_line_color=None
bokeh.io.reset_output()
bokeh.io.output_notebook()
show(p)
