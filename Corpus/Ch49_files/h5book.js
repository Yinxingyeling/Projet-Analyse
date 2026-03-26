function $id(id){return document.getElementById(id);}
function $sel(v){return document.querySelector(v);}
function getLocalData(key){if(typeof localStorage!='undefined'){return localStorage.getItem(key);}return null;}
function setLocalData(key,value){if(typeof localStorage!='undefined'){localStorage.setItem(key,value);}}
function delLocalData(key){if(typeof localStorage!='undefined'){localStorage.removeItem(key)}}
var fontArr = [['24px', '14px'],['27px', '16px'],['30px', '18px'],['33px', '20px'],['37px', '22px']];
function goTop(acceleration, time) {
	acceleration = acceleration || 0.1;
	time = time || 16;
	var x1 = 0;
	var y1 = 0;
	var x2 = 0;
	var y2 = 0;
	var x3 = 0;
	var y3 = 0;
	if (document.documentElement) {
		x1 = document.documentElement.scrollLeft || 0;
		y1 = document.documentElement.scrollTop || 0;
	}
	if (document.body) {
		x2 = document.body.scrollLeft || 0;
		y2 = document.body.scrollTop || 0;
	}
	var x3 = window.scrollX || 0;
	var y3 = window.scrollY || 0;
	var x = Math.max(x1, Math.max(x2, x3));
	var y = Math.max(y1, Math.max(y2, y3));
	var speed = 1 + acceleration;
	window.scrollTo(Math.floor(x / speed), Math.floor(y / speed));
	if(x > 0 || y > 0) {
		var invokeFunction = "goTop(" + acceleration + ", " + time + ")";
		window.setTimeout(invokeFunction, time);
	}
}
function logout(){
	$.post("logout.htm",{},function(data){
		if(eval(data)=="success"){
			window.location="login.htm";
		}
	});
}