function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $.get("/api/profile/auth", function(data){
        if ("4101" == data.errno) {
            location.href = "/login.html";
        }
        else if ("0" == data.errno) {
            if (data.data.real_name && data.data.id_card) {
                $("#real-name").val(data.data.real_name);
                $("#id-card").val(data.data.id_card);
                $("#real-name").prop("disabled", true);
                $("#id-card").prop("disabled", true);
                $("#form-auth>input[type=submit]").hide();
            } 
        }
    });
    $("#form-auth").submit(function(e){
        e.preventDefault();
        if ($("#real-name").val()=="" || $("#id-card").val() == "") {
            $(".error-msg").show();
        }
        var data = {};
        $(this).serializeArray().map(function(x){data[x.name] = x.value;}); 
        var jsonData = JSON.stringify(data);
        $.ajax({
            url:"/api/profile/auth",
            type:"POST",
            data: jsonData, 
            contentType: "application/json",
            dataType: "json",
            headers:{
                "X-XSRFTOKEN":getCookie("_xsrf"),
            },
            success: function (data) {
                if ("0" == data.errno) {
                    $(".error-msg").hide();
                    showSuccessMsg();
                    $("#real-name").prop("disabled", true);
                    $("#id-card").prop("disabled", true);
                    $("#form-auth>input[type=submit]").hide();
                }
            }
        });
    })

})