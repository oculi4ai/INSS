document.onreadystatechange = function() {
    if (document.readyState !== "complete") {
        document.querySelector("#body-content").style.display = "none";
        document.querySelector("#loader").style.visibility = "visible";
        console.log('0')
    } else {
        document.querySelector("#loader").style.display = "none";
        document.querySelector("#body-content").style.display = "block";
        console.log('1')
    }
};