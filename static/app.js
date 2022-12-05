// const BASE_URL = "https://qnews.herokuapp.com/api";

//   /** given data about a article, generate html */

// function generateArticleHTML(article) {
//   return `
// <div class="article-display">
//     <div  class="top-box" style="background-image:url(${article.Image_URL}";>
//     </div>
//         <div role="img" aria-label="place alt text here" title="place alt text here" class="background-image"
//     style="background-image:url(${article.Image_URL}";>
//         <img src="" alt="" class="alt-image"/>
//         </div>
//     <div class="article-box">
//         <a href="${article.url}" style="text-decoration:none;">
//          ${article.title}
//         </a>
//     </div>
// </div> `;
// }

//   // /** put initial articles on page. */
// $('#article-list').click(showInitialArticles)
//   async function showInitialArticles() {
//     // const id = $(this).data('id')
//     const response = await axios.get(`${BASE_URL}/articles`);
//       for (let articledata of response.data.articles) {
//         let newarticle = $(generateArticleHTML(articledata));
//         $(".article-list").append(newarticle);
//       }
//     }

  
// $('.delete-article').click(deleteArticle)
// async function deleteArticle(){
//   const id = $(this).data('id')
//   axios.delete(`/categories/articles/${id}`)
//   $(this).parent().remove()
// }

// const btn = document.querySelector(".navbar-brand");
// btn.addEventListener("click", displayCategory())
// let ul = document.createElement('ul')
// async function displayCategory(){  
//   category = await axios.get(`${BASE_URL}/categories`)
//   let li = document.createElement('li')
//   li.innerText=category.data.title
//   ul.append(li)
// }


// $('input[type=search]').on('input', function(){
//   clearTimeout(this.delay);
//   this.delay = setTimeout(function(){
//      $(this).trigger('search');
//   }.bind(this), 800);
// }).on('search',  async function(){
//   if(this.value){
//      console.log(this.value);
//      response = await axios.get(`https://qnews.herokuapp.com/api/get_articles/query_data`)
//      result = response.data.articles
//      let ArticleModel = []
//      for (let i=0; i<result.length; i++){
//       let topic = result[i].title;
//       let des = result[i].description;
//       let url = result[i].url
//       let Image_URL = result[i].urlToImage
//       ArticleModel.push({title:topic, description:des, url:url, image:Image_URL})
//     }
//   }
// });
// // for (let articledata of response.data.articles) {
// //   let newarticle = $(generateArticleHTML(articledata));


// let form = document.getElementById("searchform");
// form.addEventListener('submit', logsubmit);
// async function logsubmit(e){
//   e.preventDefault();  
//   let formdata = document.getElementById("search"); 
//   // let key = formdata.value;
//   let url = `https://qnews.herokuapp.com/api/get_articles/query_data/${key}`
//    await fetch(url, {methods:'GET'}).then((response) => {return response.json()}).then ((data) => {
//     let art = data;
//     let modelArray = []
//     for(let articledata of art.articles){
//       let title = articledata.title;
//       let url = articledata.url;
//       let Image_URL = articledata.urlToImage;
//       modelArray.push({title: title, url: url, Image_URL:Image_URL})
//   }
//   return generateArticleHTML(modelArray);
//   })
// }

$(document).on('click', '.makefavorite', function(e){ 
  e.preventDefault(); 
  const id = $(this).data('id') 
  location.assign(`http://127.0.0.1:5000/favorites/articles/${id}`);
});


// http://127.0.0.1:5000/article


// $(document).on('click', '.getArticle', function(e){ 
//   e.preventDefault(); 
//   $(".maincontent").empty(); 
//   let char = "us"
//   let url = `http://127.0.0.1:5000/api/get_articles/query_data/${char}`
//   res = axios.get(url)
//     .then( res => {
//       res.data.articles.forEach( result => $(".container").append(
//       `
//         <div class="col-12 col-sm-6 col-xl-4" style="margin-top:3rem;">
//           <div class="card">
//             <img src="${result.urlToImage}" class="card-img-top" alt=""> 
//               <div class="card-body">
//                 <a class="card-text" href="${result.url}">
//                   <p>${result.title}</p>
//                 </a>
//               </div>
//           </div>        
//         </div>
      
//       `
//       ))
//   })
// })

  // $(document).ready(function(){    
    // $("#submitBtn").click(function(){ 
        // $("#myForm").submit(function(){
        //   e.preventDefault();        
        //   let searchvalue = $("#search").val();
        //   // var searchvalue = $(this).find('input[type="text"]').val();
        //     alert(searchvalue)
      //     $(".maincontent").empty(); 
      //     // let char = "us"
      //     let url = `http://127.0.0.1:5000/api/get_articles/query_data/${searchvalue}`
      //     return axios.get(url)
      //       .then( res => {
      //         res.data.articles.forEach( result => $(".container").append(
      //         `
      //           <div class="col-12 col-sm-6 col-xl-4" style="margin-top:3rem;">
      //             <div class="card">
      //               <img src="${result.urlToImage}" class="card-img-top" alt=""> 
      //                 <div class="card-body">
      //                   <a class="card-text" href="${result.url}">
      //                     <p>${result.title}</p>
      //                   </a>
      //                 </div>
      //             </div>        
      //           </div>
              
      //         `
      //         ))
      //   })
      // });
    // });
// });


$(document).ready(function(){  
$("#myForm").submit(function(e){
  e.preventDefault();        
  let searchvalue = $("#search").val();
    $(".maincontent").remove();
    $("p").append(`Displaying results for ${searchvalue}`)
    let url = `http://127.0.0.1:5000/api/get_articles/query_data/${searchvalue}`
         axios.get(url)
          .then( res => {
            res.data.articles.forEach( result => $(".container").append(
            `
              <div class="col-sm-6 col-xl-4" style="margin-top:1rem;">
                <div class="card">
                  <img src="${result.urlToImage}" class="card-img-top" alt=""> 
                    <div class="card-body">
                      <a class="card-text" href="${result.url}">
                        <p>${result.title}</p>
                      </a>
                        <small>${result.content}</small>                      
                    </div>
                </div>        
              </div>            
            `
    ))    
  })
});
})

























        // <div class="container-fluid" style="background-color:rgb(255, 255, 255); padding-top:5px; border-radius: .5rem;">
        // <div class="container-fluid">
        //   <div class="row">
        //     <div class="col-12 col-sm-6 col-xl-4 bg-danger" style="height:.3rem;"></div>
        //     <div class="col-12 col-sm-6 col-xl-4 bg-info" style="height:.3rem;"></div>
        //     <div class="col-12 col-sm-6 col-xl-4 bg-warning" style="height:.3rem;"></div>
        //   </div>


  // ).then(facts => {
  //   facts.forEach(data => $("body").append(`<p>${data.text}</p>`));
  // });
  // location.assign(`https://qnews.herokuapp.com/favorites/articles/${id}`);
// });
// $('.makefavorite').on('Click', function(e){
//   e.preventDefault();
//   const id = $(this).data('id')
//   alert("you clicked")
//   location.assign(`https://qnews.herokuapp.com/favorites/articles/${id}/`);
// })



