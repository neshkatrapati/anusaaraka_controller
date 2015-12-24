function getText(){
	var text = document.getElementById("demo").innerHTML;
	var converted = convert(text);
	document.getElementById("demo").innerHTML=converted;
}
function convert(text){
	var convertedToHindi = '';
	for (var i=0; i < text.length; i++){
		var ch = text.charCodeAt(i).toString(16).toUpperCase();
		while (ch.length < 4) {
			ch = '0' + ch;
		}
		ch="0x"+ch;
		if(eval(ch)>=eval('0x0A00') && eval(ch)<=eval('0x0A7F'))
		{
			ch=eval(ch)-eval('0x0100');
		}
		var alpha = String.fromCharCode(eval(ch));
		console.log(alpha);
		convertedToHindi+=alpha;
	}

	return convertedToHindi;
}
