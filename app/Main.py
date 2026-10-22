import serial  # Libreria per comunicazione seriale
import matplotlib.pyplot as plt  # Libreria per creare grafici statici
import csv  # Libreria per lavorare con file CSV (Comma Separated Values)
import os  # Libreria per interagire con il sistema operativo (file, cartelle, ecc.)
import datetime  # Libreria per gestire date e orari
import tkinter as tk  # Libreria standard di Python per interfacce grafiche (GUI)
from tkinter import ttk  # Moduli di Tkinter con widget a tema (aspetto più moderno)
from tkinter import filedialog, messagebox  # Moduli per finestre di dialogo standard (file, messaggi)
import configparser  # Libreria per gestire file di configurazione (INI-style)
from serial.tools import list_ports  # Modulo per rilevare automaticamente le porte seriali disponibili
import sys  # Libreria per interazione con l'interprete Python (es: redirect output)
import tkinter.font as tkFont  # Modulo per gestire i font in Tkinter (incluso monospazio)
from ttkthemes import ThemedTk  # Libreria per applicare temi avanzati all'interfaccia Tkinter

################################################################################
# --- SEZIONE: FUNZIONI DI CONFIGURAZIONE DELL'APPLICAZIONE ---
# Responsabile del caricamento delle impostazioni da file (config.ini) all'avvio
# e del salvataggio delle modifiche apportate dall'utente durante l'esecuzione.
################################################################################

def carica_configurazione():
    """
    Carica le impostazioni dell'applicazione dal file 'config.ini'.

    Se il file di configurazione non viene trovato nella stessa directory dello script,
    la funzione utilizzerà dei valori predefiniti (hardcoded) e stamperà un avviso
    nella console di debug per informare l'utente.

    Ritorna:
        dict: Un dizionario Python contenente tutte le impostazioni caricate.
              Le chiavi del dizionario corrispondono ai nomi delle impostazioni,
              e i valori sono le impostazioni stesse (stringhe o numeri convertiti).
    """
    config = configparser.ConfigParser()  # Crea un oggetto parser per il file di configurazione (INI)
    config_file_path = "config.ini"  # Definisce il nome del file di configurazione che verrà cercato

    if os.path.exists(config_file_path):  # Verifica se il file di configurazione esiste nel percorso specificato
        config.read(config_file_path)  # Se il file esiste, lo legge e carica le impostazioni
    else:
        print(f"File di configurazione '{config_file_path}' non trovato. Verranno usati i valori predefiniti.")  # Avvisa l'utente se il file non esiste

    # --- VALORI PREDEFINITI (FALLBACK) ---
    # Questi valori verranno utilizzati se il file config.ini non esiste
    # o se alcune impostazioni specifiche non sono presenti nel file.
    default_porta_seriale = "COM3"
    default_baud_rate = "9600"
    default_nome_file_base = "dati_anodici"
    default_titolo_grafico = "Tensione Anodica Rilevata"
    default_asse_x_label = "Punto di Misura"
    default_asse_y_label = "Tensione Anodica (V)"
    default_tema_gui = "ubuntu"
    default_punti_misura = "13"  # Numero predefinito di punti di misura per il test
    default_timeout_seriale = "5"  # Timeout predefinito per la comunicazione seriale (secondi)

    # --- CARICA LE IMPOSTAZIONI DAL FILE CONFIG.INI (SE PRESENTI), ALTRIMENTI USA I VALORI PREDEFINITI ---
    # Il metodo `config.get()` tenta di leggere un valore dal file config.ini.
    # Se la sezione o la chiave specificata non esistono, viene utilizzato il valore di 'fallback' (predefinito).
    porta_seriale = config.get("Seriale", "porta_seriale", fallback=default_porta_seriale)
    baud_rate = config.get("Seriale", "baud_rate", fallback=default_baud_rate)
    timeout_seriale = config.get("Seriale", "timeout_seriale", fallback=default_timeout_seriale)  # Carica il timeout seriale, con fallback
    nome_file_base = config.get("Salvataggio", "nome_file_base", fallback=default_nome_file_base)
    titolo_grafico = config.get("Grafico", "titolo_grafico", fallback=default_titolo_grafico)
    asse_x_label = config.get("Grafico", "asse_x_label", fallback=default_asse_x_label)
    asse_y_label = config.get("Grafico", "asse_y_label", fallback=default_asse_y_label)
    tema_gui = config.get("AspettoGUI", "tema_gui", fallback=default_tema_gui)
    punti_misura = config.get("Test", "punti_misura", fallback=default_punti_misura)  # Carica il numero di punti misura, con fallback

    # --- CREA E RITORNA UN DIZIONARIO PYTHON CON LE IMPOSTAZIONI ---
    # Le impostazioni caricate (o predefinite) vengono organizzate in un dizionario Python
    # per essere facilmente accessibili e utilizzate nel resto dell'applicazione.
    return {
        "porta_seriale": porta_seriale,
        "baud_rate": baud_rate,
        "timeout_seriale": int(timeout_seriale),  # CONVERTE il timeout seriale in intero
        "nome_file_base": nome_file_base,
        "titolo_grafico": titolo_grafico,
        "asse_x_label": asse_x_label,
        "asse_y_label": asse_y_label,
        "tema_gui": tema_gui,
        "punti_misura": int(punti_misura),  # CONVERTE il numero di punti misura in intero
    }


