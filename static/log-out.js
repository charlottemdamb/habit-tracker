'use strict'

const button = document.getElementById('logout-modal-btn');

button.addEventListener('click', logOut);

function logOut(){
    fetch('/logout',{
        method: 'POST',
        headers: {
            'Content-Type' : 'application/json'
        }
    
    })
    .then((response)=>{
        window.location.href = '/'
    })
}