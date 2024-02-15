class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
    
    # Istanzio la classe con il nome del file
    def __init__ (self, name):
        
        self.name = name
        
    def get_data(self):
        
        # Provo ad aprire e leggere il file
        try:
            file = open(self.name, "r")
            file.readline()
            file.close()
        # Se il file non esiste o non è apribile alzo un'eccezione
        except:
            raise ExamException('Errore: file non apribile')
        
        # Creo una lista vuota dove inserirò le liste con date e passeggeri
        data = []
        # Apro il file e creo lines che è una lista contenente le righe del file esclusa la prima
        f = open(self.name)
        lines = f.readlines()[1:]
        # Chiudo il file
        f.close()
        
        # Inizializzo la data precedente a None
        prev_year = None
        prev_month = None
        # Itero sulle righe del file
        for line in lines:
            
            # Separo la riga e mi creo una lista dove la data
            # è nella posizione 0 e i passeggeri nella posizione 1
            elements = line.split(',')
        
            # Inizializzo la data corrente alla data della riga considerata e tolgo eventuali spazi
            curr_date = elements[0].strip()
            
            # Controllo che la data sia lunga sette, altrimenti vado alla riga successiva
            if len(curr_date) != 7:
                continue
            
            # Provo a dividere la data in mese ed anno separandole con il carattere '-'
            try:
                date_separated = curr_date.split('-')
                curr_year = date_separated[0]
                curr_month = date_separated[1]
            # Se non riesco a dividere la data in anno e mese e se non c'è '-' vado alla riga successiva
            except:
                continue
            
            # Controllo che l'anno sia composto da quattro cifre e il mese da due
            if len(curr_year) != 4 or len(curr_month) != 2:
                continue
            
            # Provo a trasformare l'anno e il mese in  interi
            try:
                curr_year = int(curr_year)
                curr_month = int(curr_month)
            # Se non riesco a trasformarli vado alla riga successiva
            except:
                continue
                      
            # Se il mese non è compreso tra 1 e 12 vado alla riga successiva
            if curr_month < 1 or curr_month > 12:
                continue
            
            # Se la lista non è ordinata o ci sono duplicati alzo eccezione
            
            # Se non è la prima iterazione eseguo il ciclo
            if prev_year is not None and prev_month is not None:
                # Se l'anno corrente è minore dell'anno precedente
                if curr_year < prev_year:
                    raise ExamException('Errore: le date non sono ordinate')
                # Se l'anno corrente è uguale all'anno precedente e il mese corrente è minore del mese precedente
                if curr_year == prev_year and curr_month <= prev_month:
                    raise ExamException('Errore: le date non sono ordinate')
                # Se c'è un duplicato
                if curr_year == prev_year and curr_month == prev_month:
                    raise ExamException('Errore: ci sono duplicati')
            
            # Mi salvo i valori per il confronto all'iterazione successiva
            prev_year = curr_year
            prev_month = curr_month

            # Mi creo una lista vuota dove andrò ad aggiungere la data e i passeggeri
            # Si crea una lista ad ogni iterazione, ossia per ogni riga del file
            new_line = []
            
            # Itero sugli elementi della riga divisa
            # Mi tengo sia l'indice che il valore di ciascun elemento
            for index, element in enumerate(elements):
                
                # Elimino eventuali spazi
                value = element.strip()
                
                # Se index è maggiore di uno lo ignoro, non mi interessa
                # lavoro solo con i primi due indici (data e passeggeri)
                if index <= 1:
                    
                    # Se è l'indice della seconda posizione (passeggeri) 
                    # mi assicuro che il numero possa essere convertito a intero
                    if index == 1:
                        try:
                            value = int(value)
                            # Se i passeggeri sono negativi o 0 salto la riga
                            if value <= 0:
                                continue
                        # Se non converte a int salto la riga
                        except:
                            continue
                    
                    # Aggiungo i valori alla lista new_line
                    new_line.append(value)
                
            # Aggiungo alla lista data la lista new_line solo se newline ha due elementi (data e passeggeri)
            if len(new_line) == 2:
                data.append(new_line)
        
        return data
        
def compute_increments (time_series, first_year, last_year):
    
    if time_series is None or time_series == []:
        raise ExamException('Errore: la lista in input è vuota')
    
    if type(first_year) != str or type(last_year) != str:
        raise ExamException('Errore: i due anni devono essere stringhe')
    
    # Provo a convertire le due stringhe in input a interi
    try:
        first_year = int(first_year)
        last_year = int(last_year)
    except:
        raise ExamException('Errore: la stringa degli anni non è composta da cifre')
    
    if first_year == last_year:
        raise ExamException('Errore: i due anni sono uguali')
    
    # Creo una lista 'years_psg' dove le date sono spezzate per anno, e il secondo elemento sono i passeggeri
    years_psg = []
    
    # Itero sulle liste della lista time_series
    for line in time_series:
        
        # Prendo il primo elemento della lista, ossia la data
        first_el = line[0]
        # Divido la data su '-'
        tmp = first_el.split('-')
        # Prendo l'anno e i passeggeri convertiti a interi
        year = int(tmp[0].strip())
        psg = int(line[1])
        # Aggiungo la lista [anno, passeggeri] alla lista di liste years_psg
        years_psg.append([year,psg])
        
    # Controllo che il primo e l'ultimo anno siano presenti nella lista years_psg
    check_f = 0
    check_l = 0
    for line in years_psg:
        # Se gli anni sono presenti allora setto check_f e check_l a 1
        if line[0] == first_year:
            check_f = 1
        if line[0] == last_year:
            check_l = 1
    
    # Eseguo l'if se uno dei due anni non è presente
    if check_f == 0 or check_l == 0:
        # Se i due anni sono consecutivi ritorno una lista vuota
        if last_year - first_year == 1:
            return []
        # Se i due anni non sono consecutivi ritorno un errore
        else:
            raise ExamException('Errore: uno dei due anni non è presente')
    
    # Se first_year è maggiore di last_year scambio i due valori
    if first_year > last_year:
        first_year, last_year = last_year, first_year
    
    # Creo un dizionario vuoto
    incr = {}
    
    # Inizializzo la media precedente e un contatore a 0
    mean_prev = 0
    c = 0
    
    # Itero sugli anni
    for i in range(first_year, last_year + 1):
        
        # Conto i mesi e sommo i passeggeri per l'anno i
        counter = 0
        sum_i = 0
        # Itero sulla lista con anni e passeggeri
        for line in years_psg:
            # Se l'anno coincide con i, incremento il contatore e sommo i passeggeri
            if line[0] == i:
                counter += 1
                sum_i += line[1]
        
        # Se l'anno è presente posso calcolare la media dei passeggeri per l'anno
        if counter != 0:
            mean_i = sum_i / counter
        # Se l'anno non è presente aggiungo 1 alla variabile c
        # mi serve per tenere conto per quanti anni consecutivi non ho valori
        # vado direttamente all'iterazione successiva
        else:
            c += 1
            continue
        
        # Eseguo l'if se non è la prima iterazione
        if i != first_year:
            # Faccio 'i - c - 1' per ottenere l'ultimo anno utile per cui ho valori
            incr[f'{i - c - 1}-{i}'] = mean_i - mean_prev
            # Imposto c = 0 perché ho trovato valori per l'anno eseguito
            c = 0
        
        # Mi salvo la media dell'iterazione per quella successiva
        mean_prev = mean_i
    
    return incr