def salva_configurazione(config_data):
    """
    Salva le impostazioni dell'applicazione nel file 'config.ini'.

    Questa funzione prende un dizionario Python (`config_data`) contenente le impostazioni
    e le scrive nel file di configurazione 'config.ini', organizzandole in sezioni
    e coppie chiave-valore.

    Args:
        config_data (dict): Un dizionario Python contenente le impostazioni da salvare.
                             Le chiavi del dizionario corrispondono ai nomi delle impostazioni,
                             e i valori sono le impostazioni stesse (stringhe o numeri).
    """
    config = configparser.ConfigParser()  # Crea un oggetto parser per scrivere nel file di configurazione

    # --- SEZIONE "Seriale" ---
    config.add_section("Seriale")  # Aggiunge la sezione [Seriale] al file config.ini
    config.set("Seriale", "porta_seriale", config_data["porta_seriale"])  # Imposta la porta seriale nella sezione [Seriale]
    config.set("Seriale", "baud_rate", config_data["baud_rate"])  # Imposta il baud rate nella sezione [Seriale]
    config.set("Seriale", "timeout_seriale", str(config_data["timeout_seriale"]))  # Salva il timeout seriale (CONVERTITO IN STRINGA)

    # --- SEZIONE "Salvataggio" ---
    config.add_section("Salvataggio")  # Aggiunge la sezione [Salvataggio] per le impostazioni relative al salvataggio dei dati
    config.set("Salvataggio", "nome_file_base", config_data["nome_file_base"])  # Imposta il nome base dei file di salvataggio

    # --- SEZIONE "Grafico" ---
    config.add_section("Grafico")  # Aggiunge la sezione [Grafico] per le impostazioni relative al grafico
    config.set("Grafico", "titolo_grafico", config_data["titolo_grafico"])  # Imposta il titolo del grafico
    config.set("Grafico", "asse_x_label", config_data["asse_x_label"])  # Imposta l'etichetta dell'asse X
    config.set("Grafico", "asse_y_label", config_data["asse_y_label"])  # Imposta l'etichetta dell'asse Y

    # --- SEZIONE "AspettoGUI" ---
    config.add_section("AspettoGUI")  # Aggiunge la sezione [AspettoGUI] per le impostazioni dell'aspetto grafico dell'interfaccia utente
    config.set("AspettoGUI", "tema_gui", config_data["tema_gui"])  # Imposta il tema grafico della GUI

    # --- SEZIONE "Test" ---
    config.add_section("Test")  # Aggiunge una sezione dedicata alle impostazioni specifiche del test
    config.set("Test", "punti_misura", str(config_data["punti_misura"]))  # Salva il numero di punti misura (CONVERTITO IN STRINGA)

    config_file_path = "config.ini"  # Riassegna il percorso del file di configurazione (coerenza)
    try:
        with open(config_file_path, 'w') as configfile:  # Apre il file config.ini in modalità scrittura ('w')
            config.write(configfile)  # Scrive l'oggetto ConfigParser (con tutte le sezioni e impostazioni) nel file
        print(f"Configurazione salvata in: {config_file_path}")  # Stampa un messaggio di conferma nella console di debug
    except Exception as e:  # Gestisce eventuali eccezioni che possono verificarsi durante il salvataggio del file
        print(f"Errore salvando configurazione: {e}")  # Stampa un messaggio di errore nella console di debug


################################################################################
# --- SEZIONE: FUNZIONI DI COMUNICAZIONE SERIALE CON ARDUINO ---
# Gestiscono l'inizializzazione della porta seriale, la lettura dei dati provenienti da Arduino
# e l'implementazione di un timeout per evitare blocchi indefiniti in caso di problemi di comunicazione.
################################################################################

ser = serial.Serial(timeout=None)  # Inizializza l'oggetto seriale. Timeout impostato inizialmente a None (verrà configurato dinamicamente).

