function getCookie(name) {
	    var cookieValue = null;
	    if (document.cookie && document.cookie != '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	}

	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
	            // Only send the token to relative URLs i.e. locally.
	            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	        }
	    }
	});

	wsstart();

	function wsstart(){
		chat_socket = new WebSocket("ws://"+window.location.host+"/chat/");
		$('.chat-error').slideUp();
			chat_socket.onmessage = function(event){
			// var msg = event.data;
		 //    if (msg == '__pong__') {
		 //        pong();
		 //        return;
		 //    }
			var data = JSON.parse(event.data);
			var chatdiv = $('#chat-'+data.id);
			// console.log(data);
			chatdiv.append(data.html);
			document.getElementById('message-'+data.message_id).scrollIntoView();
			// chatdiv.append("<li class='self'><div class='msg'><p>"+data.message+"</p><time>"+Date.now()+"</time></div></li>");
		}
		// var tm;
		// function ping() {
		// 	tm = setTimeout( warning, 5000);
		// 	try{
		//         chat_socket.send('__ping__');
		//     }
		//     catch(exc){
		//     	warning();
		//     }
		        
		// }

		// function pong() {
		//     clearTimeout(tm);
		// }
		
		chat_socket.onopen = function(event){
			$('.chat-error').slideUp();
			// setInterval(ping, 10000);
		}


		chat_socket.onclose = warning;
	}

	$('#reconnect').click(warning);

	function warning(){
		var errordiv = $('.chat-error');
		var error = $('.chat-error-text');
		error.text("Unable to connect to servers :/ ");
		errordiv.slideDown();
		chat_socket=null;
		setTimeout(wsstart, 10000);
	}

	


	$('.message-form').submit(function(event){
		event.preventDefault();
		var form = new FormData(this);
		var id = $(this).attr("data");
		var url = $(this).attr('action');
		var text = $("#chat-input-"+id).val();
		// console.log($("input[name='csrfmiddlewaretoken']").attr('value'));
		if($.trim(text).length != 0 || $('#file-input-'+id).val()!="" || $('#image-input-'+id).val()!="" ){
			$.ajax({
				type: "POST",
				url: url,
				data: form,
		        success: function (data) {
					$("#chat-input-"+id).val("");
					$('#file-input-'+id).val("");
					$('#image-input-'+id).val("");
					$("#img-count-"+id).html("");
					$("#img-count-"+id).hide();
					$("#file-count-"+id).html("");
					$("#file-count-"+id).hide();
		        },
		        error: function (data) {
		            alert("error"+data)
		        },
		        cache: false,
		        contentType: false,
		        processData: false,
			});
			// $.post(url, form, function(data){alert(data);});
		}
	});

	$(".chat-menu").click(function(e){
		e.preventDefault();
	});

	$('.menu').click(function(e){
		var id = $(this).attr("data");
		$("#chat-"+id).slideToggle();
		$(".message-form-"+id).slideToggle();
	});

	$('.chat-file-btn').click(function(e){
		var id = $(this).attr("data");
		$('#file-input-'+id).trigger("click");
	});

	$('.chat-image-btn').click(function(e){
		var id = $(this).attr("data");
		$('#image-input-'+id).trigger("click");
	});

	$('.chat-input').keyup(function (event) {
		var id = $(this).attr('data');
    	if (event.keyCode == 13 & !event.shiftKey) {          
            $('.message-form-'+id).submit();
    	}
	});

	var ValidImageTypes = ["image/gif", "image/jpeg", "image/png"];

	$('.chat-image-input').change(function(e){
		var id = $(this).attr('data');
		var boolsize = true, booltype = true;
		for(i=0; i < e.target.files.length; i++){
			var fl = e.target.files[i];
			if ((fl.size/(1024*1024)) > 10)
				boolsize = false;

			if($.inArray(fl["type"], ValidImageTypes) < 0)
				booltype = false
		}
		if(!boolsize)
		{
			image.val("");
			alert("Upload image size should be below 10 Mb");
		}
		else if(!booltype)
		{
			image.val("");
			alert("Uploaded image should be among "+ValidImageTypes);
		}
		if(e.target.files.length>0)
		{
			$("#img-count-"+id).show();
			$("#img-count-"+id).html(e.target.files.length);
		}
		else
			$("#img-count-"+id).hide();
	});

	$('.chat-file-input').change(function(e){
		var boolsize = true;
		var id = $(this).attr('data');
		for(i=0; i < e.target.files.length; i++){
			var fl = e.target.files[i];
			if ((fl.size/(1024*1024)) > 25)
				boolsize = false;
		}
		if(!boolsize)
		{
			file.val("");
			alert("Upload file size should be below 25 Mb");
		}
		if(e.target.files.length>0)
		{
			$("#file-count-"+id).show();
			$("#file-count-"+id).html(e.target.files.length);
		}
		else
			$("#file-count-"+id).hide();
	});

	$(document).ready(function(event){
		$(".chat").animate({ scrollTop: 9999 }, 1000);
		$(".chat-error").hide();
	});

	$(".load-more").click(function(e){
		var loadbtn = $(this);
		var data_id = $(this).attr('data-id');
		var url = $(this).attr('action');
		$.ajax({
			type: "POST",
			url: url,
			data: {"message_id":data_id},
			success: function (data) {
				var dat = JSON.parse(data);
					if(dat.success==true)
					{
						loadbtn.after(dat.html);
						document.getElementById('message-'+data_id).scrollIntoView();
						if(dat.last_id==-1){
							loadbtn.remove();
						}
						else{
							loadbtn.attr("data-id",dat.last_id);
						}
					}
					else{
						console.log(dat.html);
					}
		        },
		        error: function (data) {
		            console.log("error"+data)
		        },

		});
	});