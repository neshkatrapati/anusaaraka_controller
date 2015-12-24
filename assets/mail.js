<style type="text/css">
        /* popup_box DIV-Styles*/
        
        #popup_box {
            display: none;
            position: fixed;
            _position: absolute;
            height: 160px;
            width: 37%;
            background: #FFFFFF;
            left: 20%;
            top: 150px;
            z-index: 100;
            margin-left: 15px;
            border: 2px solid #ff0000;
            opacity: 0;
            padding: 15px;
            font-size: 15px;
            -moz-box-shadow: 0 0 5px #ff0000;
            -webkit-box-shadow: 0 0 5px #ff0000;
            box-shadow: 0 0 5px #ff0000;
        }
        
        a {
            cursor: pointer;
            text-decoration: none;
        }
        /* This is for the positioning of the Close Link */
        
        #popupBoxClose {
            font-size: 20px;
            line-height: 15px;
            right: 5px;
            top: 5px;
            position: absolute;
            color: #6fa5e2;
            font-weight: 500;
        }
    </style>
    <div id="popup_box" style="width:60%;">
        <textarea name="message" id="message" rows="5" style="width:80%;" readonly></textarea>
        <br/>
        <br/> Suggestion :
        <input type="text" id="sug" name="sug" />
        <br/>
        <input type="submit" value="Send Email" style="float: right; position: absolute; bottom: 18px; right: 10px;" onclick="mail();return false;"><br>
        <a id="popupBoxClose">Close</a>
    </div>
<script>
       function mail() {
            document.getElementById("popup_box").style.display = "none";
            document.getElementById('popup_box').style.opacity = "0";
            hideLayer();
            alert("MESSAGE HAS BEEN SUCCESSFULLY SENT");
        }
        function loadPopupBox() { // To Load the Popupbox
            document.getElementById('popup_box').style.display = "block";
            document.getElementById('popup_box').style.opacity = "1";
        }
        document.getElementById('popupBoxClose').onclick = function() {
            document.getElementById('popup_box').style.display = "none";
            document.getElementById('popup_box').style.opacity = "0";
            hideLayer();
        }
        function getBrowserHeight() {
            var intH = 0;
            var intW = 0;
            if (document.body && (document.body.clientWidth || document.body.clientHeight)) {
                intH = document.body.clientHeight;
                intW = document.body.clientWidth;
            }
            return {
                width: parseInt(intW),
                height: parseInt(intH)
            };
        }

        function setLayerPosition() {
            var shadow = document.getElementById("shadow");
            var bws = getBrowserHeight();
            shadow.style.width = bws.width + "px";
            shadow.style.height = bws.height + "px";
            shadow = null;
        }

        function showLayer() {
            setLayerPosition();
            var shadow = document.getElementById("shadow");
            shadow.style.display = "block";
            shadow = null;
        }

        function hideLayer() {
            var shadow = document.getElementById("shadow");
            shadow.style.display = "none";
            shadow = null;
        }
table = document.getElementsByTagName("table");
var checkKeyPressedForTableClick = null;
document.addEventListener('keydown', function(e){
    checkKeyPressedForTableClick = String.fromCharCode( e.which );
    console.log( "Key down fired", checkKeyPressedForTableClick);
});
document.addEventListener('keyup', function(e){
    checkKeyPressedForTableClick = null;
    console.log( "Key down fired", checkKeyPressedForTableClick);
});

