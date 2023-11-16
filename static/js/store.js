var viewButtons = document.getElementsByClassName('view-product')

console.log(viewButtons);

for (i = 0; i<viewButtons.length; i++ ){
    viewButtons[i].addEventListener('click', function () {
        var prodID = this.dataset.prod
        url = `/view_product/${prodID}`
        window.location = url
    })
}


