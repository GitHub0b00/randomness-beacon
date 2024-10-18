var uria = '/rng/';
var flag = true;  // With the change of event listener, the flag is set to true at the beginning. The true state flag indicate that we are in the navigation mode but not automatic updating mode.

var curci; // curci and curpi are the variables that stores the user's current pulse indexes
var curpi;
var lastci; // lastci and lastpi are the variables that stores the lastest pulse indexes in the database.
var lastpi;

// 'year', 'month', 'day', 'hour', 'pervious' methods retrieve the corresponding pulse and the update the pulse index and chain index to the pulse acquired.
// When there is a fetch().then() block, it means it is an Asynchronous process. The code in such a cell will be only excuted one by one, after the response is sent back.
// At the same time, the code after the asynchronous call will continue to be excuted while the asynchronous block is waiting for the response.
function year () {
    // console.log('year clicked');
    if (flag == false) {
        clearInterval(interval);
        flag = true;
    };
    // flag = true;
    // clearInterval(interval);
    var urix = '/rng/chainIndexandpulseIndex_year?chainIndex='+curci.toString()+'&pulseIndex='+curpi.toString();
    disp(urix);
    fetch(urix) // this is here to update the current chain index and pulse index after calling the skip list API. There could be better ways to do it uniformly or simpler. The same applies for the other 3 similar methods.
    .then(response => {
        if (!response.ok) {
            // curci = 1;
            // curpi = 1;
            throw new Error('there was no year pulse linked to this pulse.');
        }
        return response.json();
    })
    .then(re => {
        curci = re.chainIndex
        curpi = re.pulseIndex
    })
    .catch(error => console.error("Error fetching JSON data:", error));
}

function month () {
    if (flag == false) {
        clearInterval(interval);
        flag = true;
    };
    // flag = true;
    // clearInterval(interval);
    var urix = '/rng/chainIndexandpulseIndex_month?chainIndex='+curci.toString()+'&pulseIndex='+curpi.toString();
    disp(urix);
    fetch(urix)
    .then(response => {
        if (!response.ok) {
            // curci = 1;
            // curpi = 1;
            throw new Error('there was no month pulse linked to this pulse.');
        }
        return response.json()
    })
    .then(re => {
        curci = re.chainIndex
        curpi = re.pulseIndex
    })
    .catch(error => console.error("Error fetching JSON data:", error));
}

function day () {
    if (flag == false) {
        clearInterval(interval);
        flag = true;
    };
    // flag = true;
    // clearInterval(interval);
    var urix = '/rng/chainIndexandpulseIndex_day?chainIndex='+curci.toString()+'&pulseIndex='+curpi.toString();
    disp(urix);
    fetch(urix)
    .then(response => {
        if (!response.ok) {
            // curci = 1;
            // curpi = 1;
            throw new Error('there was no day pulse linked to this pulse.');
        }
        return response.json()
    })
    .then(re => {
        curci = re.chainIndex
        curpi = re.pulseIndex
    })
    .catch(error => console.error("Error fetching JSON data:", error));
}

function hour () {
    if (flag == false) {
        clearInterval(interval);
        flag = true;
    };
    // flag = true;
    // clearInterval(interval);
    var urix = '/rng/chainIndexandpulseIndex_hour?chainIndex='+curci.toString()+'&pulseIndex='+curpi.toString();
    disp(urix);
    fetch(urix)
        .then(response => {
        if (!response.ok) {
            // curci = 1;
            // curpi = 1;
            throw new Error('there was no hour pulse linked to this pulse.');
        }
        return response.json()
    })
        .then(re => {
            curci = re.chainIndex
            curpi = re.pulseIndex
        })
        .catch(error => console.error("Error fetching JSON data:", error));
}

// 'first' function display the first pulse of a chain.
function first () {
    if (flag == false) {
        clearInterval(interval);
        flag = true;
    };
    // flag = true;
    // clearInterval(interval);
    // curci = 1;
    curpi = 1;

    var urix = '/rng/chainIndexandpulseIndex?chainIndex='+curci.toString()+'&pulseIndex='+curpi.toString();
    disp(urix);
}

// 'last' function ask for the last pulse from the database via the API call, then it query the database again with the chain index and pulse index of the last pulse returned.
function last () {  // Here it should actually be another function that separate the automatic update button and the last button. So that the clicking of last will stop the automatic update to give user the freedom of navigating among the pulses without bing interrupted by the automatic update.
    fetch('/rng/last')
        .then(response => response.json())
        .then(re => {
            var lci = re[0].chainIndex;
            var lpi = re[0].pulseIndex;
            return [lci, lpi]
        })
        .then((x) => {
            lastci = x[0];
            lastpi = x[1];
            curci = lastci;
            curpi = lastpi;
            // console.log(curci, curpi, lastci, lastpi, '111');
            var urix = '/rng/chainIndexandpulseIndex?chainIndex='+lastci.toString()+'&pulseIndex='+lastpi.toString();
            // return curci, curpi
            return urix;
        })
        .then((urixb) => disp(urixb))
}

