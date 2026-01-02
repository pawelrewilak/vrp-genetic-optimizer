const canvas = document.getElementById('mojapapa');
const ctx = canvas.getContext('2d');

const ROZMIAR_CANVAS = 600;  
const MAX_WSPOLRZEDNA = 600; 
const SKALA = ROZMIAR_CANVAS / MAX_WSPOLRZEDNA;
const GODZINA_STARTU = 8; 
const MINUTY_STARTU = GODZINA_STARTU * 60; 

let listaSzkol = [];

let wykresInstancja = null;
const KOLORY_TRAS = ["#FF0000", "#008000", "#0000FF", "#FFA500", "#800080", "#00CED1", "#FF1493"];

function rysujTrasy(trasy) {
ctx.clearRect(0, 0, ROZMIAR_CANVAS, ROZMIAR_CANVAS);
rysujPunkt(300, 30, "red", 8);

listaSzkol.forEach(s => rysujPunkt(s.x, s.y, "#007bff"));

trasy.forEach((trasa, index) => {
    ctx.beginPath();
    ctx.lineWidth = 2;
    ctx.strokeStyle = KOLORY_TRAS[index % KOLORY_TRAS.length];
    let startX = 300; 
    let startY = ROZMIAR_CANVAS - 30;
    ctx.moveTo(startX, startY);

    trasa.forEach(idSzkoly => {
        if (idSzkoly === 0) {
            ctx.lineTo(startX, startY);
        } else {
            let szkola = listaSzkol.find(s => s.id === idSzkoly);
            if (szkola) {
                let px = szkola.x;
                let py = ROZMIAR_CANVAS - szkola.y;
                ctx.lineTo(px, py);
            }
        }
    });
    ctx.stroke();
});
}

function pokazWykres(historia, historiaBest) {
const modal = document.getElementById('modalWykres');
const ctxWykres = document.getElementById('wykresCanvas').getContext('2d');

modal.style.display = 'flex';

if (wykresInstancja) wykresInstancja.destroy();

const labels = historia.map((_, i) => i + 1);

wykresInstancja = new Chart(ctxWykres, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [
            {
                label: 'Rekord Globalny',
                data: historiaBest,
                borderColor: '#28a745',
                borderWidth: 2,
                tension: 0,
                pointRadius: 0
            },
            {
                label: 'Populacja',
                data: historia,
                borderColor: '#007bff',
                borderWidth: 1,
                borderDash: [5, 5],
                pointRadius: 0
            }
        ]
    },
    options: { 
        responsive: true, 
        maintainAspectRatio: false,
        scales: {
            x: { title: { display: true, text: 'Generacja' } },
            y: { title: { display: true, text: 'Zysk (Fitness)' } }
        }
    }
});
}

function zamknijWykres() {
document.getElementById('modalWykres').style.display = 'none';
}

function czasNaMinuty(czasString) {
    if (!czasString) return 0;
    let czesci = czasString.split(':');
    let h = parseInt(czesci[0]);
    let m = parseInt(czesci[1]);
    return (h * 60) + m - MINUTY_STARTU;
}

function rysujPunkt(x, y, kolor, rozmiar = 5) {
    let pixelX = x;
    let pixelY = ROZMIAR_CANVAS - y;

    ctx.beginPath();
    ctx.arc(pixelX, pixelY, rozmiar, 0, Math.PI * 2);
    ctx.fillStyle = kolor;
    ctx.fill();
    ctx.strokeStyle = "black";
    ctx.lineWidth = 1;
    ctx.stroke();
    
    if (kolor === "#007bff") {
        ctx.fillStyle = "white";
        ctx.font = "10px Arial";
    }
}