def leggi_dati_seriale(config):
    """
    Legge i dati di tensione anodica dalla porta seriale.

    La funzione attende di ricevere il segnale di inizio test da Arduino ("Test in corso").
    Una volta ricevuto il segnale, legge un numero configurabile di valori di tensione anodica
    inviati da Arduino sulla seriale.

    Per migliorare la robustezza, è implementato un TIMEOUT SERIALE: se la lettura dei dati
    richiede troppo tempo (supera il timeout configurato), la funzione interrompe la lettura
    e ritorna un segnale di errore, evitando che il programma rimanga bloccato indefinitamente.

    Args:
        config (dict): Dizionario di configurazione contenente le impostazioni, incluso 'timeout_seriale'.

    Ritorna:
        tuple: Una tupla contenente due elementi:
            - list: Una lista di valori di tensione anodica letti dalla seriale (float).
                    Se si verifica un timeout o un errore durante la lettura, la lista sarà `None`.
            - str: Un timestamp formattato (AAAA-MM-GG_HH-MM-SS) che indica l'ora di inizio della lettura.
                    Se si verifica un timeout o un errore, il timestamp sarà `None`.
    """
    dati_anodici = []  # Inizializza una lista vuota per memorizzare i valori di tensione anodica letti
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Genera un timestamp univoco per questa sessione di lettura
    timeout_secondi = config["timeout_seriale"]  # Ottiene il valore di timeout seriale (in secondi) dalla configurazione
    ser.timeout = timeout_secondi  # **IMPOSTA IL TIMEOUT SERIALE DINAMICAMENTE** prima di iniziare la lettura

    #print(f"Timeout seriale impostato a: {timeout_secondi} secondi.")  # Stampa un messaggio di debug indicando il timeout impostato
    print("Premere il pulsante di test...")  # Istruisce l'utente su come avviare il test
    ser.reset_input_buffer()  # Pulisce il buffer di input seriale per scartare eventuali dati residui precedenti

    try:  # Utilizza un blocco try-except per gestire l'eccezione di timeout seriale
        while True:  # Loop principale in attesa di dati sulla porta seriale
            if ser.in_waiting > 0:  # Verifica se ci sono dati disponibili in ricezione sulla porta seriale
                linea_seriale = ser.readline().decode('utf-8').strip()  # Legge una linea di dati dalla seriale, la decodifica in UTF-8 e rimuove spazi/newline

                if "Test in corso" in linea_seriale:  # Ricerca la frase "Test in corso" nella linea seriale ricevuta (segnale di inizio test da Arduino)
                    print("Avvio ricezione dati...")  # Messaggio di debug per confermare l'inizio della ricezione dati
                    punti_misura_da_leggere = config["punti_misura"]  # Ottiene il numero di punti di misura da leggere dalla configurazione
                    while True:  # Loop interno per leggere i valori di tensione anodica (dopo aver ricevuto il segnale di inizio test)
                        if ser.in_waiting > 0:  # Verifica nuovamente se ci sono dati seriali disponibili (valori di tensione)
                            linea_valore = ser.readline().decode('utf-8').strip()  # Legge una linea di dati, decodifica e rimuove spazi/newline
                            if linea_valore:  # Verifica che la linea letta non sia vuota
                                try:
                                    valore_anodico = float(linea_valore.replace(',', '.'))  # Converte la linea letta in un valore numerico float (gestisce la virgola come separatore decimale)
                                    dati_anodici.append(valore_anodico)  # Aggiunge il valore di tensione alla lista `dati_anodici`
                                    if len(dati_anodici) == punti_misura_da_leggere:  # Controlla se sono stati ricevuti il numero configurato di valori
                                        print("Ricezione dati completata!")  # Messaggio di debug di completamento ricezione dati
                                        return dati_anodici, timestamp  # **RITORNA LA LISTA DEI DATI E IL TIMESTAMP** e termina la funzione
                                except ValueError:  # Gestisce l'eccezione che si verifica se la conversione a float fallisce (es: dato non numerico ricevuto)
                                    print(f"Valore non numerico ricevuto e ignorato: {linea_valore}")  # Messaggio di errore nella console di debug
                elif "Premere il pulsante su Arduino per iniziare." in linea_seriale: # Gestione di un'altra possibile risposta da Arduino
                    print("Arduino in attesa: Premere il pulsante su Arduino per iniziare il test.")  # Messaggio di debug se Arduino invia questo messaggio

    except serial.SerialTimeoutException:  # Cattura l'eccezione SerialTimeoutException se si verifica un timeout durante la lettura
        print(f"Errore: Timeout di {timeout_secondi} secondi raggiunto durante la lettura dalla porta seriale.")  # Messaggio di errore di timeout nella console di debug
        return None, None  # **RITORNA None, None per segnalare il timeout** a chi ha chiamato la funzione (es: avvia_test())


################################################################################
# --- SEZIONE: FUNZIONI DI CREAZIONE GRAFICO E SALVATAGGIO DATI ---
# Gestiscono la creazione del grafico con Matplotlib, la visualizzazione del grafico
# a schermo intero e il salvataggio dei dati (in formato CSV) e del grafico (in formato PNG) su disco.
################################################################################

