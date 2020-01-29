
google.charts.load('current', {'packages':['timeline']});
google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        var container = document.getElementById('timeline');
    var chart = new google.visualization.Timeline(container);
    var dataTable = new google.visualization.DataTable();


    dataTable.addColumn({ type: 'string', id: 'Project' });
    dataTable.addColumn({ type: 'string', id: 'Event' });
    dataTable.addColumn({ type: 'date', id: 'Start' });
    dataTable.addColumn({ type: 'date', id: 'End' });

    dataTable.addRows([
[ '\0','Now', new Date(), new Date() ],
[ '\0','VAC', new Date(2020, 3, 17), new Date(2020, 3, 30) ],
[ 'INT','P-1 (10/01)', new Date(2019, 9, 01), new Date(2019, 9, 01) ],
[ 'INT','P-2 (11/20)', new Date(2019, 10, 20), new Date(2019, 10, 20) ],
[ 'INT','OS-1 (1/27)', new Date(2020, 0, 27), new Date(2020, 0, 27) ],
[ 'PREP','P-1 (9/30)', new Date(2019, 8, 30), new Date(2019, 8, 30) ],
[ 'PREP','P-2 (11/19)', new Date(2019, 10, 19), new Date(2019, 10, 19) ]
]);


    var options = {
      timeline: {    colorByRowLabel : 'True',
                     groupByRowLabel : 'True',
                     rowLabelStyle: {fontName: 'Helvetica', fontSize: 8, color: '#603913' },
                     barLabelStyle: { fontName: 'Garamond', fontSize: 8 } }
    };

     chart.draw(dataTable, options);

     nowLine('timeline');

     google.visualization.events.addListener(chart, 'onmouseover', function(obj){
  	    if(obj.row == 0){
    	   $('.google-visualization-tooltip').css('display', 'none');
		}
        nowLine('timeline');
     })

     google.visualization.events.addListener(chart, 'onmouseout', function(obj){
  	   nowLine('timeline');
     })

}

function nowLine(div){
//get the height of the timeline div
	var height;
    $('#' + div + ' rect').each(function(index){
  	  var x = parseFloat($(this).attr('x'));
      var y = parseFloat($(this).attr('y'));

      if(x == 0 && y == 0) {height = parseFloat($(this).attr('height'))}
  })

var VACWord = $('#' + div + ' text:contains("VAC")');
VACWord.prev().first().attr('height', height + 'px').attr('y', '0');   
var NowWord = $('#' + div + ' text:contains("Now")');
NowWord.prev().first().attr('height', height + 'px').attr('y', '0');  
}