function dodajWierszDoTabeli(szkola) {
    const tabela = document.getElementById('tabela-szkol').getElementsByTagName('tbody')[0];
    const nowyWiersz = tabela.insertRow();
    
    const komorkaId = nowyWiersz.insertCell(0);
    komorkaId.innerText = szkola.id;

    const komorkaXY = nowyWiersz.insertCell(1);
    komorkaXY.innerText = `(${szkola.x}, ${szkola.y})`;

    const komorkaOkno = nowyWiersz.insertCell(2);
    komorkaOkno.innerText = `${szkola.display_time[0]} - ${szkola.display_time[1]}`;
    const komorkaZysk = nowyWiersz.insertCell(3);
    komorkaZysk.innerText = szkola.profit;
}

console.log("Dashboard VRP Gotowy.");
rysujPunkt(300, 30, "red", 8); 

const btnDodaj = document.getElementById('btn-dodaj');

btnDodaj.addEventListener('click', function() {
    
    let idInput = document.getElementById('new_id');
    let xInput = document.getElementById('new_x');
    let yInput = document.getElementById('new_y');
    let pInput = document.getElementById('new_profit');
    let tminInput = document.getElementById('new_tmin'); 
    let tmaxInput = document.getElementById('new_tmax'); 
    let sTimeInput = document.getElementById('service_time');

    let currentId = parseInt(idInput.value);
    let x = parseFloat(xInput.value);
    let y = parseFloat(yInput.value);
    let profit = parseFloat(pInput.value);
    let sTime = parseFloat(sTimeInput.value);
    let tmin = czasNaMinuty(tminInput.value);
    let tmax = czasNaMinuty(tmaxInput.value);

    if (isNaN(x) || isNaN(y)) { alert("Podaj X i Y!"); return; }
    if (x < 0 || x > 600 || y < 0 || y > 600) { alert("X i Y muszą być 0-600!"); return; }
    if (tmin > tmax) { alert("Koniec okna nie może być przed startem!"); return; }
    if (sTime > (tmax - tmin)) { alert("Za krótkie okno na serwis!"); return; }

    let nowaSzkola = {
        id: currentId,
        x: x,
        y: y,
        profit: profit,
        service_time: sTime,
        time_window_start: tmin, 
        time_window_end: tmax,
        display_time: [tminInput.value, tmaxInput.value]
    };

    listaSzkol.push(nowaSzkola);
    
    rysujPunkt(x, y, "#007bff"); 
    dodajWierszDoTabeli(nowaSzkola);
    
    document.getElementById('licznik_szkol').innerText = "Liczba szkół: " + listaSzkol.length;

    idInput.value = currentId + 1;
    xInput.value = "";
    yInput.value = "";
    xInput.focus();
});

const btnRandom = document.getElementById('btn-random');

