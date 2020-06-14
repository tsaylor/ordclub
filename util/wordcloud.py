from profiles.models import Status
status_text = []
all_statuses = Status.objects.all()
for s in all_statuses:
    j = s.status_json
    try:
        if 'retweeted_status' in j:
            status_text.append(j['retweeted_status']['text'])
        else:
            status_text.append(j['text'])
    except KeyError as e:
        print e
        print j
        raise e

from wordcloud import WordCloud, STOPWORDS

stopwords = STOPWORDS.update(['t', 'co', 'amp', 'https', 'http', 'ly', 'rt'])
wc = WordCloud(font_path='/Library/Fonts/Microsoft Sans Serif.ttf', stopwords=stopwords, width=1000, height=600)
wc.generate(status_doc)
wc.to_file('img.png')
