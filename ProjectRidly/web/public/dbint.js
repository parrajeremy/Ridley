    var AAArray = [];
    var ABArray = [];
    var BAArray = [];
    var BBArray = [];
    var CAArray = [];
    var CBArray = [];
    var DAArray = [];
    var DBArray = [];
    var timeArray = [];
    var tempArray = [];
    var rhArray = [];
    var pressureArray = [];

function fetchPosts() {
    "use strict";
    $.ajax({ url: 'fetch', dataType: 'json',
        error: function (jqxhr, textStatus, errorThrown) {
            console.log('error', textStatus, '//', errorThrown);
        },
        success: function (json) {
		console.log(json);
            var currentvals;
	    var currentCO;
            currentCO = $('#currentCO');
	    var currentNO2;
            currentNO2 = $('#currentNO2');
	    var currentO3;
            currentO3 = $('#currentO3');
	    var currentSO2;
            currentSO2 = $('#currentSO2');
	    var currentH2S;
            currentH2S = $('#currentH2S');
	    var currentTOX;
            currentTOX = $('#currentTOX');
	    var currentTOR;
            currentTOR = $('#currentTOR');
            currentvals = $('#currentvals');
            $.each(json.data, function (i, post) {
    	
		localStorage.setItem('AA_sen', post.AA_sen);
		localStorage.setItem('AA_base', post.AA_base);
		localStorage.setItem('AA_zero', post.AA_zero);
		localStorage.setItem('AA_span', post.AA_span);
		localStorage.setItem('AB_sen', post.AB_sen);
		localStorage.setItem('AB_base', post.AB_base);
		localStorage.setItem('AB_zero', post.AB_zero);
		localStorage.setItem('AB_span', post.AB_span);
		localStorage.setItem('BA_sen', post.BA_sen);
		localStorage.setItem('BA_base', post.BA_base);
		localStorage.setItem('BA_zero', post.BA_zero);
		localStorage.setItem('BA_span', post.BA_span);
		localStorage.setItem('BB_sen', post.BB_sen);
		localStorage.setItem('BB_base', post.BB_base);
		localStorage.setItem('BB_zero', post.BB_zero);
		localStorage.setItem('BB_span', post.BB_span);
		localStorage.setItem('CA_sen', post.CA_sen);
		localStorage.setItem('CA_base', post.CA_base);
		localStorage.setItem('CA_zero', post.CA_zero);
		localStorage.setItem('CA_span', post.CA_span);
		localStorage.setItem('CB_sen', post.CB_sen);
		localStorage.setItem('CB_base', post.CB_base);
		localStorage.setItem('CB_zero', post.CB_zero);
		localStorage.setItem('CB_span', post.CB_span);
		localStorage.setItem('DA_sen', post.DA_sen);
		localStorage.setItem('DA_base', post.DA_base);
		localStorage.setItem('DA_zero', post.DA_zero);
		localStorage.setItem('DA_span', post.DA_span);
		localStorage.setItem('DB_sen', post.DB_sen);
		localStorage.setItem('DB_base', post.DB_base);
		localStorage.setItem('DB_zero', post.DB_zero);
		localStorage.setItem('DB_span', post.DB_span);
		localStorage.setItem('AAsel', post.AAsel);
		localStorage.setItem('ABsel', post.ABsel);
		localStorage.setItem('BAsel', post.BAsel);
		localStorage.setItem('BBsel', post.BBsel);
		localStorage.setItem('CAsel', post.CAsel);
		localStorage.setItem('CBsel', post.CBsel);
		localStorage.setItem('DAsel', post.DAsel);
		localStorage.setItem('DBsel', post.DBsel);
		localStorage.setItem('AAunit', post.AAunit);
		localStorage.setItem('ABunit', post.ABunit);
		localStorage.setItem('BAunit', post.BAunit);
		localStorage.setItem('BBunit', post.BBunit);
		localStorage.setItem('CAunit', post.CAunit);
		localStorage.setItem('CBunit', post.CBunit);
		localStorage.setItem('DAunit', post.DAunit);
		localStorage.setItem('DBunit', post.DBunit);
		
            });
        }});
}

