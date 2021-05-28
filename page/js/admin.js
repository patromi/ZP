(function(){
	var btn = document.getElementById("parkinglist").getElementsByTagName("tr");
	for(var a = 0; a < btn.length; a++){
		if(btn[a].firstElementChild.tagName.toLowerCase() == "td"){
			btn[a].addEventListener("click", function() {
				var id = this.firstElementChild.innerText;
				alert("Przekierowanie na szczegóły parkingu (w przyszłości) id: "+id);
			});
		}
	}
})();