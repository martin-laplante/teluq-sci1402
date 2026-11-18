// Initialiser la date de départ du fichier par défaut dans le formulaire
document.getElementById('start_date').valueAsDate = new Date("1995-06-16");

const form = document.getElementById('paramForm');
const resultPanel = document.getElementById('resultPanel');
const statPanel =  document.getElementById('statPanel');
const topBottom =  document.getElementById('topBottom');


form.addEventListener('submit', async (e) => {
    e.preventDefault(); // Empêche le rechargement brutal de la page

    // Récupération des données du formulaire
    const formData = new FormData(form);
    
    // Gestion explicite des boîtiers de sélection (checkboxes non cochées omises par FormData)
    const params = new URLSearchParams();
    params.append('start_date', formData.get('start_date'));
    params.append('duration_days', formData.get('duration_days'));
    params.append('nb_catego', formData.get('nb_catego'));
    params.append('strategy', formData.get('strategy'));
    params.append('flag_lowercase', document.getElementById('flag_lowercase').checked);
    params.append('flag_tf_idf', document.getElementById('flag_tf_idf').checked);
    // Mettre d'autre param ici, si nécessaire   ##PARAM

    // 1. Construit l'URL avec les paramètres visibles (Requête GET)
    const apiUrl = `/api/process?${params.toString()}`;
    
    // Optionnel : Met à jour la barre d'adresse du navigateur pour voir les paramètres
    window.history.pushState({}, '', `?${params.toString()}`);

    try {
        // 2. Envoi de la requête au serveur FastAPI
        const response = await fetch(apiUrl);
        if (!response.ok) throw new Error("Erreur serveur lors de la récupération");
        
        const jsonResult = await response.json();

        // 3. Génération dynamique du contenu HTML (H4 et UL) "resultPanel" est l'ID html du template ##RESPO##
        resultPanel.innerHTML = "";
        statPanel.innerHTML="";
        topBottom.innerHTML = "<p>La liste de tous les mot selectionnés par ordre décroissant de quantité:</p>";

        // Parcourt les clés du dictionnaire JSON (ex: "Statistiques globales", etc.)  
        // Cle `sectionTitle`, liste: `items`
        for (const [sectionTitle, items] of Object.entries(jsonResult)) {              
            // Crée le titre de section H2
            const h2 = document.createElement('h2');
            h2.textContent = sectionTitle;
            if (sectionTitle == 'Statistiques')
                statPanel.appendChild(h2);
            else if (sectionTitle == 'Palmarès')
                topBottom.appendChild(h2);
            else
                resultPanel.appendChild(h2);

            // Crée la liste UL
            const ul = document.createElement('ul');
            items.forEach(item => {                       // Notre liste
                const li = document.createElement('li');
                const my_arr = item.split("::");
                if (my_arr.length==2)
                    li.innerHTML = '<b>'+my_arr[0]+'</b>:&nbsp;&nbsp;<i>'+my_arr[1]+'</i>';
                else
                    li.textContent = item;
                ul.appendChild(li);
            });
            if (sectionTitle == 'Statistiques') {
                statPanel.appendChild(ul);
            }
            else if (sectionTitle == 'Palmarès')
                topBottom.appendChild(ul);
            else
                resultPanel.appendChild(ul);
        }
        const imageUrl = `/static/errmap.png?t=${Date.now()}`;
        statPanel.innerHTML+="<div><h3>Carte d'erreurs entre W x H et M à l'origine</h3></div>";
        statPanel.innerHTML+=`<img class="errmap" src="${imageUrl}">`;


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
