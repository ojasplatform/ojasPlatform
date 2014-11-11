var graph = new joint.dia.Graph;

var paper = new joint.dia.Paper({
    el: $('#paper'),
    width: 800,
    height: 400,
    gridSize: 1,
    model: graph
});

var erd = joint.shapes.erd;

var element = function(elm, x, y, label) {
    var cell = new elm({ position: { x: x, y: y }, size: { width: 100, height: 30 },
	      attrs: { text: { text: label }}});
	
	cell.attr({
		  rect: { fill: '#2C3E50', rx: 5, ry: 5, 'stroke-width': 2, stroke: 'black' },
	      text: {
	          fill: '#3498DB',
	          'font-size': 18, 'font-weight': 'bold', 'font-variant': 'small-caps', 'text-transform': 'capitalize'
	      }
	  });
	
    graph.addCell(cell);
    return cell;
};



var link = function(elm1, elm2) {
    var myLink = new erd.Line({ source: { id: elm1.id }, target: { id: elm2.id }});
    graph.addCell(myLink);
	myLink.attr({
	    '.connection': { stroke: 'White' },
	    '.marker-source': { fill: 'None' },
	    '.marker-target': { fill: 'White', d: 'M 10 0 L 0 5 L 10 10 z' },
		'.marker-arrowheads' : { fill: 'None'},
	});
	myLink.label(0, {
	    position: .5,
	    attrs: {
	        rect: { fill: 'Black' },
	        text: { fill: 'blue', text: 'my label' }
			
	    }
	});
	
    return myLink;
};

/* var employee = element(erd.Entity, 100, 200, "Switch");
var salesman = element(erd.Entity, 100, 400, "Salesman");
var wage = element(erd.WeakEntity, 530, 200, "Wage");
var paid = element(erd.IdentifyingRelationship, 350, 190, "gets paid");
var isa = element(erd.ISA, 125, 300, "ISA");
var number = element(erd.Key, 0, 90, "number");
var nameEl = element(erd.Normal, 75, 30, "name");
var skills = element(erd.Multivalued, 150, 90, "skills");
var amount = element(erd.Derived, 440, 80, "amount");
var date = element(erd.Normal, 590, 80, "date");
var plate = element(erd.Key, 405, 500, "plate");
var car = element(erd.Entity, 430, 400, "Company car");
var uses = element(erd.Relationship, 300, 390, "uses"); */


/* link(employee, paid).cardinality('1');
link(employee, number);
link(employee, nameEl);
link(employee, skills);
link(employee, isa);
link(isa, salesman);
link(salesman, uses).cardinality('0..1');;
link(car, uses).cardinality('1..1');
link(car, plate);
link(wage, paid).cardinality('N');
link(wage, amount);
link(wage, date); */

switchlist = {};
url = "http://tap-test.t-labs.us:8080"
//Get the switches from the topology info

function drawLinks(){
	console.log("Got list of switchs"+switchlist);
	srcPort = {};
	dstPort = {};
	srcSwitch = {}; 
	dstSwitch = {};
	$.getJSON("http://tap-test.t-labs.us:8080/v1.0/topology/links", function(links){
	    $.each(links, function(key, value){
		var valueJson = JSON.stringify(value);
        var obj = JSON.parse(valueJson);
		var switchname = obj.src.name.split('-')[0];
		var portname = obj.src.name.split('-')[1];
		srcPort.key = obj.src.port_no;
		dstPort.key = obj.dst.port_no;
		srcSwitch.key = obj.src.name.split('-')[0];
		dstSwitch.key = obj.dst.name.split('-')[0];
		link(switchlist[srcSwitch.key], switchlist[dstSwitch.key]).cardinality(portname);
		});
	});
}

$.getJSON("http://tap-test.t-labs.us:8080/v1.0/topology/switches", function(switches){
	var counter = 0;
    $.each(switches, function(key, value){
		//switchlist.count = ++counter++;		
		var valueJson = JSON.stringify(value);
        var obj = JSON.parse(valueJson);
		var switchname = obj.ports[0].name.split('-')[0];
		switchlist[switchname] = element(joint.shapes.basic.Rect, 200+(key*200), 100, switchname);		
		console.log("1st"+switchlist[switchname]);
    });	
}).then(drawLinks);