var onTableClicked = function(e) {
    console.log('si');
    if (checkKeyPressedForTableClick == 'M') {
        e.stopPropagation();
    }
    else {
        return;
    }
            
    showLayer();
    var str = "Word - ";
    var str1 = "";
    tr = this.getElementsByTagName('tr');
    if(tr.length==0)return;
    td = tr[0].getElementsByTagName('td');
    if(td.length==0)return;
    a = td[0].getElementsByTagName('a');    
    if(a.length==0)return;
    str=a[0].innerHTML;
    var sen = "";
    var hindi = "";
/*    span = a[0].getElementsByTagName('span');

    if (span[0] == null) {
        a = td[1].getElementsByTagName('a');
        span = a[0].getElementsByTagName('span');
        str += span[0].innerHTML;
    } else str += span[0].innerHTML;

    //getting sentence
    table1 = document.getElementsByTagName("table");
    var nextsen = "";
    var man = 0;
    for (i = 0; i < table1.length; i++) {
        if (table1[i].getElementsByTagName("tr")[0].getElementsByTagName("td").length == 2) man++;
        if (table1[i] == this) break;
    }
    man--;
    var k = i;
    for (j = i; j >= 0; j--) {
        tr = table1[j].getElementsByTagName('tr');
        td = tr[0].getElementsByTagName('td');
        if (td[1] != null) {
            senno = td[0].innerHTML;
            k = j;
            break;
        }
    }
    for (j = k; j <= i; j++) {
        tr = table1[j].getElementsByTagName('tr');
        td = tr[0].getElementsByTagName('td');
        if (j != k) {
            a = td[0].getElementsByTagName('a');
        } else {
                a = td[1].getElementsByTagName('a');
        }
        span = a[0].getElementsByTagName('span');
        nextsen += span[0].innerHTML + " ";
    }
    for (j = i + 1; j < table1.length; j++) {
        r = table1[j].getElementsByTagName('tr');
        td = tr[0].getElementsByTagName('td');
        if (td[1] == null) {
            a = td[0].getElementsByTagName('a');
            span = a[0].getElementsByTagName('span');
            nextsen += span[0].innerHTML + " ";
        } else {
            break;
        }
    }
            //Storing Word, Root, English Sentence and hindi Trnslation in str variable.
            str += "\nRoot -" + str1 + "\nSentence - " + nextsen;

            if (top.frames["ManHindiTranslation"]) {
                var fr = top.ManHindiTranslation;
                var tableid = "table" + man;
                var mansen = fr.document.getElementById(tableid);
                var manspan = mansen.getElementsByTagName("span");
                var manhnd = "";
                for (i = 0; i < manspan.length; i++) {
                    manhnd += manspan[i].innerHTML + " ";
                }
                str += "\nManual Translation - " + manhnd;
            }
            str += "\nHindi Translation - ";
            //if(top.frames["ManHindiTranslation"]){
            var hnd = new Array();
            for (i = 0; i < 2; i++) {
                hnd[i] = new Array();
            }
            hnd[0][0] = "1.1";
            hnd[0][1] = "जाँच कीजिए .";
            hnd[1][0] = "2.1";
            hnd[1][1] = "यह अनुसारका के लिए नमूना फाइल है .";
            var k = 0;
            var i = 0;
            while (k != 2) {
                if (senno[i] == '.') k++;
                i++;
            }
            senno = senno.slice(0, i - 1);
            for (i = 0; i < 2; i++) {
                if (hnd[i][0] == senno) {
                    str += hnd[i][1];
                    break;
                }
            }
*/
if(str === "ਪਾਕਿਸਤਾਨ" || str === "ਸ਼ਾਹਮੁਖੀ" ||  str === "ਪੰਜਾਬੀ" || str === "ਅਤੇ" || str === "ਗੁਰਮੁਖੀ")
{
sen= "ਪੰਜਾਬੀ (ਸ਼ਾਹਮੁਖੀ ) ਪਾਕਿਸਤਾਨ ਅਤੇ (ਗੁਰਮੁਖੀ)";
hindi = "प॰जाबी (स़ाहमुखी‎) पाकिसतान और  (गुरमुखी) ";
}
else if (str ==="ਇਹ" || str ==="ਭਾਸ਼ਾਵਾਂ ਦੇ"||str === "ਹਿੰਦ" || str === "ਇਰਾਨੀ" || str === "ਪਰਵਾਰ ਵਿਚੋਂ" || str === "ਹਿੰਦ" || str ==="ਯੂਰਪੀ")
{
sen="ਇਹ ਭਾਸ਼ਾਵਾਂ ਦੇ ਹਿੰਦ-ਇਰਾਨੀ ਪਰਵਾਰ ਵਿੱਚੋਂ ਹਿੰਦ-ਯੂਰਪੀ ਪਰਵਾਰ ਨਾਲ ਸਬੰਧ ਰੱਖਦੀ ਹੈ। ";
hindi = "इह भास़ावां दे हि॰द-इरानी परवार विॱचों हि॰द-यूरपी परवार नाल सब॰ध रॱखदी है।";
}
            document.getElementById("message").innerHTML ="ROOT - "+ str+"\n\nsentence - "+sen+"\n\nHindi - "+ hindi;
            loadPopupBox();
        };
        for (i = 0; i < table.length; i++) {
            table[i].addEventListener('click', onTableClicked, true);
        }
</script>