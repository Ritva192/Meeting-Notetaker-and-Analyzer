$(function(){
	$('#btnschedule').click(function(){
		
		$.ajax({
			url: '/schedule',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
