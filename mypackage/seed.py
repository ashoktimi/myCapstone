import requests
import json
from app import app
from mypackage.models import db, User, Category, Article, CategoryArticle
from mypackage.apidata import SUPER_SECRET_KEY

API_BASE_URL = "https://newsapi.org/v2"

API_SECRET_KEY=SUPER_SECRET_KEY
app.app_context().push()
# db.drop_all()
# db.create_all()


# Fetching data from api and inserting into database table Category

res = requests.get(f"{API_BASE_URL}/top-headlines/sources",
                        params={'apiKey':API_SECRET_KEY})
results = res.json()

def creating_list():
    return[x['category'] for x in results['sources']]
r = creating_list()
for result in [*set(r)]:
    new_category = Category(name=result)                           
    db.session.add(new_category)
    db.session.commit()

def name_list1():
    return[x['url'].split("/")[2]  for x in results['sources'] if x['category']=="general" ]
def name_list2(): 
    return[x['url'].split("/")[2]  for x in results['sources'] if x['category']=="business" ]
def name_list3(): 
    return[x['url'].split("/")[2] for x in results['sources'] if x['category']=="technology" ]
def name_list4(): 
    return[x['url'].split("/")[2]  for x in results['sources'] if x['category']=="entertainment" ]
def name_list5(): 
    return[x['url'].split("/")[2]  for x in results['sources'] if x['category']=="science" ]
def name_list6(): 
    return[x['url'].split("/")[2]  for x in results['sources'] if x['category']=="sports" ]
def name_list7(): 
    return[x['url'].split("/")[2]  for x in results['sources'] if x['category']=="health" ]

g= [*set(name_list1())]
general = ','.join(g)

b= [*set(name_list2())]
business=','.join(b)

t= [*set(name_list3())]
technology= ','.join(t)

e= [*set(name_list4())]
entertainment= ','.join(e)

s= [*set(name_list5())]
science= ','.join(s)

sp= [*set(name_list6())]
sports= ','.join(sp)

h = [*set(name_list7())]
health= ','.join(h)



# # Fetching data from api and inserting into database table articles and categories_articles

# ############## getting article data for category general #########################

response1 = requests.get(f"{API_BASE_URL}/everything", params={'domains':general,'apiKey':API_SECRET_KEY})
data1 = response1.json()
for article in data1['articles']:
    author =article['author']
    title = article['title']
    description = article['description']
    url = article['url']
    Image_URL = article['urlToImage']
    published_date = article['publishedAt']
    content = article['content']

    new_article = Article(author=author, 
                       title=title,
                       description=description,
                       url=url,
                       Image_URL=Image_URL,                   
                       published_date=published_date,
                       content=content)
    db.session.add(new_article)

lst1 = []
for i  in data1['articles']:
    title=i['title']
    lst1.append(title)

for ag in lst1:
    category = Category.query.filter_by(name="general").first()
    category_id = category.id
    if article is not None:
        article = Article.query.filter_by(title=ag).first()
        article_id = article.id
        new_cat_article = CategoryArticle(category_id=category_id, article_id=article_id)
        db.session.add(new_cat_article)
        db.session.commit()


# ############## getting article data for category business #########################
response2 = requests.get(f"{API_BASE_URL}/everything", params={'domains':business,'apiKey':API_SECRET_KEY})
data2 = response2.json()
for article in data2['articles']:
    author =article['author']
    title = article['title']
    description = article['description']
    url = article['url']
    Image_URL = article['urlToImage']
    published_date = article['publishedAt']
    content = article['content']

    new_article = Article(author=author, 
                       title=title,
                       description=description,
                       url=url,
                       Image_URL=Image_URL,                   
                       published_date=published_date,
                       content=content)
    db.session.add(new_article)

lst2 = []
for i  in data2['articles']:
    title=i['title']
    lst2.append(title)
for ag in lst2:
    category = Category.query.filter_by(name="business").first()
    category_id = category.id
    if article is not None:
        article = Article.query.filter_by(title=ag).first()
        article_id = article.id
        new_cat_article = CategoryArticle(category_id=category_id, article_id=article_id)
        db.session.add(new_cat_article)
        db.session.commit()


# # ############## getting article data for category technology #########################
response3 = requests.get(f"{API_BASE_URL}/everything", params={'domains':technology,'apiKey':API_SECRET_KEY})
data3 = response3.json()
for article in data3['articles']:
    author =article['author']
    title = article['title']
    description = article['description']
    url = article['url']
    Image_URL = article['urlToImage']
    published_date = article['publishedAt']
    content = article['content']

    new_article = Article(author=author, 
                       title=title,
                       description=description,
                       url=url,
                       Image_URL=Image_URL,                   
                       published_date=published_date,
                       content=content)
    db.session.add(new_article)
    db.session.commit()

