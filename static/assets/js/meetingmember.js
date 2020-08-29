
$(function(){
	$('#btnmember').click(function(){
		
		$.ajax({
			url: '/meetingmember',
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
