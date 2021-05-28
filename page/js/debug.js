function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}
var yes = true;
async function reload() {
	await sleep(5000);
	if (yes) {
		location.reload();
	}
}

const di = document.createElement("div");
const but = document.createElement("button");
di.style = "position: fixed; bottom: 100px; width: 100%; text-align: center;";
but.style = "transition-duration: 0.2s; background: blue; color: white; font-weight: 600; font-size: 20px; padding: 10px; border: 2px solid black; border-radius: 20px;";
but.onmouseover = function() { this.style.background = 'green'; };
but.onmouseout = function() { this.style.background = 'blue'; };
but.onclick = function() { yes = false; document.body.removeChild(di); if (window.location.hash !== "#noref") { window.location.hash = "#noref"; } else { window.location.hash = ""; location.reload(); } };
di.appendChild(but);
document.body.appendChild(di);
if (window.location.hash !== "#noref") {
	but.innerHTML = "Przestań odświeżać!";
	reload();
} else {
	but.innerHTML = "Wznów odświeżanie!";
}