lst3 = []
for i  in data3['articles']:
    title=i['title']
    lst3.append(title)
for ag in lst3:
    category = Category.query.filter_by(name="technology").first()
    category_id = category.id
    if article is not None:
        article = Article.query.filter_by(title=ag).first()
        article_id = article.id
        new_cat_article = CategoryArticle(category_id=category_id, article_id=article_id)
        db.session.add(new_cat_article)
        db.session.commit()

# # ############## getting article data for category entertainment #########################
response4 = requests.get(f"{API_BASE_URL}/everything", params={'domains':entertainment,'apiKey':API_SECRET_KEY})
data4 = response4.json()

for article in data4['articles']:
    author =article['author']
    title = article['title']
    description = article['description']
    url = article['url']
    Image_URL = article['urlToImage']
    published_date = article['publishedAt']
    content = article['content']

    new_article = Article(author=author, 
                       title=title,
                       description=description,
                       url=url,
                       Image_URL=Image_URL,                   
                       published_date=published_date,
                       content=content)
    db.session.add(new_article)
    db.session.commit()
   
lst4 = []
for i  in data4['articles']:
    title=i['title']
    lst4.append(title)
for ag in lst4:
    category = Category.query.filter_by(name="entertainment").first()
    category_id = category.id
    if article is not None:
        article = Article.query.filter_by(title=ag).first()
        article_id = article.id
        new_cat_article = CategoryArticle(category_id=category_id, article_id=article_id)
        db.session.add(new_cat_article)
        db.session.commit()

# # ############## getting article data for category science #########################

response5 = requests.get(f"{API_BASE_URL}/everything", params={'domains':science,'apiKey':API_SECRET_KEY})
data5 = response5.json()
for article in data5['articles']:
    author =article['author']
    title = article['title']
    description = article['description']
    url = article['url']
    Image_URL = article['urlToImage']
    published_date = article['publishedAt']
    content = article['content']

    new_article = Article(author=author, 
                       title=title,
                       description=description,
                       url=url,
                       Image_URL=Image_URL,                   
                       published_date=published_date,
                       content=content)
    db.session.add(new_article)
    db.session.commit()
   
lst5 = []
for i  in data5['articles']:
    title=i['title']
    lst5.append(title)
for ag in lst5:
    category = Category.query.filter_by(name="science").first()
    category_id = category.id
    if article is not None:
        article = Article.query.filter_by(title=ag).first()
        article_id = article.id
        new_cat_article = CategoryArticle(category_id=category_id, article_id=article_id)
        db.session.add(new_cat_article)
        db.session.commit()

# # ############## getting article data for category sports #########################
response6 = requests.get(f"{API_BASE_URL}/everything", params={'domains':sports,'apiKey':API_SECRET_KEY})
data6 = response6.json()


for article in data6['articles']:
    author =article['author']
    title = article['title']
    description = article['description']
    url = article['url']
    Image_URL = article['urlToImage']
    published_date = article['publishedAt']
    content = article['content']

    new_article = Article(author=author, 
                       title=title,
                       description=description,
                       url=url,
                       Image_URL=Image_URL,                   
                       published_date=published_date,
                       content=content)
    db.session.add(new_article)
    db.session.commit()

lst6 = []
for i  in data6['articles']:
    title=i['title']
    lst6.append(title)
for ag in lst6:
    category = Category.query.filter_by(name="sports").first()
    category_id = category.id
    if article is not None:
        article = Article.query.filter_by(title=ag).first()
        article_id = article.id
        new_cat_article = CategoryArticle(category_id=category_id, article_id=article_id)
        db.session.add(new_cat_article)
        db.session.commit()

# # ############## getting article data for category health #########################


response7 = requests.get(f"{API_BASE_URL}/everything", params={'domains':health,'apiKey':API_SECRET_KEY})
data7 = response7.json()

for article in data7['articles']:
    author =article['author']
    title = article['title']
    description = article['description']
    url = article['url']
    Image_URL = article['urlToImage']
    published_date = article['publishedAt']
    content = article['content']

    new_article = Article(author=author, 
                       title=title,
                       description=description,
                       url=url,
                       Image_URL=Image_URL,                   
                       published_date=published_date,
                       content=content)
    db.session.add(new_article)
    db.session.commit()

lst7 = []
for i  in data7['articles']:
    title=i['title']
    lst7.append(title)
for ag in lst7:
    category = Category.query.filter_by(name="health").first()
    category_id = category.id
    if article is not None:
        article = Article.query.filter_by(title=ag).first()
        article_id = article.id
        new_cat_article = CategoryArticle(category_id=category_id, article_id=article_id)
        db.session.add(new_cat_article)
        db.session.commit()