def crea_grafico(dati, timestamp, config):
    """
    Crea un grafico della tensione anodica utilizzando Matplotlib, lo visualizza a schermo intero
    e salva sia i dati numerici (in formato CSV) che l'immagine del grafico (in formato PNG) su disco.

    I file vengono salvati all'interno di una cartella datata, creata automaticamente nella
    stessa directory dello script, per organizzare i risultati dei test in base alla data di esecuzione.

    Args:
        dati (list): Una lista di valori di tensione anodica (float) da utilizzare per creare il grafico.
        timestamp (str): Una stringa timestamp che rappresenta la data e l'ora della misurazione.
                         Utilizzato per generare nomi di file univoci per CSV e PNG.
        config (dict): Un dizionario di configurazione contenente impostazioni per il grafico
                         come titolo, etichette degli assi, ecc.
    """

    # --- GESTIONE DELLA CARTELLA DATATA PER I RISULTATI ---
    data_odierna = datetime.date.today().strftime("%d_%m_%Y")  # Ottiene la data odierna nel formato "gg_mm_aaaa"
    nome_cartella_data = f"Test effettuati in data {data_odierna}"  # Crea il nome della cartella basato sulla data odierna
    percorso_cartella_data = os.path.join(".", nome_cartella_data)  # Definisce il percorso completo della cartella (nella stessa directory dello script)
    os.makedirs(percorso_cartella_data, exist_ok=True)  # Crea la cartella se non esiste già. `exist_ok=True` evita errori se la cartella esiste.

    # --- SALVATAGGIO DEI DATI IN FORMATO CSV (COMMA SEPARATED VALUES) ---
    nome_file_csv = f"{config['nome_file_base']}_{timestamp}.csv"  # Crea un nome file CSV univoco usando il nome base e il timestamp
    percorso_file_csv = os.path.join(percorso_cartella_data, nome_file_csv)  # Definisce il percorso completo del file CSV

    # --- CREAZIONE DEL GRAFICO UTILIZZANDO MATPLOTLIB ---
    x_values = list(range(len(dati)))  # Crea una lista di valori per l'asse X (punti di misura: 0, 1, 2, ..., N-1)
    fig = plt.figure(figsize=(10, 6), dpi=100)  # Crea una nuova figura Matplotlib con dimensioni e DPI specificati
    plt.plot(x_values, dati, marker='o', linestyle='-')  # Crea il grafico a linee: asse X, valori dati, marcatori circolari, linea continua
    plt.title(config["titolo_grafico"])  # Imposta il titolo del grafico usando l'impostazione dal file di configurazione
    plt.xlabel(config["asse_x_label"])  # Imposta l'etichetta dell'asse X (presa dalla configurazione)
    plt.ylabel(config["asse_y_label"])  # Imposta l'etichetta dell'asse Y (presa dalla configurazione)
    plt.grid(True)  # Abilita la griglia sullo sfondo del grafico per migliorare la leggibilità
    plt.xticks(x_values)  # Imposta i ticks (etichette) sull'asse X in corrispondenza dei punti di misura
    plt.tight_layout()  # Regola automaticamente il layout del grafico per evitare sovrapposizioni di elementi (titoli, etichette, legenda, ecc.)

    # --- MODIFICA L'ETICHETTA DELLA FINESTRA DEL GRAFICO ---
    fig.canvas.manager.set_window_title("Tube Tester Graph")  # Imposta il titolo della finestra che contiene il grafico

    # --- MASSIMIZZAZIONE DELLA FINESTRA DEL GRAFICO A SCHERMO INTERO ---
    fig_manager = plt.get_current_fig_manager()  # Ottiene il gestore della finestra corrente del grafico
    fig_window = fig_manager.window  # Ottiene l'oggetto finestra Tkinter associato al grafico
    fig_window.wm_state('zoomed')  # Massimizza la finestra del grafico a schermo intero

    # --- SALVATAGGIO DEL GRAFICO COME FILE PNG NELLA CARTELLA DATATA ---
    nome_file_png = f"{config['nome_file_base']}_{timestamp}.png"  # Crea un nome file PNG univoco
    percorso_file_png = os.path.join(percorso_cartella_data, nome_file_png)  # Definisce il percorso completo del file PNG
    fig.savefig(percorso_file_png, dpi=100)  # Salva la figura del grafico come file PNG nella cartella datata, con DPI 100 per una buona risoluzione
    print(f"PNG Creato: {nome_file_png}")  # Messaggio di debug per confermare il salvataggio del PNG

    plt.show()  # Visualizza il grafico a schermo (blocca l'esecuzione del programma fino a quando la finestra del grafico non viene chiusa)

    # --- SALVATAGGIO DEI DATI NUMERICI IN FORMATO CSV ---
    try:
        with open(percorso_file_csv, 'w', newline='') as csvfile:  # Apre il file CSV in modalità scrittura ('w') e con gestione newline per compatibilità tra sistemi operativi
            csv_writer = csv.writer(csvfile)  # Crea un oggetto 'writer' CSV per scrivere i dati nel file
            csv_writer.writerow(['Punto Misura', 'Tensione Anodica (V)'])  # Scrive la riga di intestazione del file CSV (nomi delle colonne)
            for i, valore in enumerate(dati):  # Itera attraverso la lista dei dati di tensione anodica e i loro indici (punti di misura)
                csv_writer.writerow([i + 1, valore])  # Scrive una riga nel CSV per ogni punto di misura e valore di tensione (punto misura parte da 1)
        print(f"CSV Creato: {nome_file_csv}")  # Messaggio di debug per confermare il salvataggio del CSV
    except Exception as e:  # Gestisce eventuali eccezioni che possono verificarsi durante il salvataggio del file CSV
        print(f"Errore durante il salvataggio del file CSV: {e}")  # Messaggio di errore nella console di debug


