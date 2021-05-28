(function(){
	var btn = document.getElementById("drop-swicher");
	var menu = document.getElementById('drop-menu');
	btn.onmouseover = function() {
		if(menu.style.display == "none"){
			menu.style.display = ""; 
		}
		btn.style.backgroundColor = "#b0bac100";
	};
	btn.onmouseleave = function() { 
		btn.style.backgroundColor = "#b0bac100";
	};
	menu.addEventListener("mouseleave", function() { 
		if(menu.style.display == ""){
			menu.style.display = "none"; 
		}
		console.log("aaa"+menu.style.display);
	});
})(function myFunction() {
  var element = document.body;
  element.classList.toggle("dark-mode");
});