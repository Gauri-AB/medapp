document.addEventListener('DOMContentLoaded', () => {
    const appointmentsList = document.getElementById('appointments-list');
    const appointments = JSON.parse(localStorage.getItem('appointments')) || [];

    function updateAppointmentsList() {
        appointmentsList.innerHTML = '';

        appointments.forEach((appointment, index) => {
            const listItem = document.createElement('li');
            listItem.className = 'list-group-item';
            listItem.innerHTML = `
                <div>
                    <h5>${appointment.patientName}</h5>
                    <p>${new Date(appointment.appointmentDate).toLocaleString()}</p>
                    <p>Doctor: ${appointment.doctorName}</p>
                </div>
                <button class="btn btn-danger btn-sm" onclick="removeAppointment(${index})">Cancel</button>
            `;
            appointmentsList.appendChild(listItem);
        });
    }

    window.removeAppointment = (index) => {
        appointments.splice(index, 1);
        localStorage.setItem('appointments', JSON.stringify(appointments));
        updateAppointmentsList();
    };

    updateAppointmentsList();
});
