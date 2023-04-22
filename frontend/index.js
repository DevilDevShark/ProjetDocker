const API_URL = "http://localhost:5001";

async function fetchPetitions(isClosed) {
    const response = await fetch(`${API_URL}/petitions?closed=${isClosed}`);
    const petitions = await response.json();
    return petitions;
}

function createPetitionElement(petition) {
    const li = document.createElement("li");
    li.innerHTML = `<strong>${petition.title}</strong><br>${petition.content}`;
    return li;
}

async function loadPetitions() {
    const openPetitions = await fetchPetitions(false);
    const pastPetitions = await fetchPetitions(true);

    const openPetitionsList = document.getElementById("open-petitions-list");
    const pastPetitionsList = document.getElementById("past-petitions-list");

    openPetitions.forEach((petition) => {
        openPetitionsList.appendChild(createPetitionElement(petition));
    });

    pastPetitions.forEach((petition) => {
        pastPetitionsList.appendChild(createPetitionElement(petition));
    });
}

loadPetitions();
