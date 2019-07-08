$("#idForm").submit(function(e) {
    alert("HI");
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');
	alert(form.serialize());
    $.ajax({
           type: "GET",
           url: 'http://35.199.58.182/price',
           data: form.serialize(), // serializes the form's elements.
           success: function(data)
           {
               alert(data); // show response from the php script.
	       console.log(data);
           },
           fail: function( jqXHR, textStatus ) 
           {
              alert( "Request failed: " + textStatus );
		   }
         });


});
function addRow(price,size,url){
	$('#table_body').append('<tr><td>'+price+'</td><td>'+size+'</td><td><a href="'+url+'">'+url+'</a></td></tr>');
}
function clearTable(){
	$('#table_body').empty();
}
addRow('100','1mg','http://www.neverssl.com');
