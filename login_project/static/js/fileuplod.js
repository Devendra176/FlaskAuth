function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        console.log(reader.onload);
        reader.onload = function (e) {
            $('#yt_link').val(input.files[0].name);

        };

        reader.readAsDataURL(input.files[0]);
    }
}

function getFile() {
    document.getElementById("upfile").click();
}




$(document).ready(function () {
    $("#download",).click(function (e) {
        e.preventDefault();
        formdata = new FormData();
        var file_name = $('input[name=file_name]')[0].files[0];
        
        if (file_name) {
            formdata.append("file_name", file_name);
        }

        if (file_name == undefined) {
            console.log("Please enter video file");
        }
        else {
            let url = "/download/auido";
            $.ajax({
                url: url,
                type: 'POST',
                processData: false,
                enctype: 'multipart/form-data',
                contentType: false,
                data: formdata,
                
                success: function (data) {
                    if (data.status == true){
                        $('#div_link').show();
                        $('#new_link').attr("href", data.output);
                        console.log(data)
                    } else if (data.status == false) {
                        $('#danger').text("Error while exracting use other video");

                    } else {
                        console.log(" sever failed  ")
                    }
                },
            });
        }

    });
});

$(document).ready(function () {
    $("#wifi_qr",).click(function (e) {
        e.preventDefault();

        let wifi_name = $('#wifi_name').val();
        let hid = $('#hid').val();
        let password = $('#password').val();
        var encryption = $("input[name='inlineRadioOptions']:checked").val();
        formdata={wifi_name:wifi_name,password:password,hid:hid ,encryption:encryption}
        if (wifi_name == "") {
            console.log("Please enter video file");
        }

        if (password == "") {
            console.log("Please enter video file");
        }
        // if (hidden) {
        //     formdata.append("hidden", hidden);
        // }
       
        else {
            let url = "/download/wifi_qr";
            $.ajax({
                url: url,
                type: 'POST',
                data: formdata,
                success: function (data) {
                    
                    if (data.status == true){
                        $('#div_link').show();
                        $('#gen').hide();
                        $('#new').attr("href", data.output);
                        $('#new').attr("download", data.file_name);
                        $('#new_link').attr("src", data.output);
                        // $('#new_link').attr("alt", data.file_name);
                        console.log(data)
                    } else if (data.status == false) {
                       $('#danger').text("Error");

                    } else {
                        console.log(" sever failed  ")
                    }
                },
            });
        }

    });
}); 