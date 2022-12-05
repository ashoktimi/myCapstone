"use strict";
const $body = $("body");
const $allStoriesList = $("#all-stories-list");
const $storiesLists = $(".stories-list");

async function start() {
    console.debug("start"); 
    await getAndShowArticlesOnStart();
  }
  
 $(start);