$(function(){
	$('#regbutton').click(function(){
		
		$.ajax({
			url: '/register',
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