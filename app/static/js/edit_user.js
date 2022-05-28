$(document).ready(function(){
    hiddenValue = $('#text').attr('type','hidden')
    if (hiddenValue.val()  == $('#gender-0').val()){
        $('#gender-0').prop("checked", true);
    }else {
        $('#gender-1').prop("checked", true);
    }
});