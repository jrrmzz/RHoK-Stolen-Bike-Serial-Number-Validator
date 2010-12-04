jQuery(function() {

    var serial_input_text = 'enter serial #';
    $('#serial').val(serial_input_text);
    $('#serial').focus(function() {
       if($(this).val() == serial_input_text) {
           $(this).val(''); // clear input
       }
    });
    $('#serial').blur(function() {
       if($(this).val() == '') {
           $(this).val(serial_input_text); // repopulate input
       }
    });

	$('.answer').toggle();
	$('.question').click(function() {
		$('.answer').slideToggle('fast');
	});
	
	$('#serialText #submit').click(function() {
	  $.POST('checkSerial', function(data) {
        $('.result').html(data);
      });
	  return false;
	});
});
