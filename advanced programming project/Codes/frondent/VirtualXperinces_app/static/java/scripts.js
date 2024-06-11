
// login API 
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

// Events 
document.getElementById('event-form').addEventListener('submit', function (event) {
    event.preventDefault();
    
    // Gather form data
    const eventName = document.getElementById('event-name').value;
    const eventDescription = document.getElementById('event-description').value;
    const eventType = document.getElementById('event-type').value;
    const password = eventType === 'private' ? document.getElementById('password').value : null;

    // Create event object
    const eventData = {
        name: eventName,
        description: eventDescription,
        type: eventType,
        password: password
    };

    // Send data to the backend
    fetch('YOUR_BACKEND_API_ENDPOINT', { // Replace with your actual API endpoint
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // Add any other headers you need here, such as authentication tokens
        },
        body: JSON.stringify(eventData)
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response data
        console.log('Success:', data);
        // You can add more logic here to handle success, like showing a success message or redirecting the user
    })
    .catch((error) => {
        console.error('Error:', error);
        // Handle errors here, such as showing an error message to the user
    });
});

function handleEventTypeChange() {
    var eventType = document.getElementById('event-type').value;
    var passwordGroup = document.getElementById('password-group');
    if (eventType === 'private') {
        passwordGroup.style.display = 'block';
    } else {
        passwordGroup.style.display = 'none';
    }
}

