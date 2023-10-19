document.addEventListener("DOMContentLoaded", function () {
    var updateBtns = document.getElementsByClassName('update-cart');

    for (var i = 0; i < updateBtns.length; i++) {
        updateBtns[i].addEventListener('click', function () {
            var productId = this.getAttribute('data-product');
            var action = this.getAttribute('data-action');
            
            console.log('User :' ,user)

            if(user=="AnonymousUser"){
                addCookieItem(productId, action)
            }else{
                updateUserOrder(productId, action)
            }
        });
    }
    function updateUserOrder(productId, action){
        console.log('User authenticated')

        var url = '/updateItem/'

        fetch(url,{
            method:'POST',
            headers:{
                'Content-Type':'aplication/json',
                'X-CSRFToken':csrftoken,
            },
            body:JSON.stringify({'productId':productId , 'action':action})
        })
        .then((response) =>{
            return response.json();
        })
        .then((data)=>{
            location.reload()
        });
    }
    function addCookieItem(productId, action){
        if (action == 'add'){
            if(cart[productId]==undefined){
                cart[productId]={'quantitade':1}
            }
            else{
                cart[productId]['quantidade'] += 1
            }
        }
    }
});
