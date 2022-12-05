"use strict";
const BASE_URL = "https://qnews.herokuapp.com/api";

class Article{
    constructor({ title, url,urlToImage}) {
      this.title = title;
      this.url = url;
      // console.log(this.url)
      this.urlToImage = urlToImage;
    }
    // getHostName() {
    //   return new URL(this.url).host;
    // }
  }
  
  class ArticleList {
    constructor(articles){
      this.articles = articles;
    }
  
  
  static async getArticles(){
    let key = 'bitcoin'
    const response = await axios({
      url:`${BASE_URL}/get_articles/query_data/${key}`,
      method:"GET",
    });
    const stories = response.data.articles.map(story => new Article(story));
    return new ArticleList(stories);
  }
  }