function losujLiczbe(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function minutyNaGodzine(minutyOdStartu) {
    let totalMinuty = minutyOdStartu + MINUTY_STARTU; 
    let h = Math.floor(totalMinuty / 60);
    let m = totalMinuty % 60;
    return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}`;
}

if (btnRandom) {
    btnRandom.addEventListener('click', function() {
        console.log("Kliknięto generuj losowo");

        let countInput = document.getElementById('num_generate');
        if (!countInput.value) {
            alert("Wpisz ilość szkół!");
            return;
        }

        let ile = parseInt(countInput.value);
        
        let idInput = document.getElementById('new_id');
        let startId = parseInt(idInput.value);

        for (let i = 0; i < ile; i++) {
            let x = losujLiczbe(10, MAX_WSPOLRZEDNA - 10); 
            let y = losujLiczbe(10, MAX_WSPOLRZEDNA - 10);
            
            let profit = losujLiczbe(100, 500);

            let tmin = losujLiczbe(0, 300); 
            let tmax = tmin + losujLiczbe(60, 180); 
            if (tmax > 480) tmax = 480;

            let tminStr = minutyNaGodzine(tmin);
            let tmaxStr = minutyNaGodzine(tmax);

            let nowaSzkola = {
                id: startId + i,
                x: x,
                y: y,
                profit: profit,
                service_time: 20, 
                time_window_start: tmin,
                time_window_end: tmax,
                display_time: [tminStr, tmaxStr]
            };

            listaSzkol.push(nowaSzkola);
            rysujPunkt(x, y, "#007bff"); 
            dodajWierszDoTabeli(nowaSzkola);
        }

        idInput.value = startId + ile;
        document.getElementById('licznik_szkol').innerText = "Liczba szkół: " + listaSzkol.length;
        console.log(`Wylosowano ${ile} szkół. Lista:`, listaSzkol);
    });
} else {
    console.error("Nie znaleziono przycisku btn-random!");
}

const btnUsun = document.getElementById('btn-usun');

btnUsun.addEventListener('click', function(){
    let idDeleteInput = document.getElementById('id_delete');
    
    let idToDelete = parseInt(idDeleteInput.value);

    if (isNaN(idToDelete)) {
        alert("Podaj ID szkoły do usunięcia!");
        return;
    }

    const index = listaSzkol.findIndex(s => s.id === idToDelete);

    if (index === -1) {
        alert("Nie znaleziono szkoły o ID: " + idToDelete);
        return;
    }

    listaSzkol.splice(index, 1);
    for (let i = index; i < listaSzkol.length; i++) {
        listaSzkol[i].id = listaSzkol[i].id - 1;
    }
    
    let currentNextId = parseInt(document.getElementById('new_id').value);
    document.getElementById('new_id').value = currentNextId - 1;

    ctx.clearRect(0, 0, ROZMIAR_CANVAS, ROZMIAR_CANVAS);
    rysujPunkt(300, 30, "red", 8);

    listaSzkol.forEach(szkola => {
        rysujPunkt(szkola.x, szkola.y, "#007bff");
    });
    const tbody = document.getElementById('tabela-szkol').getElementsByTagName('tbody')[0];
    tbody.innerHTML = ""; 
    
    listaSzkol.forEach(szkola => {
        dodajWierszDoTabeli(szkola);
    });

    document.getElementById('licznik_szkol').innerText = "Liczba szkół: " + listaSzkol.length;
    idDeleteInput.value = "";
});

const btnZatwierdz = document.getElementById('btn-zatwierdz');

btnZatwierdz.addEventListener('click', async function() {
    
    btnZatwierdz.disabled = true;
    btnZatwierdz.innerText = "Obliczam trasę... Proszę czekać.";
    document.body.style.cursor = "wait";

    try {
        const params = {
            pop_size: parseInt(document.getElementById('pop_size').value),
            generations: parseInt(document.getElementById('generations').value),
            mutation_mode: document.querySelector('input[name="tryb_mutacji"]:checked').value,
            cross_mode: document.querySelector('input[name="tryb_krzyzowania"]:checked').value,
            mut_rates: [
                parseFloat(document.getElementById('mut_rate1').value),
                parseFloat(document.getElementById('mut_rate2').value),
                parseFloat(document.getElementById('mut_rate3').value),
                parseFloat(document.getElementById('mut_rate4').value),
                1.0
            ]
        };

        const payload = {
            parametry: params,
            szkoly: listaSzkol
        };

        console.log("Wysyłam do Pythona:", payload);

        const odpowiedz = await fetch('/oblicz-vrp', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!odpowiedz.ok) {
            throw new Error(`Błąd serwera: ${odpowiedz.status}`);
        }
        
        const wynik = await odpowiedz.json();
        console.log("Serwer zwrócił: ", wynik);
        
        if (wynik.routes) {
            rysujTrasy(wynik.routes);
        }

        if (wynik.history && wynik.history_best) {
            pokazWykres(wynik.history, wynik.history_best);
        }
        
        alert("Obliczenia zakończone sukcesem!");

    } catch (blad) {
        console.error("Wystąpił błąd:", blad);
        alert("Wystąpił błąd połączenia z serwerem. Sprawdź konsolę (F12).");
    } finally {

        btnZatwierdz.disabled = false;
        btnZatwierdz.innerText = "Zatwierdź i Oblicz VRP";
        document.body.style.cursor = "default";
    }
});
