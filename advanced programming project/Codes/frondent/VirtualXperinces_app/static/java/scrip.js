// scrip.js
document.addEventListener('DOMContentLoaded', () => {
    fetchActivityDetails();
    fetchComments();
});

function fetchActivityDetails() {
    fetch('https://api.example.com/activity-details')
        .then(response => response.json())
        .then(data => {
            const detailsContainer = document.getElementById('activity-details');
            detailsContainer.innerHTML = `
                <li><span class="bold">Submission Deadline:</span> ${data.submissionDeadline}</li>
                <li><span class="bold">Requirements:</span>
                    <ul>
                        ${data.requirements.map(req => `<li>${req}</li>`).join('')}
                    </ul>
                </li>
                <li><span class="bold">Deliverables:</span>
                    <ul>
                        ${data.deliverables.map(del => `<li>${del}</li>`).join('')}
                    </ul>
                </li>
            `;
        })
        .catch(error => console.error('Error fetching activity details:', error));
}

function fetchComments() {
    fetch('https://api.example.com/comments')
        .then(response => response.json())
        .then(data => {
            const commentsContainer = document.getElementById('comments');
            commentsContainer.innerHTML = data.map(comment => `
                <div class="comment">
                    <img src="${comment.avatarUrl}" alt="Avatar">
                    <div>
                        <h3>${comment.author}</h3>
                        <p>${comment.text}</p>
                    </div>
                </div>
            `).join('');
        })
        .catch(error => console.error('Error fetching comments:', error));
}
