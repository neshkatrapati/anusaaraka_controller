var word;
var hwords = [];
var index = 0;
var pop_up_val="";
var length = 0;

// To get english word for the requested punjabi word in w
function makeCall(callback, w) {

        $.ajax({
        
                //To get html of url

                url: 'http://www.shabdkosh.com/pa/translate?e='+w+'&l=pa',
        
                type: 'GET',
        
                success: function(res) {
                        var word = $(res.responseText).find('a.in').eq(0).text();
                        callback(word);
                },
        
                error: function() {
                        callback("");
                }
        });
}

// To get word meaning from Shabdkosh.com of request_word
function dictionary(request_word) {

        document.getElementById("content1").innerHTML="Loading...";
        var w = document.getElementById(request_word).innerHTML;

        pop_up_val = "";
        pop_up_val += "<strong>"+w+"</strong><br/>";
        pop_up_val += "Results from shabdkosh.com<br/>";

        makeCall(function (word) {
                
                index=0;
                hwords = [];
                length=0;

                        if(word != "") {

                                $.ajax({ 
                                        
                                        //To get html of url
                                        
                                        url: 'http://www.shabdkosh.com/hi/translate?e='+word+'&l=hi',
                                        
                                        type: 'GET',
                                        
                                        success: function(res) {
                                                
                                                while(index<10) {
                                                        var hword = $(res.responseText).find('a.in').eq(index).text();
                                                        if(hword != "") hwords.push(hword);
                                                        else break;
                                                        index += 1;
                                                }

                                                length = index;
                                                
                                                if(length == 0) pop_up_val += "Not found<br/>";
                                                else {
                                                        index=0;
                                                        while(index<length) { 
                                                                pop_up_val += "<br/>"+((index+1)+" "+hwords[index]);
                                                                index += 1;
                                                        }
                                                }

                                                document.getElementById("content1").innerHTML=pop_up_val; 
                                        },

                                        error: function() {
                                                pop_up_val += "Not found<br/>";
                                                document.getElementById("content1").innerHTML=pop_up_val; 
                                        }
                                });
                        }

                        else {
                                pop_up_val += "Not found<br/>";
                                
                                document.getElementById("content1").innerHTML=pop_up_val; 
                        }
        }, w);
}

// To get word meaning from glosbe.com of request_word
function glosbeDictionary(request_word) {

        document.getElementById("content1").innerHTML="Loading...";
        var w = document.getElementById(request_word).innerHTML;   

        pop_up_val = "";    
        pop_up_val += "<strong>"+w+"</strong><br/>";
        pop_up_val += "Results from glosbe.com<br/>";
        hwords = [];
        index = 0;
        length = 0;

        $.ajax({

                //To get html of url

                url: 'https://glosbe.com/pa/hi/'+w,
                
                type: 'GET',
                
                success: function(res) {
                        
                        while(index<10) {
                                
                                var hword = $(res.responseText).find('strong.nobold').eq(index).text();
                                    
                                if(hword != "") hwords.push(hword);
                                else break;
                                index += 1;
                        }

                        length = index;
                        
                        if(length == 0) {
                                pop_up_val += "Not found<br/>";
                        }
                        else {
                                index=0;
                                while(index<length) {
                                        pop_up_val += "<br/>"+((index+1)+" "+hwords[index]);
                                        index += 1;
                                }
                        }   
        
                        document.getElementById("content1").innerHTML=pop_up_val; 
                
                },
                
                error: function() {
                        pop_up_val += "Not found<br/>";
                        
                        document.getElementById("content1").innerHTML=pop_up_val; 
                }
        });
}

// To get word meaning from local dictionary pdict.utf8 of source morph of the punjabi word in request_word
function localDict(request_word) {
        
	var file = "Resources/Dictionary/pdict.utf8";
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
	var results = "Not found\n";	
	
        for(var i=0;i<Text.length;i++)
	{		
		var dict_word = Text[i].split(',')[0].slice(1,-1);
		if(String(request_word).trim() == String(dict_word).trim()) {
			
			results = Text[i];
			break;
		}
	}

	document.getElementById("content1").innerHTML = results;		
}