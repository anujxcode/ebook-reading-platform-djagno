
const pdfurl = document.getElementById("bookurlid").value;


let pdfDoc = null,
    pageNum = 1,
    pageIsRendering = false,
    pageNumIsPending = null,
    scale = 1;


const canvas = document.querySelector("#pdfreaderbox"),
    ctx = canvas.getContext('2d')

//render the page

const renderPage = num => {
    pageIsRendering = true;
    
    pdfDoc.getPage(num).then(page => {
        const viewport = page.getViewport({scale});
            canvas.height = viewport.height;
            canvas.width = viewport.width;
        
        const renderCtx = {
            canvasContext:ctx,
            viewport
        }

        page.render(renderCtx).promise.then(()=>{
            pageIsRendering = false;

            if(pageNumIsPending !== null){
                renderPage(pageNumIsPending);
                pageNumIsPending = null;
            }
        });

        // current page
        document.querySelector("#page-num").textContent = num;


    });
    
}

// get the doc
pdfjsLib.getDocument(pdfurl).promise.then(pdfDoc_ => {
    pdfDoc = pdfDoc_;
    document.getElementById("pageCount").textContent = pdfDoc.numPages;
    renderPage(pageNum)
    
}); 



// next previous btn
const queueRenderPage = num =>{
    if(pageIsRendering){
        pageIsRendering = num;
    }else{
        renderPage(num);
    }
}

const showPrevPage = () =>{
    if(pageNum <= 1 ){
        return;
    }else{
        pageNum = pageNum - 1;
        queueRenderPage(pageNum);
        window.scrollTo(0,1);
    }
}

const showNextPage = () =>{
    if(pageNum >=  pdfDoc.numPages){
        return;
    }else{
        pageNum = pageNum + 1;
        queueRenderPage(pageNum);
        window.scrollTo(0,1);
          
    }
}
const zoomIn = () =>{
    if(scale < 2.2){
        scale += 0.3;
        queueRenderPage(pageNum);
    }
}

const zoomOut = () =>{
    if(scale > 0.5){
        scale -= 0.3;
        queueRenderPage(pageNum);
    }
}

// call the function

document.getElementById("btnNext").addEventListener('click',showNextPage)
document.getElementById("btnPrev").addEventListener('click',showPrevPage)

window.addEventListener("keypress" ,(e)=>{
    alert(e.key)
    if(e.key == 'n'){
        
        showNextPage();
        document.getElementById("btnNext").style.background = "red";
        document.getElementById("btnPrev").style.background = "inherit";
    }
    else if(e.key == 'b'){
        showPrevPage();
        document.getElementById("btnNext").style.background = "inherit";
        document.getElementById("btnPrev").style.background = "red";
    }
})


document.getElementById('zoom-in').addEventListener('click',zoomIn);
document.getElementById('zoom-out').addEventListener('click',zoomOut);