
function ShowPass() {
    var PassShow = document.getElementById("txt_password");
    var cPassShow = document.getElementById("txt_cpassword");
    var oPassShow = document.getElementById("txt_opassword");

    var check = document.getElementById("check_box_show");
    if (check.checked) {
        PassShow.removeAttribute('type');
        cPassShow.removeAttribute('type');
        oPassShow.removeAttribute('type');
    }
    else {
        PassShow.setAttribute('type', 'password');
        cPassShow.setAttribute('type', 'password');
        oPassShow.setAttribute('type', 'password');
    }
}
var NavLinks = document.getElementById('navLinks');
function openMenu(){
    NavLinks.style.top ="60px";
    
}
function closeMenu(){
    NavLinks.style.top="-1000px";
}

function isNumberKey(eve) {
    var charCode = (evt.which) ? evt.which : evt.keyCode
    if (charCode > 31 && (charCode < 48 || charCode > 57))
        return false;
    return true;
}


function ViewMore() {
    var menuContent2 = document.getElementById("menu-content2");
    var CViewMore = document.getElementById("c_viewmore");

    if (menuContent2.style.display == "none") {
        menuContent2.style.display = "flex";
        CViewMore.innerHTML = "View Less"
    }
    else {
        menuContent2.style.display = "none";
        CViewMore.innerHTML = "View More"
    }
   
}


var Preloader =document.getElementById('preloader');
window.addEventListener('load',function(){
    Preloader.style.display="none"
})

var MessCloseBtn = document.getElementById('message_close_btn');
var SMessage = document.getElementById('ssmessage');
var NofiSound = document.getElementById('notifi');
    
if(SMessage.style.top == 0){
    NofiSound.play();
}
MessCloseBtn.addEventListener('click',function(){
    SMessage.style.top="-100px"; 
})

setInterval(function(){
    SMessage.style.top="-100px";
},3000)


