Per far partire il progetto basta eseguire il file vqa_app.py che è un app FLask.

l'app consiste in un form con 4 campi (domanda, descrizione testuale, path dell'immagine, submit).
la pagina HTML riferita al form si trova in templates/vqa_form.html eseguendo una richiesta POST corretta
 il sistema restituisce un file .json con la struttura {"answer": risposta}.
 
Le cartelle bert_evaluation, grid_feats_vqa_master e vqa_bottom_up_evaluation riguardano le reti che fanno rispettivamente 
estrazione di classificazione della domanda, estrazione delle features dell'immagine e VQA (non sono da toccare).

All'inizio del file VQA_app.py vengono caricati tutti i pesi delle reti. 
A questo punto appena arriva una richiesta post corretta vengono estratte le features dall'immagine e salvate 
nella cartella /image_features. La funzione produceAnswer contenuta nel file generate_answer.py produce la risposta,
che tramite la funzione jsonify({'answer': answer}) viene ritornata.    
