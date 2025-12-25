let currentPuzzle = null;
let audio;
let currentMedia = null;
let currentPhrases = null;
let currentPhraseIndex = 0;
let messageTimeout = null;

window.onload = () => {
    loadState();
};

// -------------------------------------------------------------
// Charger l’état du jeu depuis le serveur
// -------------------------------------------------------------
function loadState() {
    fetch("/api/state")
        .then(r => r.json())
        .then(updateView)
        .catch(err => showMessage("Erreur : " + err));
}

// -------------------------------------------------------------
// Affichage général
// -------------------------------------------------------------
function updateView(state) {
    const img = document.getElementById("room-image");
    img.src = `${mediaUrl}/rooms/` + state.image;

    const gameOverlay = document.getElementById('game-overlay');
    gameOverlay.classList.add("hidden");
    const inputContainer = document.getElementById('input-container');
    inputContainer.classList.add('hidden');

    clearZones();
    renderZones(state.zones, state.bools);
    updateInventory(state.inventory);
    if (state.phrases && state.phrases.length > 0) {
        currentPhrases = state.phrases;
        currentPhraseIndex = 0;
        showMessage(currentPhrases[0]["message"],"phrase",0,( currentPhrases.length == 1) ? "✖" : "⇒",currentPhrases[0]["image"]);

    } else {
        currentPhrases = null;
        currentPhraseIndex = 0;
    }
}

// -------------------------------------------------------------
// Affichage des zones cliquables
// -------------------------------------------------------------
function renderZones(zones, bools) {
    const container = document.getElementById("room-container");

    zones.forEach(z => {
        const div = document.createElement("div");
        div.className = "zone";

        const [x1, y1, w, h] = z.coords;

        div.style.left = x1 + "px";
        div.style.top = y1 + "px";
        div.style.width = w + "px";
        div.style.height = h + "px";
        if (z.image) {
            const img = document.createElement("img");
            img.src = `${mediaUrl}/zones/`+z.image;
            img.style.width = "100%";
            img.style.height = "100%";
            img.style.objectFit = "cover";
            div.appendChild(img);
        }
        if (z.type == "bool" && (z.image_true || z.image_false)) {
            if (z.bool_id in bools) {
                const img = document.createElement("img");
                if (bools[z.bool_id].status) {
                    img.src = `${mediaUrl}/zones/`+z.image_true;
                } else {
                    img.src = `${mediaUrl}/zones/`+z.image_false;
                }
                img.style.width = "100%";
                img.style.height = "100%";
                img.style.objectFit = "cover";
                div.appendChild(img);
            }
        }
        div.onclick = () => clickZone(z.id);

        container.appendChild(div);
    });
}

// -------------------------------------------------------------
// Suppression des zones cliquables
// -------------------------------------------------------------
function clearZones() {
    document.querySelectorAll(".zone").forEach(z => z.remove());
}

// -------------------------------------------------------------
// Envoi d’un clic "objet de l'inventaire" au serveur
// -------------------------------------------------------------
function clickObject(objet, media) {
    fetch("/api/clickObject", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ object_id: objet.id,media_id: media ? media.id : null,media_version:media ? media.version : null })
    })
    .then(r => r.json())
    .then(handleEvent)
    .catch(err => showMessage("Erreur action : " + err));
}

// -------------------------------------------------------------
// Envoi d’un clic "zone" au serveur
// -------------------------------------------------------------
function clickZone(zoneId) {
    fetch("/api/click", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ zone_id: zoneId })
    })
    .then(r => r.json())
    .then(handleEvent)
    .catch(err => showMessage("Erreur action : " + err));
}

