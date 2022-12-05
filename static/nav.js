"use strict";
function navAllStories(evt) {
    console.debug("navAllStories", evt);
    hidePageComponents();
    putArticlesonPage();
  }
  
  $body.on("click", "#nav-all", navAllStories);