function myFunction() {
    /* Get the text field */
    var copyText = document.getElementById("myInput");
  
    /* Select the text field */
    copyText.select();
    copyText.setSelectionRange(0, 99999); /* For mobile devices */
  
    /* Copy the text inside the text field */
    document.execCommand("copy");
  
    /* Alert the copied text */
  }



function readURL2(input) {
    if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function (e) {
    
        $('#yt_link').val(input.files[0].name);
        $('#blah').attr('src', e.target.result).width(500).height(550);
    };
    reader.readAsDataURL(input.files[0]);
    }
}


$(document).ready(function () {
    $("#downloadimg",).click(function (e) {
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
            let url = "/get-text/extract-text";
            $.ajax({
                url: url,
                type: 'POST',
                processData: false,
                enctype: 'multipart/form-data',
                contentType: false,
                data: formdata,
                
                success: function (data) {
                    if (data.status == true){
                        $('#blah2').attr("src", data.filename).width(500).height(550);
                        $('#myInput').text(data.result);
                        $('#textarea').css('display','block' );
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