// -------------------------------------------------------------
// Gestion des réponses du serveur
// -------------------------------------------------------------
function handleEvent(event) {

    // Déplacement
    if (event.event === "move") {
        if (event.text){
            showMessage(event.text.message, "normal", 5000, "", event.text.image);
        }
        
        fermeMedia();
        loadState();
        return;
    }

    // Recommencer.
    if (event.event === "game_reset") {
        location.reload();
    }

    // Condition manquante pour quelque chose.
    if (event.event === "missing_condition") {
        showMessage(event.message.message, "normal", 5000, "", image=event.message.image);
        return;
    }

    // Déposer qqch avant de pouvoir prendre l'objet
    if (event.event === "inventory_full") {
        showMessage("Déposez un objet avant de pouvoir prendre celui-ci.","normal",5000,"","narrateur.png")
        return;
    }

    // Objet trouvé
    if (event.event === "item_found") {
        showMessage("Objet trouvé : " + event.item.name,"normal",5000,"","narrateur.png")
        loadState();
        return;
    }

    // Message
    if (event.event === "message") {
        showMessage(event.message.message,"normal",5000,"",image=event.message.image);
        return;
    }

    // Déjà pris
    if (event.event === "already_picked") {
        showMessage("Rien de plus ici.","normal",5000,"","narrateur.png")
        return;
    }

    // Zone bloquée
    if (event.event === "blocked") {
        showMessage("Vous ne pouvez pas accéder ici pour l’instant.","normal",5000,"","narrateur.png")
        return;
    }

    // Interrupteur
    if (event.event === "switch_on") {
        loadState()
        return;
    }
    if (event.event === "switch_off") {
        loadState()
        return;
    }

    // Objet posé
    if (event.event === "deleted_object") {
        showMessage(event.message.message,"normal",5000,"",event.message.image);
    }

    // Input énigme
    if (event.event === "show_input") {
        if(event.input.message) {
            showMessage(event.input.message.message,"normal",5000,"",event.input.message.image);
        }
        removeInputAndButton();
        const inputContainer = document.getElementById('input-container');
        const imageElement = document.getElementById('input-image-to-display');
        const gameOverlay = document.getElementById('game-overlay');
        gameOverlay.classList.remove('hidden');
        
        // Mettre l'URL de l'image dans l'élément img
        imageElement.src = `${mediaUrl}/inputs/`+event.input.image;
        
        // Afficher le div contenant l'image
        inputContainer.classList.remove('hidden');
        
        // Ajouter un événement sur l'image pour fermer l'affichage
        imageElement.onclick = function() {
            imageElement.src='';
            gameOverlay.classList.add('hidden');
            inputContainer.classList.add('hidden');
            removeInputAndButton();
        };

        createInputAndButton(event.input);

        function createInputAndButton(input) {
            // Créer l'input text
            const inputElement = document.createElement('input');
            inputElement.type = 'text';
            inputElement.id = 'user-input';
            inputElement.style.position = 'absolute';
            inputElement.style.left = `${input.input_position[0]}px`;
            inputElement.style.top = `${input.input_position[1]}px`;
            inputContainer.appendChild(inputElement);

            // Créer le bouton OK
            const buttonElement = document.createElement('button');
            if (event.input.ok_text) {
                buttonElement.textContent = event.input.ok_text;
            } else {
                buttonElement.textContent = 'Démarrer';
            }
            buttonElement.id = 'submit-button';
            buttonElement.style.position = 'absolute';
            buttonElement.style.left = `${input.ok_position[0]}px`;
            buttonElement.style.top = `${input.ok_position[1]}px`;
            inputContainer.appendChild(buttonElement);

            // Placeholder
            inputElement.placeholder = input.placeholder ?? '';
            inputElement.focus();
            inputElement.select();

            // Fonction de validation
            function validateInput() {
                const userInput = inputElement.value.trim().toLowerCase();
                fetch("/api/testEnigme", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({ input_id: input.id, valeur:userInput})
                })
                .then(r => r.json())
                .then(handleEvent)
                .catch(err => showMessage("Erreur action : " + err));
            }

            // Ajouter l'événement de validation du bouton OK
            buttonElement.onclick = validateInput;

            // Ajouter un événement pour la touche Enter
            inputElement.addEventListener('keydown', function(event) {
                if (event.key === 'Enter') {
                    event.preventDefault(); // empêche le comportement par défaut (soumission d’un form)
                    validateInput();        // simule le clic sur le bouton
                }
            });
        }


        // Fonction pour retirer l'input et le bouton après la validation ou la fermeture de l'image
        function removeInputAndButton() {
            const inputElement = document.getElementById('user-input');
            const buttonElement = document.getElementById('submit-button');
            if (inputElement) inputElement.remove();
            if (buttonElement) buttonElement.remove();
        }
    }

    // Afficher ou jouer un média.
    if (event.event === "show_media") {
        if(event.media.message)
            showMessage(event.media.message.message,"normal",5000,"",event.media.message.image);
        if (event.media.image) {
            // Récupérer l'élément div et l'image
            const imageContainer = document.getElementById('image-container');
            const imageElement = document.getElementById('image-to-display');
            const gameOverlay = document.getElementById('game-overlay');

            gameOverlay.classList.remove('hidden');

            // Mettre l'URL de l'image dans l'élément img
            imageElement.src = `${mediaUrl}/media/`+event.media.image;
            
            // Afficher le div contenant l'image
            imageContainer.classList.remove('hidden');
            
            // Ajouter un événement sur l'image pour fermer l'affichage
            imageElement.onclick = function() {
                imageElement.src='';
                gameOverlay.classList.add('hidden');
                imageContainer.classList.add('hidden');
                currentMedia = null;
            };
        }
        if (event.media.audio) {
            if (audio && !audio.paused) {
                audio.pause();  // Arrêter l'audio
                audio.currentTime = 0;  // Remettre à 0 pour pouvoir recommencer depuis le début
            }
            audio = new Audio(`${mediaUrl}/media/`+event.media.audio);
            audio.addEventListener('ended', () => {
                currentMedia = null;
            });
            audio.play();
        }
        currentMedia = event.media;
        return;
    }

    console.log("Event inconnu :", event);
}

function fermeMedia() {
    const imageContainer = document.getElementById('image-container');
    const imageElement = document.getElementById('image-to-display');
    const gameOverlay = document.getElementById('game-overlay');
    imageElement.src='';
    gameOverlay.classList.add('hidden');
    imageContainer.classList.add('hidden');
    currentMedia = null;
}

