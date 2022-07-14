//Setting axios defaults to handle the csrftoken
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";


//Function to grab form fields for signup and using axios to do a POST request to push to backside
function signUp(event) {
    event.preventDefault()
    const first_name = document.getElementById("first_name").value;
    const last_name = document.getElementById("last_name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;  
    

    //building my form data for Post request
    const data = new FormData();
    data.append("first_name", first_name);
    data.append("last_name", last_name);
    data.append("email", email);
    data.append("password", password);
    //actual post and .then
    axios.post('signup', data).then((response) => {
        //alerting user of status and then re-directing to home page
        alert(response['data']['status']);
        window.location.href = '/todos';
    });
    
};

//Function to grab form fields for login and using axios to do a POST request to push to backside
function logIn(event) {
    event.preventDefault()
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;  

    //building my form data for Post request
    const data = new FormData();
    data.append("email", email);
    data.append("password", password);
    //actual post and .then
    axios.post('login', data).then((response) => {
        //alerting user of status and then re-directing to home page
        alert(response['data']['status']);
        window.location.href = '/todos';
    });
    
};