################################################################################
# --- SEZIONE: FUNZIONI DI GESTIONE DELL'INTERFACCIA GRAFICA (GUI) ---
# Contiene le funzioni che gestiscono l'interazione con l'utente attraverso l'interfaccia grafica Tkinter,
# come l'avvio del test, il salvataggio della configurazione e la gestione degli eventi GUI.
################################################################################

def avvia_test():
    """
    Funzione principale per avviare la procedura di test.

    Questa funzione esegue in sequenza le seguenti operazioni:
        1. Ottiene le impostazioni di porta seriale e baud rate selezionate dall'utente nella GUI.
        2. Apre la porta seriale utilizzando le impostazioni selezionate.
        3. Chiama la funzione `leggi_dati_seriale()` per leggere i dati di tensione anodica da Arduino.
        4. Se la lettura dei dati ha successo, chiama `crea_grafico()` per generare il grafico e salvare i risultati.
        5. Gestisce eventuali errori che possono verificarsi durante la comunicazione seriale o il processo di test,
           mostrando messaggi di errore all'utente tramite finestre di dialogo (messagebox).
        6. In ogni caso (test completato con successo o errore), chiude la porta seriale per rilasciare la risorsa.
    """
    porta_seriale = porta_seriale_var.get()  # Ottiene la porta seriale selezionata dall'utente tramite la Combobox GUI
    baud_rate = baud_rate_var.get()  # Ottiene il baud rate selezionato dall'utente tramite la Combobox GUI
    config_data["porta_seriale"] = porta_seriale  # Aggiorna il dizionario di configurazione con la porta seriale selezionata dalla GUI (per il salvataggio successivo)
    config_data["baud_rate"] = baud_rate  # Aggiorna il dizionario di configurazione con il baud rate selezionato dalla GUI (per il salvataggio successivo)

    try:  # Utilizza un blocco try-except-finally per gestire le eccezioni e assicurare la chiusura della porta seriale
        ser.port = porta_seriale  # Imposta la porta seriale per l'oggetto seriale con la porta selezionata
        ser.baudrate = int(baud_rate)  # Imposta il baud rate per la comunicazione seriale, convertendo il valore da stringa a intero
        ser.open()  # **APRE LA PORTA SERIALE** - Inizia la comunicazione seriale

        print("Porta seriale aperta con successo.")  # Messaggio di debug per confermare l'apertura della porta seriale
        dati, timestamp = leggi_dati_seriale(config_data)  # **CHIAMATA ALLA FUNZIONE PER LEGGERE I DATI SERIALI**, passando il dizionario di configurazione
        if dati is None:  # **GESTIONE DEL CASO DI TIMEOUT SERIALE**: `leggi_dati_seriale()` ritorna `None, None` in caso di timeout
            messagebox.showerror("Errore Seriale", "Timeout durante la ricezione dei dati dalla porta seriale.\nVerificare la connessione e riprovare.")  # Mostra un messaggio di errore all'utente
            print("Test interrotto a causa di TIMEOUT SERIALE.")  # Messaggio di errore nella console di debug
            return  # **ESCE DALLA FUNZIONE `avvia_test()`** in caso di timeout, interrompendo la procedura di test
        crea_grafico(dati, timestamp, config_data)  # **CHIAMATA ALLA FUNZIONE PER CREARE IL GRAFICO E SALVARE I DATI**, se la lettura seriale ha avuto successo
        print("Test completato con successo.")  # Messaggio di debug di completamento del test

    except serial.SerialException as e:  # Cattura eccezioni specifiche per errori relativi alla porta seriale (es: porta non trovata, occupata, errore di accesso)
        messagebox.showerror("Errore Seriale", f"Impossibile aprire la porta seriale '{porta_seriale}':\n{e}")  # Mostra un messaggio di errore dettagliato all'utente
        print(f"Errore di comunicazione seriale: {e}")  # Stampa l'errore seriale nella console di debug
    except Exception as e:  # Cattura eccezioni generiche che possono verificarsi durante l'esecuzione del test (altri tipi di errori non specificatamente legati alla seriale)
        messagebox.showerror("Errore Generico", f"Si è verificato un errore durante l'esecuzione del test:\n{e}")  # Mostra un messaggio di errore generico all'utente
        print(f"Errore generico durante il test: {e}")  # Stampa l'errore generico nella console di debug
    finally:  # Clausola `finally`: il codice in questo blocco verrà eseguito SEMPRE, indipendentemente dal fatto che si siano verificate eccezioni o meno
        if ser.is_open:  # Verifica se la porta seriale è attualmente aperta
            ser.close()  # **CHIUDE LA PORTA SERIALE** - Rilascia la risorsa seriale, rendendola disponibile per altre applicazioni
            print("Porta seriale chiusa.")  # Messaggio di debug di conferma chiusura porta seriale
            print("------------------------------------------------------------")  # Linea di separazione nella console di debug per migliorare la leggibilità dell'output
            print("") # Riga vuota per spaziatura nella console


