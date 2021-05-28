(function(){
var xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
				var res = JSON.parse(this.responseText);
				var ilegodzin = 24*2;
				//var ileparkingow = 10;
				var cal = document.getElementById("parking-calendar-zaj");
				if(cal.childElementCount > 1){
				    return;
				}
				for(var row = 0; row < ilegodzin; row++){
					var r = document.createElement("div");
					r.classList.add("cal-row");
					r.classList.add("tooltip");
					//var ileprocent = Math.random()*row*100.0/ilegodzin;
					console.log("Ile:"+res.reservation[row]);
					var ileprocent = Number.parseInt(res.reservation[row])*100.0/res.maxparking;
					//r.style.height = (100-ileprocent)+"px";
					var goh1 = Math.floor(row/2);
					if(row % 2 == 1){
					    goh1 += ":30";
					}else{
					    goh1 += ":00";
					}
					var goh2 = Math.floor((row)/2);

					if(row % 2 == 1){
					    goh2 = (goh2+1)+":00";
					}else{
					    goh2 = goh2+":30";
					}
					var goh ="<br>"+ goh1 +" - "+goh2;
					var spn = 'Rezerwacja' +goh;
					spn = "Zajęte: "+ileprocent+"%<br>"+spn;
					if(res.reservation[row] >= res.maxparking){
					 	spn = 'Brak miejsc';
					}
					spn = '<span class="tooltiptext">'+spn+'</span>';
					r.innerHTML = '<div style="height: '+(100-ileprocent)+'%;"></div><div></div>'+spn;//<div class="cal-hour"><div>12:00</div></div>';
					cal.appendChild(r);
					if(row % 2 == 1 && row != ilegodzin-1){
						var spac = document.createElement("div");
						spac.classList.add("cal-space");
						cal.appendChild(spac);
					}
				}
				var obj = document.getElementById("parking-calendar-ops");
				for(var row = 0; row < ilegodzin; row++){
					if(row % 2 == 0){
						var spac = document.createElement("div");
						spac.classList.add("cal-hour");
						spac.innerHTML = '<div>'+(row/2)+':00</div>';
						obj.appendChild(spac);
					}
				}
			}else{
			    var res = JSON.parse('{"id":9,"maxparking":"4","reservation":[3,2,2,4,4,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2]}');
				console.log(res);
				var ilegodzin = 24*2;
				//var ileparkingow = 10;
				var cal = document.getElementById("parking-calendar-zaj");
				if(cal.childElementCount > 1){
				    return;
				}
				for(var row = 0; row < ilegodzin; row++){
					var r = document.createElement("div");
					r.classList.add("cal-row");
					r.classList.add("tooltip");
					//var ileprocent = Math.random()*row*100.0/ilegodzin;
					console.log("Ile:"+res.reservation[row]);
					var ileprocent = Number.parseInt(res.reservation[row])*100.0/res.maxparking;
					//r.style.height = (100-ileprocent)+"px";
					var goh1 = Math.floor(row/2);
					if(row % 2 == 1){
					    goh1 += ":30";
					}else{
					    goh1 += ":00";
					}
					var goh2 = Math.floor((row)/2);

					if(row % 2 == 1){
					    goh2 = (goh2+1)+":00";
					}else{
					    goh2 = goh2+":30";
					}
					var goh ="<br>"+ goh1 +" - "+goh2;
					var spn = 'Rezerwacja' +goh;
					spn = "Zajęte: "+ileprocent+"%<br>"+spn;
					if(res.reservation[row] >= res.maxparking){
					 	spn = 'Brak miejsc';
					}
					spn = '<span class="tooltiptext">'+spn+'</span>';
					r.innerHTML = '<div style="height: '+(100-ileprocent)+'%;"></div><div></div>'+spn;//<div class="cal-hour"><div>12:00</div></div>';
					cal.appendChild(r);
					if(row % 2 == 1 && row != ilegodzin-1){
						var spac = document.createElement("div");
						spac.classList.add("cal-space");
						cal.appendChild(spac);
					}
				}
				var obj = document.getElementById("parking-calendar-ops");
				for(var row = 0; row < ilegodzin; row++){
					if(row % 2 == 0){
						var spac = document.createElement("div");
						spac.classList.add("cal-hour");
						spac.innerHTML = '<div>'+(row/2)+':00</div>';
						obj.appendChild(spac);
					}
				}
			}
		};
		var data = new Date();
		var dat = data.getDay() +"-"+ data.getMonth() +"-"+ data.getFullYear();
		dat = "21-02-13"

		xhttp.open("GET", "/parking_reservation/"+document.getElementById("parkingidcalendar").value+"/"+dat+"/", true);
		//xhttp.open("GET", "a/parking_reservation.json", true);
		xhttp.setRequestHeader("Content-type", "application/json");
		xhttp.send();
		/*var res = JSON.parse('{"id":9,"maxparking":"4","reservation":[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2]}');
		console.log(res);
		var ilegodzin = 24*2;
		//var ileparkingow = 10;
		var cal = document.getElementById("parking-calendar-zaj");
		for(var row = 0; row < ilegodzin; row++){
			var r = document.createElement("div");
			r.classList.add("cal-row");
			//var ileprocent = Math.random()*row*100.0/ilegodzin;
			console.log("Ile:"+res.reservation[row]);
			var ileprocent = Number.parseInt(res.reservation[row])*100.0/res.maxparking;
			//r.style.height = (100-ileprocent)+"px";
			r.innerHTML = '<div style="height: '+(100-ileprocent)+'%;"></div><div></div>';//<div class="cal-hour"><div>12:00</div></div>';
			cal.appendChild(r);
			if(row % 2 == 1 && row != ilegodzin-1){
				var spac = document.createElement("div");
				spac.classList.add("cal-space");
				cal.appendChild(spac);
			}
		}
		var obj = document.getElementById("parking-calendar-ops");
		for(var row = 0; row < ilegodzin; row++){
			if(row % 2 == 0){
				var spac = document.createElement("div");
				spac.classList.add("cal-hour");
				spac.innerHTML = '<div>'+(row/2)+':00</div>';
				obj.appendChild(spac);
			}
		}*/	});
		}
	}
})();