// 'auto' function set a time interval to excute the 'last' function repeatedly.
function auto () {
    if (flag == true) {
        document.getElementById("message").textContent = '';
        interval = setInterval(last, 1000);
        flag = false;  // When auto is clicked, the flag is set to false indicating the state of "not in te navigation mode".
    }
}

// This line of code uses DOM in javascript to start the automatic updating function on startup of the page.
// document.addEventListener("DOMContentLoaded", auto);

document.addEventListener("DOMContentLoaded", last);  // The function called by this event listener was auto. It is changed to last to cancel the automatic update function at the startup of the webpage.

function previous () {
    if (flag == false) {
        clearInterval(interval);
        flag = true;
    };
    // flag = true;
    // clearInterval(interval);
    var urix = '/rng/chainIndexandpulseIndex_previous?chainIndex='+curci.toString()+'&pulseIndex='+curpi.toString();
    disp(urix);
    fetch(urix)
        .then(response => {
        if (!response.ok) {
            // curci = 1;
            // curpi = 1;
            throw new Error('there was no previous pulse linked to this pulse.');
        }
        return response.json()
    })
        .then(re => {
            curci = re.chainIndex
            curpi = re.pulseIndex
        })
        .catch(error => console.error("Error fetching JSON data:", error));
}

// 'next' method increase the pulse index by 1. Then, it query the database with the new chain index and pulse index.
function next () {
    // if it is in the automatic update mode, then we are in the last pulse.
    if (flag == false) {
        curci = lastci;
        curpi = lastpi;
        clearInterval(interval);
        flag = true;
    };
    // flag = true;
    // clearInterval(interval);
    if (curpi < lastpi) {
        curpi = curpi + 1;
    } else {
        document.getElementById("message").textContent = 'This is the last pulse of the chain, do not continue clicking';
        return;
    }

    var urix = '/rng/chainIndexandpulseIndex?chainIndex='+curci.toString()+'&pulseIndex='+curpi.toString();
    disp(urix);
}

function specific () {
    if (flag == false) {
        clearInterval(interval);
        flag = true;
    };
    // flag = true;
    // clearInterval(interval);
    curci = parseInt(document.getElementById("chainid").value, 10);
    curpi = parseInt(document.getElementById("pulseid").value, 10);
    var urix = '/rng/chainIndexandpulseIndex?chainIndex='+curci.toString()+'&pulseIndex='+curpi.toString();
    disp(urix);
}

// 'disp' function is for displaying the json data from the API call onto the HTML page.
function disp (uri) {
    document.getElementById("message").textContent = '';
    fetch(uri)
        .then(response => {
        if (!response.ok) {
            throw new Error('there was no pulse to be displayed.');
        }
        return response.json();
    })
        .then(data => {
            const dataDisplay = document.getElementById("dataDisplay");
            // Create HTML elements to display the JSON data
                const tbl = document.createElement("table");

            const tblBody = document.createElement("tbody");
            for (const key in data) {
                if (key != "_id") {
                    if (key != "listValues") {
                        if (key == 'year' || key == 'month' || key == 'day' || key == 'hour' || key == 'minute') {
                            continue;
                        }
                        const row = document.createElement("tr");
                        const cell_f = document.createElement("td");
                        cell_f.className = "left";
                        cell_f.innerHTML ='<br><font size="+1">' + key + '</font>' + " :";
                        const cell_d = document.createElement("td");
                        cell_d.className = "right";
                        cell_d.innerHTML = '<br>' + data[key] + '<br>';
                        row.appendChild(cell_f);
                        row.appendChild(cell_d);
                        tblBody.appendChild(row);
                    }
                    else {
                        for (let i = 0; i < data['listValues'].length; i++) {
                            const row = document.createElement("tr");
                            const cell_f = document.createElement("td");
                            cell_f.className = "left"
                            cell_f.innerHTML = '<br><font size="+1">' + data['listValues'][i]['type'] + '</font>' + " :";
                            const cell_d = document.createElement("td");
                            cell_d.className = "right";
                            cell_d.innerHTML = '<br>' + data['listValues'][i]['value'] + '<br>';
                            row.appendChild(cell_f);
                            row.appendChild(cell_d);
                            tblBody.appendChild(row);
                        }
                    };
                };
            };
            tbl.appendChild(tblBody);
            dataDisplay.innerHTML = "";
            dataDisplay.appendChild(tbl);
        })
        .catch(error => console.error("Error fetching JSON data:", error));
}