def salva_configurazione_gui():
    """
    Salva le impostazioni correnti della GUI nel file di configurazione 'config.ini'.

    Questa funzione viene chiamata quando l'utente preme il pulsante "Salva Configurazione" nella GUI.
    Preleva i valori correnti dei widget di input (porta seriale, baud rate, ecc.) e li salva nel file config.ini
    utilizzando la funzione `salva_configurazione()`.
    """
    config_data["porta_seriale"] = porta_seriale_var.get()  # Ottiene la porta seriale selezionata dalla Combobox GUI e la aggiorna nel dizionario config_data
    config_data["baud_rate"] = baud_rate_var.get()  # Ottiene il baud rate selezionato dalla Combobox GUI e lo aggiorna nel dizionario config_data
    config_data["timeout_seriale"] = int(timeout_seriale_var.get()) # Ottiene il valore di timeout seriale dall'Entry GUI e lo aggiorna
    salva_configurazione(config_data)  # **CHIAMATA ALLA FUNZIONE `salva_configurazione()`** per scrivere le impostazioni aggiornate nel file config.ini


################################################################################
# --- SEZIONE: CLASSE PER REDIREZIONE DELL'OUTPUT DI PRINT() ALLA CONSOLE GUI ---
# Implementa una classe `StdoutRedirector` per reindirizzare l'output standard (stdout)
# della funzione `print()` verso un widget di testo (Text) all'interno dell'interfaccia grafica (GUI).
# Questo permette di visualizzare i messaggi di debug e informativi direttamente nella finestra dell'applicazione.
################################################################################

class StdoutRedirector(object):
    """
    Classe per reindirizzare l'output della funzione `print()` verso un widget `Text` di Tkinter.

    Questa classe ridefinisce i metodi `write()` e `flush()` per intercettare l'output di `print()`
    e indirizzarlo verso un widget `Text` specificato, che funge da "console di debug" all'interno della GUI.
    """
    def __init__(self, text_widget):
        """
        Costruttore della classe `StdoutRedirector`.

        Args:
            text_widget (tk.Text): Il widget `Text` di Tkinter a cui si desidera reindirizzare l'output di `print()`.
        """
        self.text_widget = text_widget  # Memorizza un riferimento al widget `Text` a cui reindirizzare l'output

    def write(self, str_val):
        """
        Metodo chiamato automaticamente ogni volta che la funzione `print()` viene invocata.

        Questo metodo inserisce la stringa `str_val` (che rappresenta l'output di `print()`)
        alla fine del widget `Text`, consentendo di visualizzare il testo nella console di debug GUI.

        Args:
            str_val (str): La stringa di testo da scrivere nel widget `Text` (output di `print()`).
        """
        self.text_widget.configure(state=tk.NORMAL)  # Abilita temporaneamente la modifica del widget `Text` (se fosse disabilitato)
        self.text_widget.insert(tk.END, str_val)  # Inserisce il testo `str_val` alla fine del contenuto attuale del widget `Text`
        self.text_widget.see(tk.END)  # Effettua lo scroll automatico del widget `Text` per visualizzare sempre l'ultima riga aggiunta
        self.text_widget.configure(state=tk.DISABLED)  # Disabilita nuovamente la modifica del widget `Text` da parte dell'utente (solo visualizzazione)
        root.update_idletasks()  # Forza l'aggiornamento immediato della GUI per visualizzare subito il testo appena inserito

    def flush(self):
        """
        Metodo `flush()` (vuoto).

        Questo metodo è richiesto per compatibilità con il protocollo di `sys.stdout`,
        ma non è necessario implementare alcuna azione specifica per la re-direzione dell'output in questo contesto.
        """
        pass  # Metodo vuoto: non richiede alcuna azione specifica


################################################################################
# --- SEZIONE: INIZIALIZZAZIONE GUI E CICLO PRINCIPALE (MAINLOOP) ---
# Contiene il codice per l'inizializzazione dell'interfaccia grafica (GUI) utilizzando Tkinter,
# la creazione e il posizionamento dei widget (etichette, combobox, pulsanti, area di testo),
# il caricamento iniziale della configurazione e l'avvio del ciclo principale di Tkinter (mainloop)
# che gestisce l'interazione con l'utente e gli eventi della GUI.
################################################################################

# --- CARICA LA CONFIGURAZIONE DELL'APPLICAZIONE ALL'AVVIO ---
config_data = carica_configurazione()  # Chiama la funzione `carica_configurazione()` per leggere le impostazioni dal file config.ini all'avvio

