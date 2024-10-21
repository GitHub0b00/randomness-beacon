var ind = 0;
var m = "";
var interval;

function update () {
    fetch("word.txt")
    .then(response => {
        if (!response.ok) {
            throw new Error("random file was not found.")
        }
        return response.text();
    })
    .then(re => {
        var data = re.split("*");
        if (parseInt(data[4]) != ind) {
            console.log(parseInt(data[1]))
            // the check for m.length less than 512 is to limit the display length to be less than 512 digits.
            if (m.length < 512) {
                // m = m + data[0];
                m = data[0] + m;
            }
            else {
                // m = m.slice(1, 512) + data[0];
                m = data[0] + m.slice(0, 511)
            };
            document.getElementById("message").innerHTML = m;
            ind = parseInt(data[4]);
            document.getElementById("metrics").innerHTML = "g2(0): " + data[1] + " ch1_efficiency: " + data[2] + " ch2_efficiency: " + data[3];
        };
    });
};

function metrics () {
    fetch("word.txt")
    .then(response => {
        if (!response.ok) {
            throw new Error("random file was not found.")
        }
        return response.text();
    })
    .then(re => {
        var data = re.split("*");
        document.getElementById("metrics").innerHTML = "g2(0): " + data[1] + " ch1_efficiency: " + data[2] + " ch2_efficiency: " + data[3];
    });
};

interval2 = setInterval(metrics, 1);

function start () {
    interval = setInterval(update, 1);
};

function stop () {
    clearInterval(interval);
};

function clearAll () {
    m = "";
    document.getElementById("message").innerHTML = "";
}
