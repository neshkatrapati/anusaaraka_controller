var word;
var hwords = [];
var index = 0;
var pop_up_val="";
var length = 0;

// Function for handling events, to fetch punjabi word, source morph and root word
function handleEvent(event, req_word, source_morph, root) {

	var root_word = document.getElementById(root).innerHTML;
	var morph = (document.getElementById(source_morph).innerHTML).split(',')[0];

        document.onkeypress=function(e) {
                var e=window.event || e;
                document.getElementById("content1").innerHTML="";
		document.getElementById("content2").innerHTML="";
		if(e.charCode==108) {
			localDict(morph);
                        window.location='#popup1';
                }
                if(e.charCode==100) {
			dictionary(req_word);
                        window.location='#popup1';
                }
                if(e.charCode==103) {
                        glosbeDictionary(req_word);
                        window.location='#popup1';
                }
                if(e.charCode==115) {
                       searchSentences(req_word,root);
                        window.location='#popup2';
                }
        }
}


get_group_details = function() {
    url = window.location.toString();
    p = url.search('group');
    t = url.substr(p+6, 3);
    q = t.split('/')
    return q;
}


$('td').mouseup(function(event) {
    rowClass = event.target.parentNode.className;
    ps = event.target.parentNode.parentNode.parentNode;
    rowNumber = parseInt(rowClass[rowClass.length - 1]);
    others = get_group_details();
    colid = ps.getAttribute('col');
    //console.log(window.getSelection());
    // console.log(rowNumber);
    // console.log(ps.id);
    // console.log(others);
    text = window.getSelection().toString();
    uril = "http://localhost:5000/group/"+q[0]+"/"+q[1]+"/"+ps.id+"/"+rowNumber+'/'+colid+'?text=\"'+text+'\"';
    console.log(uril);

    $.ajax({
        url: uril,
        context: document.body
    }).done(function(data) {
        console.log(data);
        document.getElementById('side_bar').innerHTML += JSON.stringify(data);
    });

    //console.log(window.getSelection());
});