# --- INIZIALIZZAZIONE DELLA FINESTRA PRINCIPALE DELLA GUI (TKINTER) ---
root = ThemedTk(theme=config_data["tema_gui"])  # Crea la finestra principale Tkinter utilizzando `ThemedTk` per applicare un tema grafico (preso dalla config)
root.title("Tube Tester")  # Imposta il titolo della finestra principale

# --- CODICE PER CENTRARE LA FINESTRA PRINCIPALE ALL'AVVIO SULLO SCHERMO ---
screen_width = root.winfo_screenwidth()  # Ottiene la larghezza dello schermo in pixel
screen_height = root.winfo_screenheight()  # Ottiene l'altezza dello schermo in pixel
window_width = 500  # Larghezza desiderata per la finestra dell'applicazione (pixel)
window_height = 370  # Altezza desiderata per la finestra dell'applicazione (pixel)
x_coordinate = int((screen_width / 2) - (window_width / 2))  # Calcola la coordinata X per centrare orizzontalmente
y_coordinate = int((screen_height / 2) - (window_height / 2))  # Calcola la coordinata Y per centrare verticalmente
root.geometry("+{}+{}".format(x_coordinate, y_coordinate))  # Imposta la geometria della finestra per centrarla sullo schermo
# --- FINE DEL CODICE PER CENTRARE LA FINESTRA ---

root.resizable(False, False)  # Impedisce all'utente di ridimensionare manualmente la finestra (larghezza e altezza fisse)
root.geometry(f"{window_width}x{window_height}")  # Imposta la dimensione iniziale fissa della finestra (larghezza x altezza)

# --- CONFIGURAZIONE DEL LAYOUT A GRIGLIA DELLA GUI ---
root.grid_columnconfigure(0, weight=0)  # Configura la colonna 0 della griglia: non si espande, mantiene la larghezza in base al contenuto
root.grid_columnconfigure(1, weight=1)  # Configura la colonna 1 della griglia: SI espande, occupa lo spazio extra disponibile nella finestra

# --- WIDGET: ETICHETTA "Porta Seriale" ---
porta_seriale_label = ttk.Label(root, text="Porta Seriale:", width=15)  # Crea un'etichetta statica con testo "Porta Seriale:" e larghezza fissa
porta_seriale_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")  # Posiziona l'etichetta nella griglia (riga 0, colonna 0), con padding e allineamento a destra

# --- WIDGET: MENU A TENDINA (COMBOBOX) PER SELEZIONE PORTA SERIALE ---
porte_disponibili = [port.device for port in list_ports.comports()]  # Rileva le porte seriali disponibili nel sistema operativo e crea una lista con i nomi delle porte
if not porte_disponibili:  # Se non vengono trovate porte seriali disponibili nel sistema...
    porte_disponibili = ["COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "COM10", "COM11", "COM12"]  # ...popola la lista con porte COM predefinite (Windows)

porta_seriale_var = tk.StringVar(root)  # Crea una variabile di stringa Tkinter per memorizzare la porta seriale selezionata
porta_seriale_var.set(  # Imposta il valore iniziale della variabile `porta_seriale_var`
    config_data["porta_seriale"] if config_data["porta_seriale"] in porte_disponibili  # Se la porta salvata in config.ini è disponibile, usa quella
    else (porte_disponibili[0] if porte_disponibili else "Nessuna porta trovata")  # Altrimenti usa la prima porta disponibile o "Nessuna porta trovata"
)

porta_seriale_dropdown = ttk.Combobox(  # Crea un widget Combobox (menu a tendina) per la selezione della porta seriale
    root,
    textvariable=porta_seriale_var,  # Associa la Combobox alla variabile `porta_seriale_var` (il valore selezionato verrà memorizzato qui)
    values=porte_disponibili,  # Popola la Combobox con la lista delle porte seriali disponibili
    width=17,  # Imposta una larghezza fissa per la Combobox
    state='readonly'
)
porta_seriale_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")  # Posiziona la Combobox nella griglia (riga 0, colonna 1), con padding e espansione orizzontale

# --- WIDGET: ETICHETTA "Baud Rate" ---
baud_rate_label = ttk.Label(root, text="Baud Rate:", width=15)  # Crea l'etichetta "Baud Rate:" con larghezza fissa
baud_rate_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")  # Posiziona l'etichetta nella griglia (riga 1, colonna 0), con padding e allineamento a destra

# --- WIDGET: MENU A TENDINA (COMBOBOX) PER SELEZIONE BAUD RATE ---
baud_rates = ["9600", "115200", "57600", "38400"]  # Definisce una lista di baud rate predefiniti e comuni
baud_rate_var = tk.StringVar(root)  # Crea una variabile di stringa Tkinter per memorizzare il baud rate selezionato
baud_rate_var.set(config_data["baud_rate"])  # Imposta il valore iniziale della variabile `baud_rate_var` con il valore letto dalla configurazione

baud_rate_dropdown = ttk.Combobox(  # Crea un widget Combobox per la selezione del baud rate
    root,
    textvariable=baud_rate_var,  # Associa la Combobox alla variabile `baud_rate_var`
    values=baud_rates,  # Popola la Combobox con la lista dei baud rate predefiniti
    width=17,  # Imposta una larghezza fissa per la Combobox
    state='readonly'
)
baud_rate_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="ew")  # Posiziona la Combobox nella griglia (riga 1, colonna 1), con padding e espansione orizzontale

