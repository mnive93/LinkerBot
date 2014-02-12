$(document).ready(function() {
	$(".follow_button").click(function(){
		topic = this.id;
		val = $(".follow_button").val();
		$.ajax( url="/accounts/followtopic/"+topic, success = function(){})
		
		if(val == "Follow"){
            $(this).val("Unfollow");
            $(this).addClass("followed");
        }
        else{
            $(this).val("Follow");
            $(this).removeClass("followed");
        }
	});
});
