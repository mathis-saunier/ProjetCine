(function () {
    const LARGEUR_NOEUD = 72;
    const HAUTEUR_NOEUD = 36;
    const PAS_X = 130;
    const PAS_Y = 70;
    const MARGE = 36;

    function couches(noeuds, aretes) {
        const identifiants = noeuds.map((n) => String(n.id));
        const suivants = new Map(identifiants.map((id) => [id, []]));
        const degreEntrant = new Map(identifiants.map((id) => [id, 0]));
        aretes.forEach((arete) => {
            const depart = String(arete.depart);
            const arrivee = String(arete.arrivee);
            if (!suivants.has(depart) || !degreEntrant.has(arrivee)) {
                return;
            }
            suivants.get(depart).push(arrivee);
            degreEntrant.set(arrivee, degreEntrant.get(arrivee) + 1);
        });
        const file = identifiants.filter((id) => degreEntrant.get(id) === 0);
        const niveau = new Map();
        file.forEach((id) => niveau.set(id, 0));
        let lecture = 0;
        while (lecture < file.length) {
            const courant = file[lecture];
            lecture += 1;
            suivants.get(courant).forEach((voisin) => {
                niveau.set(voisin, Math.max(niveau.get(voisin) || 0, niveau.get(courant) + 1));
                degreEntrant.set(voisin, degreEntrant.get(voisin) - 1);
                if (degreEntrant.get(voisin) === 0) {
                    file.push(voisin);
                }
            });
        }
        identifiants.forEach((id) => {
            if (!niveau.has(id)) {
                niveau.set(id, 0);
            }
        });
        const parCouche = new Map();
        identifiants.forEach((id) => {
            const n = niveau.get(id);
            if (!parCouche.has(n)) {
                parCouche.set(n, []);
            }
            parCouche.get(n).push(id);
        });
        return { niveau, parCouche };
    }

    function positions(noeuds, aretes) {
        const { niveau, parCouche } = couches(noeuds, aretes);
        const coords = new Map();
        parCouche.forEach((ids, n) => {
            ids.forEach((id, rang) => {
                coords.set(id, {
                    x: MARGE + n * PAS_X,
                    y: MARGE + rang * PAS_Y
                });
            });
        });
        const maxX = Math.max(0, ...Array.from(coords.values()).map((p) => p.x));
        const maxY = Math.max(0, ...Array.from(coords.values()).map((p) => p.y));
        return {
            coords,
            largeur: maxX + LARGEUR_NOEUD + MARGE,
            hauteur: maxY + HAUTEUR_NOEUD + MARGE
        };
    }

    function svgEl(nom, attrs) {
        const el = document.createElementNS("http://www.w3.org/2000/svg", nom);
        Object.entries(attrs).forEach(([cle, valeur]) => el.setAttribute(cle, valeur));
        return el;
    }

    function elementInfobulle() {
        let bulle = document.getElementById("infobulle-graphe");
        if (!bulle) {
            bulle = document.createElement("div");
            bulle.id = "infobulle-graphe";
            bulle.className = "infobulle-graphe";
            bulle.hidden = true;
            document.body.appendChild(bulle);
        }
        return bulle;
    }

    function brancherInfobulle(groupe, identifiant, resume) {
        const bulle = elementInfobulle();
        function afficher(evenement) {
            const titre = document.createElement("strong");
            titre.textContent = "Scène " + identifiant;
            const texte = document.createElement("p");
            texte.textContent = resume.trim() || "Aucun résumé pour cette scène.";
            bulle.replaceChildren(titre, texte);
            bulle.hidden = false;
            deplacer(evenement);
        }
        function deplacer(evenement) {
            bulle.style.left = (evenement.clientX + 14) + "px";
            bulle.style.top = (evenement.clientY + 14) + "px";
        }
        function cacher() {
            bulle.hidden = true;
        }
        groupe.addEventListener("mouseenter", afficher);
        groupe.addEventListener("mousemove", deplacer);
        groupe.addEventListener("mouseleave", cacher);
    }

    window.afficherGrapheDonnees = function (conteneur, graphe) {
        if (!conteneur) {
            return;
        }
        const noeuds = (graphe && graphe.noeuds) || [];
        if (!noeuds.length) {
            conteneur.innerHTML = "<p class=\"muet\">Ajoutez des scènes pour voir le graphe.</p>";
            return;
        }
        const aretes = (graphe && graphe.aretes) || [];
        const { coords, largeur, hauteur } = positions(noeuds, aretes);
        const svg = svgEl("svg", {
            viewBox: "0 0 " + largeur + " " + hauteur,
            width: String(largeur),
            height: String(hauteur),
            role: "img",
            "aria-label": "Graphe des scènes"
        });
        const defs = svgEl("defs", {});
        const marqueur = svgEl("marker", {
            id: "fleche",
            viewBox: "0 0 10 10",
            refX: "10",
            refY: "5",
            markerWidth: "7",
            markerHeight: "7",
            orient: "auto-start-reverse"
        });
        marqueur.appendChild(svgEl("path", { d: "M 0 0 L 10 5 L 0 10 z", fill: "#555" }));
        const marqueurOr = svgEl("marker", {
            id: "fleche-or",
            viewBox: "0 0 10 10",
            refX: "10",
            refY: "5",
            markerWidth: "7",
            markerHeight: "7",
            orient: "auto-start-reverse"
        });
        marqueurOr.appendChild(svgEl("path", { d: "M 0 0 L 10 5 L 0 10 z", fill: "#b8860b" }));
        defs.append(marqueur, marqueurOr);
        svg.appendChild(defs);

        aretes.forEach((arete) => {
            const a = coords.get(String(arete.depart));
            const b = coords.get(String(arete.arrivee));
            if (!a || !b) {
                return;
            }
            const x1 = a.x + LARGEUR_NOEUD;
            const y1 = a.y + HAUTEUR_NOEUD / 2;
            const x2 = b.x;
            const y2 = b.y + HAUTEUR_NOEUD / 2;
            svg.appendChild(svgEl("path", {
                d: "M " + x1 + " " + y1 + " C " + (x1 + 36) + " " + y1 + ", " + (x2 - 36) + " " + y2 + ", " + x2 + " " + y2,
                fill: "none",
                stroke: arete.surbrillance ? "#b8860b" : "#777",
                "stroke-width": arete.surbrillance ? "3" : "1.4",
                "marker-end": arete.surbrillance ? "url(#fleche-or)" : "url(#fleche)"
            }));
        });

        noeuds.forEach((noeud) => {
            const id = String(noeud.id);
            const p = coords.get(id);
            if (!p) {
                return;
            }
            const groupe = svgEl("g", { class: "noeud-graphe", style: "cursor: pointer;" });
            groupe.appendChild(svgEl("rect", {
                x: String(p.x),
                y: String(p.y),
                width: String(LARGEUR_NOEUD),
                height: String(HAUTEUR_NOEUD),
                rx: "6",
                fill: noeud.couleur || "lightblue",
                stroke: noeud.surbrillance ? "#b8860b" : "#333",
                "stroke-width": noeud.surbrillance ? "2.4" : "1"
            }));
            const texte = svgEl("text", {
                x: String(p.x + LARGEUR_NOEUD / 2),
                y: String(p.y + HAUTEUR_NOEUD / 2 + 4),
                "text-anchor": "middle",
                fill: "#1a1408",
                "font-size": "13",
                "font-family": "Helvetica, Arial, sans-serif"
            });
            texte.textContent = id;
            groupe.appendChild(texte);
            brancherInfobulle(groupe, id, noeud.resume || "");
            svg.appendChild(groupe);
        });

        conteneur.replaceChildren(svg);
    };

    function graphesDeGeneration() {
        const source = document.getElementById("donnees-graphes");
        const conteneur = document.getElementById("graphe");
        if (!source || !conteneur) {
            return;
        }
        const donnees = JSON.parse(source.textContent);
        let vue = "superpose";
        let indexScript = 0;

        function sourceCourante() {
            if (vue === "complet") {
                return donnees.complet;
            }
            const script = (donnees.scripts || [])[indexScript] || {};
            return vue === "tirage" ? script.grapheTirage : script.grapheSuperpose;
        }

        function rafraichir() {
            window.afficherGrapheDonnees(conteneur, sourceCourante());
        }

        document.querySelectorAll(".onglet").forEach((bouton) => {
            bouton.addEventListener("click", () => {
                document.querySelectorAll(".onglet").forEach((b) => b.classList.remove("actif"));
                bouton.classList.add("actif");
                vue = bouton.dataset.vue;
                rafraichir();
            });
        });

        const selecteur = document.getElementById("choix-script");
        if (selecteur) {
            selecteur.addEventListener("change", () => {
                indexScript = Number(selecteur.value) || 0;
                rafraichir();
            });
        }

        rafraichir();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", graphesDeGeneration);
    } else {
        graphesDeGeneration();
    }
})();
