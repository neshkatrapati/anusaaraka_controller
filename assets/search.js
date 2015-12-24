var word;
var hwords = [];
var index = 0;
var pop_up_val="";
var length = 0;

// it searches punjabi and hindi sentences for the word passed in 'click' with root as the root word

function searchSentences(click, root)
{
	var file = "Resources/Sentences/sentences.txt";    // sentences.txt has sample sentences
	var allText = "";
	var rawFile = new XMLHttpRequest();
	rawFile.open("GET",file,false);

	rawFile.onreadystatechange = function()
	{
		if(rawFile.readyState === 4)
		{
			if(rawFile.status === 200 || rawFile.status == 0)
			{
				 allText = rawFile.responseText;
			}
		}
	}
	rawFile.send(null);
	
	var Text = allText.split("\n");
	var textstring = "'";
	
	for(var i=0;i<Text.length;i++)
	{
		textstring = textstring.concat('"');
		textstring = textstring.concat(Text[i]);
		textstring = textstring.concat('"');
	}
	textstring = textstring.concat("'");
	var string = textstring;

	var pun_search = document.getElementById(click).innerHTML;
	var hind_search = document.getElementById(root).innerHTML;
	
	var resultsText,resultsCount;
	if (!pun_search) {
		resultsText='';
		resultsCount='0';
		return;
	}

	var pun_rgx = new RegExp('"([^"]*' + pun_search + '[^"]*)"','gi');
	var hind_rgx = new RegExp('"([^"]*' + hind_search + '[^"]*)"','gi');
	var i = 0, results = '';
	
	while (result = hind_rgx.exec(string)) {
		results += "<br/>" + result[1];
		i += 1;
		if (i >=100)
			break;
	}
	
	i = 0;
	while (result = pun_rgx.exec(string)) {
		results += "<br/>" + result[1];
		i += 1;
		if (i >=100)
			break;
	}
	resultsText=results;
	resultsCount=i;
	
	document.getElementById("content2").innerHTML=resultsText;
}