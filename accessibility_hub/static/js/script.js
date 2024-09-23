document.addEventListener('DOMContentLoaded', function () {
    var clickableRows = document.querySelectorAll('.clickable-row');
    clickableRows.forEach(function (row) {
        row.addEventListener('click', function () {
            window.location = row.dataset.href;
        });
    });
});

function checkForUpdatesOrganisation() {
    fetch('../updates_organisatie/', {method: 'GET'})
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#list-recent-organisation tbody');
            tbody.innerHTML = '';

            data.forEach(organisatie => {
                const row = document.createElement('tr');
                row.classList.add('clickable-row');
                row.setAttribute('data-href', `/medewerkers/organisatie/${organisatie.id}`);

                const dateJoined = new Date(organisatie.date_joined);

                const formattedDate = `${('0' + dateJoined.getDate()).slice(-2)}-${('0' + (dateJoined.getMonth() + 1)).slice(-2)}-${dateJoined.getFullYear()} ${('0' + dateJoined.getHours()).slice(-2)}:${('0' + dateJoined.getMinutes()).slice(-2)}:${('0' + dateJoined.getSeconds()).slice(-2)}`;

                function escapeHTML(str) {
                    return str.replace(/&/g, "&amp;")
                              .replace(/</g, "&lt;")
                              .replace(/>/g, "&gt;")
                              .replace(/"/g, "&quot;")
                              .replace(/'/g, "&#39;");
                }

                row.innerHTML = `
                    <td>${escapeHTML(organisatie.bedrijfsnaam)}</td>
                    <td>${escapeHTML(organisatie.email)}</td>
                    <td>${escapeHTML(organisatie.first_name)}</td>
                    <td>${escapeHTML(organisatie.last_name)}</td>
                    <td>${escapeHTML(organisatie.status)}</td>
                    <td>${escapeHTML(formattedDate)}</td>
                `;

                tbody.appendChild(row);
            });

            document.querySelectorAll('.clickable-row').forEach(row => {
                row.addEventListener('click', function () {
                    window.location.href = row.getAttribute('data-href');
                });
            });
        })
        .catch(error => {
            console.error('Fout bij het ophalen van updates:', error);
        });
}

setInterval(checkForUpdatesOrganisation, 2000);

function checkForUpdatesResearch() {
    fetch('../updates_onderzoek/', {method: 'GET'})
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#list-recent-researches tbody');
            tbody.innerHTML = '';

            data.forEach(onderzoek => {
                const row = document.createElement('tr');
                row.classList.add('clickable-row');
                row.setAttribute('data-href', `/medewerkers/onderzoek/${onderzoek.id}`);


                row.innerHTML = `
                    <td>${onderzoek.titel}</td>
                    <td>${onderzoek.organisatie}</td>
                    <td>${onderzoek.startdatum}</td>
                    <td>${onderzoek.einddatum}</td>
                    <td>${onderzoek.status}</td>
                `;

                tbody.appendChild(row);
            });

            document.querySelectorAll('.clickable-row').forEach(row => {
                row.addEventListener('click', function () {
                    window.location.href = row.getAttribute('data-href');
                });
            });
        })
        .catch(error => {
            console.error('Fout bij het ophalen van updates:', error);
        });
}

setInterval(checkForUpdatesResearch, 2000);

document.addEventListener('DOMContentLoaded', function () {
    var searchInputs = document.querySelectorAll('.search_input');

    searchInputs.forEach(function (searchInput) {
        searchInput.addEventListener('keyup', function () {
            var value = this.value.toLowerCase();
            var tableRows = this.closest('.tab-pane').querySelectorAll('.table tbody tr');

            tableRows.forEach(function (row) {
                var rowText = row.textContent.toLowerCase();
                if (rowText.indexOf(value) > -1) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });
});
