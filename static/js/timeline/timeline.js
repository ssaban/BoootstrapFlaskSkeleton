
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
[ 'NEW','P1 (1/01)', new Date(2020, 0, 01), new Date(2020, 0, 01) ]
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


}