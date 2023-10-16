document.addEventListener("DOMContentLoaded", function () {
    var updateBtns = document.getElementsByClassName('update-cart');

    for (var i = 0; i < updateBtns.length; i++) {
        updateBtns[i].addEventListener('click', function () {
            var productId = this.getAttribute('data-product');
            var action = this.getAttribute('data-action');
            console.log('Id :', productId, 'Ação : ', action);
            console.log('User :' ,user)

            if(user=="AnonymousUser"){
                console.log('User is not authenticated')
            }else{
                console.log('User is authenticated, sending data...')
            }
        });
    }
});
