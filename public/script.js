document.addEventListener('DOMContentLoaded', () => {
    const loader = document.getElementById('loader');
    const dataContainer = document.getElementById('data-container');
    const errorContainer = document.getElementById('error-container');

    const fetchData = async () => {
        try {
            const response = await fetch('data.json');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            renderData(data);
            showUI(dataContainer);
        } catch (error) {
            console.error("Error fetching or parsing data.json:", error);
            showUI(errorContainer);
        }
    };

    const showUI = (elementToShow) => {
        loader.classList.add('hidden');
        dataContainer.classList.add('hidden');
        errorContainer.classList.add('hidden');
        elementToShow.classList.remove('hidden');
    };

    const createCard = (title, value) => {
        const card = document.createElement('div');
        card.className = 'card';
        
        const cardTitle = document.createElement('h3');
        cardTitle.textContent = title;
        
        const cardValue = document.createElement('p');
        cardValue.textContent = value;
        
        card.appendChild(cardTitle);
        card.appendChild(cardValue);
        return card;
    };
    
    const renderData = (data) => {
        // Render Current Versions
        const currentGrid = document.getElementById('current-cards');
        if (data.current && Object.keys(data.current).length > 0) {
            for (const [key, value] of Object.entries(data.current)) {
                currentGrid.appendChild(createCard(key, value));
            }
        } else {
             document.getElementById('current-versions').classList.add('hidden');
        }

        // Render Future Versions
        const futureGrid = document.getElementById('future-cards');
        if (data.future && Object.keys(data.future).length > 0) {
            for (const [key, value] of Object.entries(data.future)) {
                futureGrid.appendChild(createCard(key, value));
            }
        } else {
            document.getElementById('future-versions').classList.add('hidden');
        }

        // Render Android Versions
        const androidGrid = document.getElementById('android-cards');
        if (data.android && Object.keys(data.android).length > 0) {
             for (const [key, value] of Object.entries(data.android)) {
                androidGrid.appendChild(createCard(key, value));
            }
        } else {
            document.getElementById('android-versions').classList.add('hidden');
        }

        // Render Past Versions
        const pastGrid = document.getElementById('past-cards');
        if (data.past && Object.keys(data.past).length > 0) {
            for (const [key, value] of Object.entries(data.past)) {
                pastGrid.appendChild(createCard(key, value));
            }
        } else {
            document.getElementById('past-versions').classList.add('hidden');
        }
    };

    fetchData();
});