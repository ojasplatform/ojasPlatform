$(function(){
    function pageLoad(){

		
		$.getJSON('http://172.16.124.241:5000/getAlerts', function(data) {
			function makeUL(listItem, dateItem) {
				// Create the list element:
				var list = document.createElement('ul');

				for(var i = 0; i < listItem.length; i++) {
					// Create the list item:
					var item = document.createElement('li');
					item.innerHTML = '<span class="icon background-warning">'+
						'<i class="fa fa-exclamation-circle"></i></span>'+
						'<div class="news-item-info">'+
						'<h4 class="name"><a href="#">Data Breach Alert</a></h4><p>'+
						listItem[i]+'</p><div class="time">'+dateItem[i]+'</div>'+
						'</div>'
						;
					// Set its contents:
					//item.appendChild(document.createTextNode(array[i]));
					// Add it to the list:
					list.appendChild(item);
			
				}

				// Finally, return the constructed list:
				return list;
			}
			console.log(data);
			var listitem = [];
			var dateItem = [];
			$(data).each(function(index){
				listitem.push(this.alertType);
				dateItem.push(this.strTime);
			});
			document.getElementById('alert-feed').appendChild(makeUL(listitem, dateItem));
			var min = 0;
			var max = 10;
			// and the formula is:
			var random = Math.floor(Math.random() * (max - min + 1)) + min;
			document.getElementById('unread-notifications').innerHTML = random
		});
		
		$.getJSON('http://172.16.124.241:5000/getEvents', function(data) {
			function makeUL(array1, array2, array3, array4) {
				// Create the list element:
				var list = document.createElement('ul');

				for(var i = 0; i < array1.length; i++) {
					// Create the list item:
					var item = document.createElement('li');
					item.innerHTML = '<span class="icon background-warning">'+
						'<i class="fa fa-eye"></i></span>'+
						'<div class="news-item-info">'+
						'<h4 class="name"><a href="#">'+array1[i]+'</a></h4><p>'+
						array3[i]+'&nbsp &nbsp &nbsp &nbsp Size: &nbsp'+array4[i]+'Bytes</p><div class="time">'+array2[i]+'</div><div class="time">'+
						'</div>'
						;
					// Set its contents:
					//item.appendChild(document.createTextNode(array[i]));
					// Add it to the list:
					list.appendChild(item);
			
				}

				// Finally, return the constructed list:
				return list;
			}
			console.log(data);
			var listitem = [];
			var timeItem = [];
			var methodItem = [];
			var pathItem = [];
			var hostItem = [];
			var lengthItem = [];
			
			$(data).each(function(index){
				listitem.push(this['req-method']);
				timeItem.push(this.strTime);
				pathItem.push(this['req-path'])
				lengthItem.push(this['response-length'])
			});
			document.getElementById('event-feed').appendChild(makeUL(listitem, timeItem, pathItem, lengthItem));
			var min = 0;
			var max = 10;
			// and the formula is:
			var random = Math.floor(Math.random() * (max - min + 1)) + min;
			document.getElementById('unread-notifications-events').innerHTML = random
		});
		
		
	}
    pageLoad();

    PjaxApp.onPageLoad(pageLoad);
});
