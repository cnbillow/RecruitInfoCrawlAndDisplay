/**
 * Created by Cary on 2016/12/11.
 */
function selChange(){
    var val = $('.form-control').val();
    $.ajax({
        url:"/display/",
        type:"POST",
        async:true,
        data:{'choose' : val},
        success : function(data) {
            $('#display').html(data);
        },
    });
}
