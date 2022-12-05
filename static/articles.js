"use strict";
let articlelist;

async function getAndShowArticlesOnStart(){
  articlelist = await ArticleList.getArticles();
  putArticlesonPage();
  }

function generateArticleMarkup(art){
  return $(`<small class="article-title">${art.title}</small>`)
}
function putArticlesonPage(){
  console.debug("putStoriesOnPage");
  $allStoriesList.empty();


  for (let article of articlelist.articles) {
    const $article = generateArticleMarkup(article);
    $allStoriesList.append($article);
  }

  $allStoriesList.show();
}
