$(function(){
	$('#btnLogin').click(function(){
		
		$.ajax({
			url: '/ValidateOrgLogin',
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