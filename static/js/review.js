var rating = document.getElementsByName("rating");

for (let i = 0; i < rating.length; i++) {
    const element = rating[i];
    let x = document.getElementById(element.id);
    x.addEventListener('click',function(){
        document.getElementById('review').setAttribute('placeholder','write review now')
        document.getElementById('review').removeAttribute("disabled");
        document.getElementById('review').focus();
        document.getElementById('post_review').style.color ="hotpink"
    })
    

    
}

// var rate1 = document.getElementById("rate_1");

// rate1.addEventListener('click',function(){
//    
// })

