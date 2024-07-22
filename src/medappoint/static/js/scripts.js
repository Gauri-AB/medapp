document.addEventListener('DOMContentLoaded', () => {
    const appointmentForm = document.getElementById('appointment-form');

    appointmentForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const patientName = document.getElementById('patientName').value;
        const appointmentDate = document.getElementById('appointmentDate').value;
        const doctorName = document.getElementById('doctorName').value;

        fetch('/schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                patientName,
                appointmentDate,
                doctorName
            })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            window.location.href = '/appointments';
        })
        .catch(error => console.error('Error:', error));
    });
});
