// Initialiser la date du jour par défaut dans le formulaire
document.getElementById('start_date').valueAsDate = new Date();

const form = document.getElementById('paramForm');
const resultPanel = document.getElementById('resultPanel');

form.addEventListener('submit', async (e) => {
    e.preventDefault(); // Empêche le rechargement brutal de la page

    // Récupération des données du formulaire
    const formData = new FormData(form);
    
    // Gestion explicite des boîtiers de sélection (checkboxes non cochées omises par FormData)
    const params = new URLSearchParams();
    params.append('start_date', formData.get('start_date'));
    params.append('duration_days', formData.get('duration_days'));
    params.append('nb_catego', formData.get('nb_catego'));
    params.append('enum_option', formData.get('enum_option'));
    params.append('flag_lowercase', document.getElementById('flag_lowercase').checked);
    params.append('flag_tf_idf', document.getElementById('flag_tf_idf').checked);

    // 1. Construit l'URL avec les paramètres visibles (Requête GET)
    const apiUrl = `/api/process?${params.toString()}`;
    
    // Optionnel : Met à jour la barre d'adresse du navigateur pour voir les paramètres
    window.history.pushState({}, '', `?${params.toString()}`);

    try {
        // 2. Envoi de la requête au serveur FastAPI
        const response = await fetch(apiUrl);
        if (!response.ok) throw new Error("Erreur serveur lors de la récupération");
        
        const jsonResult = await response.json();

        // 3. Génération dynamique du contenu HTML (H4 et UL)
        resultPanel.innerHTML = "<h2>Résultats du traitement</h2>";
        
        // Parcourt les clés du dictionnaire JSON (ex: "Statistiques globales", etc.)
        for (const [sectionTitle, items] of Object.entries(jsonResult)) {
            // Crée le titre de section H4
            const h4 = document.createElement('h4');
            h4.textContent = sectionTitle;
            resultPanel.appendChild(h4);

            // Crée la liste UL
            const ul = document.createElement('ul');
            items.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                ul.appendChild(li);
            });
            resultPanel.appendChild(ul);
        }

    } catch (error) {
        resultPanel.innerHTML = `<p style="color:red;">Erreur: ${error.message}</p>`;
    }
});

// Gestion du bouton Reset pour nettoyer la division de droite
document.getElementById('resetBtn').addEventListener('click', () => {
    resultPanel.innerHTML = `<p style="color: #666; font-style: italic;">En attente de la soumission des paramètres...</p>`;
    document.getElementById('start_date').valueAsDate = new Date();
    window.history.pushState({}, '', window.location.pathname);
});
