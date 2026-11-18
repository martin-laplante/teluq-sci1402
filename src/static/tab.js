function ouvrirOnglet(evenement, nomOnglet) {
  // 1. Déclarer les variables
  let i, tabcontent, tablinks;

  // 2. Masquer tout le contenu des onglets
  tabcontent = document.getElementsByClassName("tab-content");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // 3. Supprimer la classe "active" de tous les boutons
  tablinks = document.getElementsByClassName("tab-button");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // 4. Afficher l'onglet actuel et ajouter la classe "active" au bouton cliqué
  document.getElementById(nomOnglet).style.display = "block";
  evenement.currentTarget.className += " active";
}
