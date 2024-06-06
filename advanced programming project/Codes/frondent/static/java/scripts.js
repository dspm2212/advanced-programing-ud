document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const requestData = {
        email: email,
        password: password
    };

    console.log('Form Data Submitted: ', requestData);

    // API request
    fetch('https://api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert('Login successful!');
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Login failed.');
    });
});
