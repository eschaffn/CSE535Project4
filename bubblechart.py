from datetime import datetime
import json


file = open('tweets.json', 'r')
tweets = json.load(file)
file.close()

x = open('owid-covid-data.json', 'r')
cases = json.load(x)
x.close()

usa_pro1 = [0, 0, 1, 18, 3, 4, 8, 1, 14, 9, 12, 16, 22, 18, 37, 30, 43, 68]
usa_against1 = [0, 0, 0, 0, 0, 1, 1, 3, 9, 4, 0, 3, 1, 2, 5, 3, 4, 11]
mex_pro1 = [6, 7, 2, 0, 3, 1, 1, 3, 0, 0, 1, 2, 17, 9, 9, 8, 3, 23]
mex_against1 = [1, 2, 1, 0, 0, 0, 2, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 26]
ind_pro1 = [0, 0, 0, 6, 15, 3, 1, 0, 1, 0, 1, 1, 0, 0, 10, 1, 14, 39]
ind_against1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6]

date_corrected = []
dates = []
stances = []
for tweet in tweets:
  if tweet['stance'] != "not vaccine related":
    stances.append(tweet)
for tweet in stances:
  tweet["tweet_date"] = datetime.strftime(datetime.strptime(tweet["tweet_date"],'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d')
  date_corrected.append(tweet)
for tweet in date_corrected:
  dates.append(tweet['tweet_date'])

unique_dates = []
for day in dates:
  if day not in unique_dates:
    unique_dates.append(day)
unique_dates = sorted(unique_dates)

usa_day_case = {}
for c in cases['USA']['data'][1:]:
  if c['date'] in unique_dates:
    usa_day_case[c['date']] = c['new_cases']

daydiv = []
for i in usa_day_case:
  daydiv.append(i)
daydiv_groups = []
for i in range(18):
  daydiv_groups.append(daydiv[i*10:(i+1)*10])

mex_day_case = {}
for c in cases['MEX']['data'][1:]:
  if c['date'] in unique_dates:
    mex_day_case[c['date']] = c['new_cases']

ind_day_case = {}
for c in cases['IND']['data'][1:]:
  if c['date'] in unique_dates:
    ind_day_case[c['date']] = c['new_cases']


usa_stance_pro = []
usa_stance_against = []
mex_stance_pro = []
mex_stance_against = []
ind_stance_pro = []
ind_stance_against = []
for tweet in date_corrected:
  if tweet['country'] == 'USA' and tweet['stance'] == 'pro':
    usa_stance_pro.append(tweet['tweet_date'])
  elif tweet['country'] == 'USA' and tweet['stance'] == 'against':
    usa_stance_against.append(tweet['tweet_date'])
  elif tweet['country'] == 'MEXICO' and tweet['stance'] == 'pro':
    mex_stance_pro.append(tweet['tweet_date'])
  elif tweet['country'] == 'MEXICO' and tweet['stance'] == 'against':
    mex_stance_against.append(tweet['tweet_date'])
  elif tweet['country'] == 'INDIA' and tweet['stance'] == 'pro':
    ind_stance_pro.append(tweet['tweet_date'])
  elif tweet['country'] == 'INDIA' and tweet['stance'] == 'against':
    ind_stance_against.append(tweet['tweet_date'])

c = []
for i in range(18):
  count = 0
  for d in ind_stance_against:
    if d in daydiv_groups[i]:
      count+=1
  c.append(count)

def bubblechartData():
    data = []
    colors = ['blue','red','green']
    for i,country in enumerate(['USA','MEXICO','INDIA']):
        if country == 'USA':
            day_case = usa_day_case
            size_case = usa_pro1
        elif country == 'MEXICO':
            day_case = mex_day_case
            size_case = mex_pro1
        else:
            day_case = ind_day_case
            size_case = ind_pro1
        # x_fig = [x for x in day_case.keys()][70::10]#[daydiv1[0],daydiv2[0],daydiv3[0],daydiv4[0]]#[
        # y_fig = [day_case[x] for x in x_fig]
        x_figs = [x for x in day_case.keys()]
        y_f = [x for x in day_case.values()]
        y_figs = [sum(y_f[ii*10:(ii+1)*10])/10 for ii in range(len(x_figs)//10)]
        data.append({
            'x':x_figs[70::10], 
            'y': y_f[70::10], 
            'name' : '{} Pro Vaccination'.format(country),
            'mode' : 'markers',
            'marker': {
                'color': colors[i],
                'opacity': 0.5,
                'size': size_case[6:]
            }})

        data.append({
            'x':x_figs[70::5], 
            'y': y_f[70::5], 
            'name' : 'New Cases Per Day in {}'.format(country),
            'mode' : 'lines',
            'opacity': 0.5,
            'marker': {
                'color': colors[i]
            }})

    return data