function determineType(address, type1, type2, value1, value2) {
    'use strict';
    var ADDR_83 = 83;
    var ADDR_85 = 85;
    var ADDR_86 = 86;
    var ADDR_87 = 87;    
    console.log(address, type1, type2, value1, value2);
    switch (address) {
       case ADDR_87:
            AAArray.push(value1)
            ABArray.push(value2)
		localStorage.setItem('AAlabel', type1)
		localStorage.setItem('ABlabel', type2)
            break
       case ADDR_86:
            BAArray.push(value1)
            BBArray.push(value2)
		localStorage.setItem('BAlabel', type1)
		localStorage.setItem('BBlabel', type2)      
            break
       case ADDR_85:
            CAArray.push(value1)
            CBArray.push(value2)
		localStorage.setItem('CAlabel', type1)
		localStorage.setItem('CBlabel', type2)
            break
       case ADDR_83:
            DAArray.push(value1)
            DBArray.push(value2)
		localStorage.setItem('DAlabel', type1)
		localStorage.setItem('DBlabel', type2)
            break
       default:
            console.log("Error parssing data: ")
            break
                    }
			
}

function timeConvert(UNIX_timestamp){
  var a = new Date(UNIX_timestamp * 1000);
  var hour = a.getHours();
  var min = a.getMinutes();
  var sec = a.getSeconds();
  var time = hour + ':' + min + ':' + sec ;
  return time;
}

function fetchData() {
      
      AAArray.length = 0;
      ABArray.length = 0;
      BAArray.length = 0;
    	BBArray.length = 0;
    	CAArray.length = 0;
    	CBArray.length = 0;
    	DAArray.length = 0;
    	DBArray.length = 0;
	timeArray.length = 0;
	tempArray.length = 0;
	rhArray.length = 0;
	pressureArray.length = 0;
	var x = 0;		
    "use strict"
    localStorage.setItem('lastTime', (localStorage.getItem('newTime'))); 
    
    $.ajax({ url: 'fetch2', dataType: 'json',
        error: function (jqxhr, textStatus, errorThrown) {
            console.log('error', textStatus, '//', errorThrown);
        },
        success: function (json) {

           $.each(json.data, function (i, post) {  
			switch (x) {
				case 4:
                            				
                            timeArray.push(timeConvert(post.time))

                            localStorage.setItem('newTime', timeArray[0]);

					rhArray.push(post.rh)
					tempArray.push(post.temp)
					pressureArray.push(post.pressure)
					x = 0
					
				default:
					//console.log(post.address, post.type1);
					determineType(post.address, post.type1, post.type2, post.value1, post.value2);
        				//determineType(post.address, post.type2, post.value2);
					x++
					break
				}
            });
			//localStorage.setItem('NO2', JSON.stringify(NO2Array));
			//localStorage.setItem('O3', JSON.stringify(O3Array));
			//localStorage.setItem('CO', JSON.stringify(COArray));
			//localStorage.setItem('TOR', JSON.stringify(TORArray));
			//localStorage.setItem('TOX2', JSON.stringify(TOX2Array));
			//localStorage.setItem('TOX', JSON.stringify(TOXArray));
			//localStorage.setItem('SO2', JSON.stringify(SO2Array));
			//localStorage.setItem('H2S', JSON.stringify(H2SArray));
			//localStorage.setItem('TEMP', JSON.stringify(tempArray));
			//localStorage.setItem('RH', JSON.stringify(rhArray));
			//localStorage.setItem('PRESSURE', JSON.stringify(pressureArray));
			//localStorage.setItem('time', JSON.stringify(timeArray));
			//console.log(timeArray.length);
        }});

}

$(document).ready(function () {
    fetchPosts();
    $('#addnew').submit(function () {
        $.ajax({ url: 'addnew', type: 'post', dataType: 'json',
            data: { AA_sen: $('#AA_sen').val(), AA_base: $('#AA_base').val(), AA_zero: $('#AA_zero').val(), AA_span: $('#AA_span').val()  },
            error: function (jqxhr, textStatus, errorThrown) {
                console.log('ERRORerror', textStatus, '//', errorThrown);
            },
            success: function (json) {
            //fetchPosts();
            }});
    });
});

