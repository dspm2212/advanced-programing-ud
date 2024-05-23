function Login(){
    let username_ = document.getElementById("txtName").value
    let password_ = document.getElementById("txtPassword").value 
    
    //javascript object 
    let LoginData = {
        username: username_, 
        password: password_
    }

    console.log(LoginData)
}