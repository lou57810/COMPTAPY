// static/js/journal/loader.js

export async function loadJournalEntries(hot, journalUrl, journalType) {
    let baseRowsCount = 0;

    /*if (!journalUrl || !journalType) {
        hot.alter("insert_row_below", hot.countRows());
        return { baseRowsCount };
    }
    */
    if (!hot || !journalUrl || !journalType) {
    return { baseRowsCount };
    }


    try {
        const response = await fetch(`${journalUrl}?type=${journalType}`);
        const json = await response.json();

        if (json.data && json.data.length > 0) {
            hot.loadData(json.data);
            baseRowsCount = hot.countRows();
        }

        hot.alter("insert_row_below", hot.countRows());  // lignes en lecture seule

        } catch (error) {
            console.error("Erreur lors du chargement du journal :", error);
        }

    return { baseRowsCount };
}

/*
export async function loadJournalEntries(hot, journalUrl, journalType) {
    let baseRowsCount = 0;

    if (!journalUrl || !journalType) {
        // Aucun journal existant → on ajoute une ligne vide
        hot.alter("insert_row_below", hot.countRows());
        return { baseRowsCount };
    }

    try {
        const response = await fetch(`${journalUrl}?type=${journalType}`);
        const json = await response.json();

        if (json.data && json.data.length > 0) {
            hot.loadData(json.data);
            baseRowsCount = hot.countRows(); // lignes en lecture seule
        } else {
            baseRowsCount = 0;
        }

        // Ajouter une ligne vide pour la saisie
        hot.alter("insert_row_below", hot.countRows());

    } catch (error) {
        console.error("Erreur lors du chargement du journal :", error);
    }

    return { baseRowsCount };
}
*/