// -------------------------------------------------------------
// Déposer un objet de l'inventaire
// -------------------------------------------------------------
function deposeObjet(id) {
    fetch("/api/deposeObjet", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ object_id: id })
    })
    .then(r => r.json())
    .then(handleEvent)
    .catch(err => showMessage("Erreur action : " + err));
}

// -------------------------------------------------------------
// Inventaire
// -------------------------------------------------------------
function updateInventory(items) {
    const list = document.getElementById("inventory-list");
    list.innerHTML = ""; // Vide la liste avant d'ajouter les éléments

    items.forEach(i => {
        // Créer un conteneur pour chaque objet
        const itemContainer = document.createElement("div");
        itemContainer.classList.add("inventory-item");

        // Créer l'image de l'objet
        const im = document.createElement("img");
        im.src = `${mediaUrl}/objects/` + i.image;
        im.title = i.description;
        im.classList.add("inventory-item-image");

        // Ajouter un événement click sur l'image pour, par exemple, afficher l'objet ou une action
        im.addEventListener('click', () => {
            clickObject(i, currentMedia);
        });

        // Créer l'icône de suppression
        const deleteIcon = document.createElement("span");
        deleteIcon.textContent = "❌";
        deleteIcon.classList.add("delete-icon");
        deleteIcon.title = "Déposer";

        // Ajouter un événement click pour supprimer l'élément
        deleteIcon.addEventListener('click', (event) => {
            event.stopPropagation();  // Empêcher le clic sur l'icône de supprimer l'objet de déclencher l'événement click sur l'image
            deposeObjet(i.id);
            loadState();
        });

        // Ajouter l'image et l'icône de suppression au conteneur
        itemContainer.appendChild(im);
        itemContainer.appendChild(deleteIcon);

        // Ajouter le conteneur de l'objet à la liste
        list.appendChild(itemContainer);
    });

}

// -------------------------------------------------------------
// Messages
// -------------------------------------------------------------
function showMessage(text, type="normal", duree=5000, charicone="x", image=false) {
    const box = document.getElementById("message");
    const contenu = document.getElementById("contenu_message");
    const icone = document.getElementById("icone_message");
    const divImage = document.getElementById("image_message");
    const img = document.getElementById("img_image_message");
    const gameOverlay = document.getElementById('game-overlay');
    // Réinitialise au cas où un fade-out est en cours
    box.classList.remove("msghidden");
    contenu.textContent = text;

    // les messages normaux n'ont pas d'icone.
    if (type == "normal") {
        icone.classList.add("hidden");
    } else {
        icone.classList.remove("hidden");
        gameOverlay.classList.remove('hidden');
        icone.textContent = charicone;
    }

    if (image) {
        img.src = `${mediaUrl}/persos/`+image;
        divImage.classList.remove("hidden");
    } else {
        divImage.classList.add("hidden");
    }

    // Annule un timeout précédent.
    if (messageTimeout) {
        clearTimeout(messageTimeout);
    }

    // Si une durée est définie, lance le timeout d'effacement.
    if (duree>0) {
        messageTimeout = setTimeout(() => {
            box.classList.add("msghidden");
        }, duree);
    }
}

// Fonction pour gérer le clic sur le message
function handleMessageClick() {
    const box = document.getElementById("message");
    const gameOverlay = document.getElementById('game-overlay');
    box.classList.add("msghidden");
    if (messageTimeout) {
        clearTimeout(messageTimeout);
        messageTimeout = null;
    }
    
    if (currentPhrases) {
        currentPhraseIndex++;

        if (currentPhraseIndex < currentPhrases.length) {
            // Affiche la prochaine phrase
            showMessage(currentPhrases[currentPhraseIndex]["message"],"phrase",0,((currentPhraseIndex+1 == currentPhrases.length) ? "✖" : "⇒"),currentPhrases[currentPhraseIndex]["image"]);
        } else {
            gameOverlay.classList.add('hidden');
        }
    }
}

// Ajout du gestionnaire d'événement clic une seule fois lors de l'initialisation
document.getElementById("message").addEventListener("click", handleMessageClick);


// Debug
function updateCoordinates(event) {
    const image = document.getElementById('room-image');
    const coordinatesDiv = document.getElementById('coordinates');
    // Récupérer la position de l'image sur la page
    const rect = image.getBoundingClientRect();

    // Calculer les coordonnées par rapport à l'image
    const mouseX = event.clientX - rect.left;
    const mouseY = event.clientY - rect.top;

    // Mettre à jour le contenu du div des coordonnées
    coordinatesDiv.textContent = `X: ${mouseX.toFixed(2)}, Y: ${mouseY.toFixed(2)}`;

    // Positionner le div des coordonnées à côté du pointeur
    coordinatesDiv.style.left = `${event.clientX + 10}px`;
    coordinatesDiv.style.top = `${event.clientY + 10}px`;
}
document.getElementById('room-image').addEventListener('mousemove', updateCoordinates);