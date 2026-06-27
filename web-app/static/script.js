async function getData() {

    const response = await fetch("/api/latest");
    const data = await response.json();

    document.getElementById("rms").innerHTML = data.rms;
}

getData();

setInterval(getData, 1000);