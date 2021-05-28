(function(){
	var btn = document.getElementById("parkinglist").getElementsByTagName("tr");
	for(var a = 0; a < btn.length; a++){
		if(btn[a].firstElementChild.tagName.toLowerCase() == "td"){
			btn[a].addEventListener("click", function() {
				var id = this.firstElementChild.innerText;
	            var route = window.location.protocol + "//" + window.location.host;
	            window.location.href=route+"/admin/user/"+ id;


			});
		}
	}
})();r