(function () {
    const zoneScene = document.getElementById("scene-courante");
    const zoneOnglets = document.getElementById("onglets-scenes");
    const zoneGraphe = document.getElementById("graphe-editeur");
    const message = document.getElementById("message");
    const { idFilm, estModifiable } = window.PROJETCINE;
    const donnees = JSON.parse(document.getElementById("donnees-film").textContent);

    let scenes = Array.isArray(donnees.scenes) && donnees.scenes.length
        ? donnees.scenes
        : [sceneVide()];
    let indexCourant = 0;

    function sceneVide() {
        return {
            info: {
                idScene: "",
                lieu: "",
                interieurExterieur: "",
                urlTexte: "",
                resume: "",
                personnages: [],
                voies: [],
                actes: [],
                estDebut: false,
                estFin: false
            },
            conditions: []
        };
    }

    function titreScene(scene, index) {
        const identifiant = scene.info && scene.info.idScene;
        return identifiant ? String(identifiant) : "Scène " + (index + 1);
    }

    function couleurNoeud(info) {
        if (info.estDebut && info.estFin) {
            return "gold";
        }
        if (info.estDebut) {
            return "palegreen";
        }
        if (info.estFin) {
            return "lightcoral";
        }
        return "lightblue";
    }

    function grapheDepuisScenes(liste) {
        const noeuds = [];
        const aretes = [];
        liste.forEach((scene) => {
            const info = scene.info || {};
            const id = info.idScene || "?";
            noeuds.push({
                id: id,
                couleur: couleurNoeud(info),
                surbrillance: false,
                resume: info.resume || ""
            });
            (scene.conditions || []).forEach((condition) => {
                if (condition.type !== "conditionSceneSuivante") {
                    return;
                }
                (condition.idScenesSuivantesPossibles || []).forEach((cible) => {
                    if (cible) {
                        aretes.push({ depart: id, arrivee: cible, surbrillance: false });
                    }
                });
            });
        });
        return { noeuds: noeuds, aretes: aretes };
    }

    function champTexte(label, valeur) {
        const enveloppe = document.createElement("label");
        enveloppe.className = "champ";
        enveloppe.textContent = label;
        const saisie = document.createElement("input");
        saisie.type = "text";
        saisie.value = valeur ?? "";
        enveloppe.appendChild(saisie);
        return { enveloppe, saisie };
    }

    function listeDynamique(valeurs, placeholder) {
        const bloc = document.createElement("div");
        bloc.className = "liste-dynamique";
        function ajouterLigne(valeur) {
            const ligne = document.createElement("div");
            ligne.className = "ligne-liste";
            const saisie = document.createElement("input");
            saisie.type = "text";
            saisie.value = valeur ?? "";
            saisie.placeholder = placeholder;
            saisie.addEventListener("input", surModification);
            const supprimer = document.createElement("button");
            supprimer.type = "button";
            supprimer.textContent = "Retirer";
            supprimer.addEventListener("click", () => {
                ligne.remove();
                surModification();
            });
            ligne.append(saisie, supprimer);
            bloc.appendChild(ligne);
        }
        const bouton = document.createElement("button");
        bouton.type = "button";
        bouton.textContent = "Ajouter";
        bouton.addEventListener("click", () => ajouterLigne(""));
        (valeurs || []).forEach(ajouterLigne);
        const enveloppe = document.createElement("div");
        enveloppe.className = "champ";
        enveloppe.append(bloc, bouton);
        enveloppe.collecter = () =>
            Array.from(bloc.querySelectorAll("input")).map((s) => s.value.trim()).filter(Boolean);
        return enveloppe;
    }

    function blocCondition(condition) {
        const carte = document.createElement("div");
        carte.className = "bloc-condition";
        const type = document.createElement("select");
        const option = document.createElement("option");
        option.value = "conditionSceneSuivante";
        option.textContent = "Scènes suivantes possibles";
        type.appendChild(option);
        type.value = condition.type || "conditionSceneSuivante";
        const suivantes = listeDynamique(condition.idScenesSuivantesPossibles || [], "idScene suivante");
        const retirer = document.createElement("button");
        retirer.type = "button";
        retirer.textContent = "Retirer la condition";
        retirer.addEventListener("click", () => {
            carte.remove();
            surModification();
        });
        carte.append(type, suivantes, retirer);
        carte.collecter = () => ({
            type: type.value,
            idScenesSuivantesPossibles: suivantes.collecter()
        });
        return carte;
    }

    function wrap(label, noeud) {
        const enveloppe = document.createElement("div");
        enveloppe.className = "champ";
        const nom = document.createElement("span");
        nom.textContent = label;
        enveloppe.append(nom, noeud);
        return enveloppe;
    }

    function construireFormulaire(scene) {
        const info = scene.info || {};
        const carte = document.createElement("article");
        carte.className = "carte-scene unique";
        const grille = document.createElement("div");
        grille.className = "grille";

        const idScene = champTexte("Identifiant", info.idScene);
        idScene.saisie.addEventListener("input", () => {
            surModification();
            rafraichirMenu();
        });
        const lieu = champTexte("Lieu", info.lieu);
        const interieur = champTexte("Intérieur / extérieur", info.interieurExterieur);
        lieu.saisie.addEventListener("input", surModification);
        interieur.saisie.addEventListener("input", surModification);

        const texte = document.createElement("label");
        texte.className = "champ champ-large";
        texte.textContent = "Texte de la scène";
        const zoneTexte = document.createElement("textarea");
        zoneTexte.rows = 6;
        zoneTexte.value = info.urlTexte || "";
        zoneTexte.addEventListener("input", surModification);
        texte.appendChild(zoneTexte);

        const resume = document.createElement("label");
        resume.className = "champ champ-large";
        resume.textContent = "Résumé (affiché au survol du graphe)";
        const zoneResume = document.createElement("textarea");
        zoneResume.rows = 2;
        zoneResume.value = info.resume || "";
        zoneResume.placeholder = "Une ou deux phrases pour identifier la scène";
        zoneResume.addEventListener("input", surModification);
        resume.appendChild(zoneResume);

        const personnages = listeDynamique(info.personnages, "personnage");
        const voies = listeDynamique(info.voies, "voie");
        const actes = listeDynamique(info.actes, "acte");

        const drapeaux = document.createElement("div");
        drapeaux.className = "drapeaux champ-large";
        const debut = document.createElement("label");
        const caseDebut = document.createElement("input");
        caseDebut.type = "checkbox";
        caseDebut.checked = Boolean(info.estDebut);
        caseDebut.addEventListener("change", surModification);
        debut.append(caseDebut, " Peut ouvrir un script");
        const fin = document.createElement("label");
        const caseFin = document.createElement("input");
        caseFin.type = "checkbox";
        caseFin.checked = Boolean(info.estFin);
        caseFin.addEventListener("change", surModification);
        fin.append(caseFin, " Peut clore un script");
        drapeaux.append(debut, fin);

        grille.append(
            idScene.enveloppe, lieu.enveloppe, interieur.enveloppe, texte, resume,
            wrap("Personnages", personnages),
            wrap("Voies", voies),
            wrap("Actes", actes),
            drapeaux
        );

        const conditions = document.createElement("div");
        conditions.className = "liste-conditions";
        (scene.conditions || []).forEach((c) => conditions.appendChild(blocCondition(c)));
        const ajouterCondition = document.createElement("button");
        ajouterCondition.type = "button";
        ajouterCondition.textContent = "Ajouter une condition";
        ajouterCondition.addEventListener("click", () => {
            conditions.appendChild(blocCondition({
                type: "conditionSceneSuivante",
                idScenesSuivantesPossibles: []
            }));
            surModification();
        });

        const supprimer = document.createElement("button");
        supprimer.type = "button";
        supprimer.textContent = "Supprimer cette scène";
        supprimer.addEventListener("click", supprimerSceneCourante);

        const actions = document.createElement("div");
        actions.className = "actions-scene";
        actions.appendChild(ajouterCondition);
        if (estModifiable) {
            actions.appendChild(supprimer);
        }
        carte.append(grille, conditions, actions);
        if (!estModifiable) {
            carte.querySelectorAll("input, textarea, select, button").forEach((el) => {
                el.disabled = true;
            });
        }

        carte.collecter = () => ({
            info: {
                idScene: idScene.saisie.value.trim(),
                lieu: lieu.saisie.value,
                interieurExterieur: interieur.saisie.value,
                urlTexte: zoneTexte.value,
                resume: zoneResume.value,
                personnages: personnages.collecter(),
                voies: voies.collecter(),
                actes: actes.collecter(),
                estDebut: caseDebut.checked,
                estFin: caseFin.checked
            },
            conditions: Array.from(conditions.children).map((c) => c.collecter())
        });
        return carte;
    }

    function capturerSceneCourante() {
        const formulaire = zoneScene.firstElementChild;
        if (formulaire && formulaire.collecter) {
            scenes[indexCourant] = formulaire.collecter();
        }
    }

    function afficherScene(index) {
        indexCourant = Math.max(0, Math.min(index, scenes.length - 1));
        zoneScene.replaceChildren(construireFormulaire(scenes[indexCourant]));
        rafraichirMenu();
        dessinerGraphe();
    }

    function rafraichirMenu() {
        zoneOnglets.replaceChildren();
        scenes.forEach((scene, index) => {
            const bouton = document.createElement("button");
            bouton.type = "button";
            bouton.className = "puce-scene" + (index === indexCourant ? " active" : "");
            bouton.textContent = titreScene(scene, index);
            bouton.addEventListener("click", () => {
                capturerSceneCourante();
                afficherScene(index);
            });
            zoneOnglets.appendChild(bouton);
        });
    }

    function dessinerGraphe() {
        if (typeof window.afficherGrapheDonnees !== "function") {
            return;
        }
        window.afficherGrapheDonnees(zoneGraphe, grapheDepuisScenes(scenes));
    }

    function surModification() {
        capturerSceneCourante();
        dessinerGraphe();
    }

    function ajouterScene() {
        capturerSceneCourante();
        scenes.push(sceneVide());
        afficherScene(scenes.length - 1);
    }

    function supprimerSceneCourante() {
        if (scenes.length === 1) {
            scenes[0] = sceneVide();
            afficherScene(0);
            return;
        }
        scenes.splice(indexCourant, 1);
        afficherScene(Math.min(indexCourant, scenes.length - 1));
    }

    function afficherMessage(texte, ok) {
        message.hidden = false;
        message.textContent = texte;
        message.className = "message " + (ok ? "ok" : "ko");
    }

    const boutonAjouter = document.getElementById("ajouter-scene");
    if (boutonAjouter) {
        boutonAjouter.addEventListener("click", ajouterScene);
    }

    const boutonEnregistrer = document.getElementById("enregistrer");
    if (boutonEnregistrer) {
        boutonEnregistrer.addEventListener("click", async () => {
            capturerSceneCourante();
            const reponse = await fetch("/films/" + encodeURIComponent(idFilm), {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ scenes: scenes })
            });
            if (reponse.ok) {
                afficherMessage("Film enregistré.", true);
            } else {
                const corps = await reponse.json().catch(() => ({ detail: reponse.statusText }));
                afficherMessage(corps.detail || "Enregistrement impossible.", false);
            }
        });
    }

    afficherScene(0);
})();
