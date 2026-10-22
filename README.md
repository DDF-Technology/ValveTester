# ValveTester

Progetto consolidato per un tester di valvole termoioniche a bassa tensione. Il sistema comprende:

- firmware Arduino che esegue 13 misure variando il PWM di griglia;
- applicazione desktop Python/Tkinter che acquisisce i valori dalla porta seriale;
- file elettronici, meccanici e materiali di riferimento del progetto originale.

## Struttura

```text
ValveTester/
|-- firmware/Arduino_Code/   Sketch Arduino originale
|-- app/                     Interfaccia Python e configurazione
|-- hardware/electronics/    Schema, Gerber e progetto PCB
|-- hardware/enclosure/      Modelli 3D del contenitore
|-- hardware/images/         Immagini di riferimento
`-- docs/                    Foglio di test e documentazione originale
```

## Funzionamento

Il firmware configura la seriale a 9600 baud, usa il pin PWM 3, il pulsante sul pin digitale 12 e l'ingresso analogico A5. Alla pressione del pulsante applica in sequenza 13 livelli PWM, attende 100 ms per ciascun livello, legge A5 e invia 13 tensioni sulla seriale. Il separatore decimale trasmesso e' la virgola.

L'applicazione apre la porta selezionata, attende la riga `Test in corso`, legge il numero di misure configurato (13 per impostazione predefinita), converte i valori in `float` e genera:

- un file CSV con punto di misura e tensione anodica;
- un grafico PNG;
- una cartella risultati denominata con la data del test.

## Avvio dell'applicazione

Da PowerShell:

```powershell
cd app
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python Main.py
```

L'applicazione cerca `config.ini` nella directory corrente, quindi va avviata dalla cartella `app`. Selezionare la porta COM collegata ad Arduino e mantenere il baud rate a 9600 per il firmware incluso.

## Firmware

Aprire `firmware/Arduino_Code/Arduino_Code.ino` con Arduino IDE e caricarlo su una scheda compatibile con i pin usati dallo sketch. La tabella PWM inclusa nel codice rappresenta punti di griglia da circa -3 V a +3 V.

## Creazione dell'eseguibile Windows

La configurazione PyInstaller originale e' in `app/Main.spec`:

```powershell
cd app
python -m pip install -r requirements-dev.txt
pyinstaller Main.spec
```

L'eseguibile viene generato in `app/dist`. `config.ini` resta un file esterno e deve essere distribuito accanto all'eseguibile, poiche' la configurazione originale non lo incorpora nel bundle.

## Verifiche e limiti noti

- Firmware e GUI concordano su 9600 baud e 13 valori per test.
- La GUI accetta sia il punto sia la virgola come separatore decimale.
- Il firmware invia `Premere il pulsante per iniziare.`, mentre la GUI controlla una variante testuale diversa; questo non impedisce l'acquisizione, che inizia sul marker `Test in corso`.
- La routine seriale controlla `in_waiting` prima di `readline()`: il timeout configurato non interrompe l'attesa quando non arrivano byte e la GUI puo' restare bloccata durante l'acquisizione.
- Il test completo richiede hardware reale; la verifica locale copre integrita' dei file, sintassi Python e coerenza statica del protocollo.

## Provenienza

I sorgenti applicativi e gli asset sono stati importati senza modificarne il contenuto dalle due cartelle fornite. Gli artefatti generati presenti nella cartella `build` originale non sono stati importati: sono riproducibili tramite PyInstaller e vengono esclusi dal controllo versione.

Non e' presente una licenza esplicita nei materiali originali. Prima di ridistribuire codice, PCB o modelli 3D, verificare i relativi diritti d'uso.
