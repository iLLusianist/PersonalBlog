function open_sign_in(){
    window.location.href = "/open_sign_in";
}

function open_index (){
    window.location.href = "/";
}



// function sign_up(){
//     const login = document.getElementById('sign_up_login')
//     const password = document.getElementById('sign_up_password')
//     const repeat_password = document.getElementById('sign_up_repeat_password')
//
//     if (password.value === repeat_password.value){
//         console.log('password correct')
//         const data = {
//             username: login.value,
//             password: password.value
//         }
//         console.log(data)
//         fetch ('/register', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify(data)
//         })
//         .then(response => response.json())
//         .then(data => console.log(data));
//     } else {console.log('Password incorrect')}
// }


//
// function sign_in(){
//     sessionStorage.setItem("is_signed_in", true);
//     window.location.href = "/";
// }
// function logout() {
//     sessionStorage.removeItem("is_signed_in");
//     window.location.href = "/";
// }
// function check_sign_in_status() {
//     const is_signed_in = sessionStorage.getItem("is_signed_in");
//
//     if (is_signed_in) {
//         document.getElementById('logout_button').style.display = 'block'
//         document.getElementById('sign_in_button').style.display = 'none'
//         document.getElementById('add_button').style.display = 'block'
//         document.getElementById('edit_button').style.display = 'block'
//     } else {
//         document.getElementById('logout_button').style.display = 'none'
//         document.getElementById('sign_in_button').style.display = 'block'
//         document.getElementById('add_button').style.display = 'none'
//         document.getElementById('edit_button').style.display = 'none'
//     }
// }

// document.addEventListener("DOMContentLoaded", function (){
//     check_sign_in_status();
// })