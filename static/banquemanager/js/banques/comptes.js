async function fetchComptes(compte_actuel) {
    try {
        const response = await fetch('/banque/comptes/recuperer_comptes', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        if (response.ok) {
            const comptes = await response.json();

            popup = document.getElementById('popup');

            // Ajouter le titre
            h2 = document.createElement('h2');
            h2.innerText = 'Comptes Disponibles';

            popup.appendChild(h2);

            const comptesList = document.createElement('div');
            comptesList.id = 'comptes-list';
            comptes.forEach(compte => {
                if (compte.id === compte_actuel) {
                    return;
                }
                const compteButton = document.createElement('button');
                compteButton.innerText = compte.nom;
                compteButton.addEventListener('click', () => {
                    clearPopUp();
                    deployPopUpForm('transfert', compte_actuel, compte);
                })
                comptesList.appendChild(compteButton);
            });

            // Afficher la popup et l'overlay
            document.getElementById('popup').classList.add('active');
            document.getElementById('overlay').classList.add('active');
            document.getElementById('popup').appendChild(comptesList);
        } else {
            console.error('Error fetching comptes:', response.status);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function deployPopUpForm(action, compte, compte_dest = null) {
    form = document.createElement('form');
    form.id = 'form';
    form.method = 'POST';
    form.action = `/banque/${action}/${compte}`;

    let action_name = ""
    let destinataire = ""
    if (action === "depot"){
        action_name = "crédité"
    }else if (action === "retrait"){
        action_name = "débité"
    }else if (action === "transfert"){
        action_name = "transféré"
        destinataire = compte_dest
    }


    // add csrf token
    const csrf = document.createElement('input');
    csrf.type = 'hidden';
    csrf.name = 'csrfmiddlewaretoken';
    csrf.value = getCookie('csrftoken');
    form.appendChild(csrf);

    // add compte_dest input
    if (compte_dest !== null) {
        const compte_dest_input = document.createElement('input');
        compte_dest_input.type = 'hidden';
        compte_dest_input.name = 'compte_dest';
        compte_dest_input.value = compte_dest.id;
        form.appendChild(compte_dest_input);
    }

    // add montant input
    const montant = document.createElement('input');
    montant.type = 'number';
    montant.name = 'montant';
    montant.placeholder = 'Montant';
    montant.required = true;
    form.appendChild(montant);


    // add submit button
    const submit = document.createElement('button');
    submit.type = 'submit';
    submit.innerText = 'Valider';
    submit.addEventListener('click', (e) => {
        submitForm(e, action_name, destinataire);
    });
    form.appendChild(submit);

    document.getElementById('popup').appendChild(form);
    document.getElementById('popup').classList.add('active');
    document.getElementById('overlay').classList.add('active');

}

const submitForm = (e, action_name, destinataire) => {
    e.preventDefault();
    let form = e.target.closest('form');

    const data = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: data,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    }).then(response => {
        if (response.ok) {
            clearPopUp();
            if (action_name === "transféré"){
                showSuccessMessage(`Le montant de ${data.get('montant')}€ a été ${action_name} au compte ${destinataire.nom} avec succès`);
            }else
                showSuccessMessage(`Le montant de ${data.get('montant')}€ a été ${action_name} avec succès`);
        } else {
            showErrorMessage('Une erreur est survenue');
            console.error('Error:', response.status);
        }
    }).catch(error => {
        showErrorMessage('Une erreur est survenue');
        console.error('Error:', error);
    }).finally(() => {
        setTimeout(() => {
            location.reload();
        }, 2000);
    })

}

function showSuccessMessage(message) {
    const body = document.querySelector('body');
    const successMessage = document.createElement('p');
    successMessage.classList.add('success-message');
    successMessage.innerText = message;
    body.appendChild(successMessage);
}

function showErrorMessage(message) {
    const body = document.querySelector('body');
    const errorMessage = document.createElement('p');
    errorMessage.classList.add('error-message');
    errorMessage.innerText = message;
    body.appendChild(errorMessage);
}

function clearPopUp() {
    document.getElementById('popup').innerHTML = `<button class="close-btn" onclick="clearPopUp()"></button>`
    document.getElementById('popup').classList.remove('active');
    document.getElementById('overlay').classList.remove('active');
}

document.getElementById('overlay').addEventListener('click', () => {
    document.getElementById('popup').classList.remove('active');
    document.getElementById('overlay').classList.remove('active');
    clearPopUp();
});