# --- WIDGET: ETICHETTA "Timeout (s)" PER TIMEOUT SERIALE ---
timeout_seriale_label = ttk.Label(root, text="Timeout (s):", width=15)  # Crea l'etichetta "Timeout (s):" con larghezza fissa
timeout_seriale_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")  # Posiziona l'etichetta nella griglia (riga 2, colonna 0), con padding e allineamento a destra

# --- WIDGET: CAMPO DI INGRESSO (ENTRY) PER IL TIMEOUT SERIALE ---
timeout_seriale_var = tk.StringVar(root)  # Crea una variabile di stringa Tkinter per memorizzare il valore del timeout seriale
timeout_seriale_var.set(config_data["timeout_seriale"])  # Imposta il valore iniziale del campo di input con il valore letto dalla configurazione

timeout_seriale_entry = ttk.Entry(root, textvariable=timeout_seriale_var, width=19)  # Crea un widget Entry (campo di input) per inserire il timeout seriale
timeout_seriale_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")  # Posiziona il campo di input nella griglia (riga 2, colonna 1), con padding e espansione orizzontale

# --- WIDGET: PULSANTE "Salva Configurazione" ---
salva_config_button = ttk.Button(root, text="Salva Configurazione", command=salva_configurazione_gui)  # Crea un pulsante con testo "Salva Configurazione" e associa la funzione `salva_configurazione_gui` al click
salva_config_button.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew", padx=(5, 5))  # Posiziona il pulsante nella griglia (riga 4, si estende su 2 colonne), con padding e espansione orizzontale

# --- WIDGET: AREA DI TESTO (TEXT) PER LA CONSOLE DI DEBUG ---
debug_console = tk.Text(root, height=10, bg="black", fg="orange", wrap=tk.WORD, state=tk.DISABLED)  # Crea un widget Text per la console di debug: altezza 10 righe, sfondo nero, testo arancione, word wrap attivo, **DISABILITATO per la modifica diretta**
debug_console.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="we")  # Posiziona l'area di testo nella griglia (riga 6, si estende su 2 colonne), con padding e espansione orizzontale

# --- CONFIGURAZIONE DEL FONT MONOSPAZIO PER LA CONSOLE DI DEBUG ---
debug_font = tkFont.Font(family="Courier New", size=10)  # Crea un oggetto Font monospazio (Courier New, dimensione 10)
debug_console.config(font=debug_font)  # Applica il font monospazio al widget Text della console di debug

# --- WIDGET: PULSANTE "Avvia Test" ---
avvia_button = ttk.Button(root, text="Avvia Test", command=avvia_test)  # Crea un pulsante con testo "Avvia Test" e associa la funzione `avvia_test` al click
avvia_button.grid(row=7, column=0, columnspan=2, pady=5, sticky="ew", padx=(5, 5))  # Posiziona il pulsante nella griglia (riga 7, si estende su 2 colonne), con padding e espansione orizzontale

# --- REDIREZIONE DELL'OUTPUT STANDARD (STDOUT) VERSO LA CONSOLE DI DEBUG GUI ---
stdout_redirector = StdoutRedirector(debug_console)  # Crea un'istanza della classe `StdoutRedirector`, associandola al widget `debug_console`
sys.stdout = stdout_redirector  # **REINDIRIZZA L'OUTPUT STANDARD (STDOUT) del sistema verso l'oggetto `stdout_redirector`**.  Ora, tutte le chiamate a `print()` nel codice Python verranno visualizzate nel widget `debug_console` della GUI.


################################################################################
# --- AVVIO DEL CICLO PRINCIPALE DI TKINTER (MAIN LOOP) ---
# Questo ciclo continuo è responsabile della gestione degli eventi dell'interfaccia grafica,
# come i click sui pulsanti, l'input dell'utente, il ridisegno della finestra, ecc.
# L'applicazione rimane in esecuzione all'interno di questo ciclo fino a quando l'utente chiude la finestra principale.
################################################################################

if __name__ == "__main__":  # Verifica se lo script viene eseguito direttamente (non importato come modulo)
    root.mainloop()  # **AVVIA IL CICLO PRINCIPALE DI TKINTER**. La GUI diventa interattiva e rimane in attesa di eventi.
    ser.close()  # **CHIUDE LA PORTA SERIALE** quando il ciclo `mainloop()` termina (ovvero quando la finestra GUI viene chiusa).  Assicura il rilascio della porta seriale.