// Please see documentation at https://docs.microsoft.com/aspnet/core/client-side/bundling-and-minification
// for details on configuring this project to bundle and minify static web assets.

// Write your JavaScript code.

// This routine is activated when the Process Button is pressed.


//Create connection and start it
/*
const connection = new signalR.HubConnectionBuilder()
    .withUrl("/chathub")  //  This is the URL from Startup.cs Configure method for route mapping.We're using the base class here
        .configureLogging(signalR.LogLevel.Information)
        .build();
connection.start().catch(err => console.error(err.toString()));
*/
//var selectTemplateInput = $(document.createElement('input')).attr({ "type": "file", "accept": ".xls*", "id":"templateFile" });
//var selectFolderInput = $(document.createElement('input')).attr({ "type": "file", "accept": ".xls*", "multiple": "" });

/*document.querySelector("button").addEventListener('click', () => {
    document.querySelector('input[type="file"]').click();
    console.log("Button pressed!!");
}); */


// This function allows user to click on button to bring up folder chooser dialog.
$("#SelectFolderButton").click(function () {
    //selectFolderInput = $(document.createElement('input'));
    //selectFolderInput.attr({ "type": "file", "accept": ".xls*" , "multiple":""});
    document.getElementById("studentFileHiddenButton").click();
    
    return false;
}); 

// This function allows user to click on button to bring up template file chooser dialog.
$("#SelectTemplateButton").click(function () {
    //selectTemplateInput = $(document.createElement('input'));
    //selectTemplateInput.attr({ "type": "file", "accept": ".xls*" });
    document.getElementById("templateFileHiddenButton").click();
    
    

    return false;
}); 

$("#templateFileHiddenButton").change(function () {
    if (document.getElementById("templateFileHiddenButton").files.length > 0) {
        $("#templateFileTextBox").html('');
        var input = document.getElementById("templateFileHiddenButton");
        var outputText;
        for (var i = 0; i < input.files.length; ++i) {
            outputText = document.createTextNode("\"" + input.files.item(i).name + "\" ");
            document.getElementById("templateFileTextBox").appendChild(outputText);
        }
    }
})

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$("#studentFileHiddenButton").change(function () {
    if (document.getElementById("studentFileHiddenButton").files.length > 0) {
        $("#studentFileTextBox").html('');
        var input = document.getElementById("studentFileHiddenButton");
        var outputText;
        for (var i = 0; i < input.files.length; ++i) {
            outputText = document.createTextNode("\"" + input.files.item(i).name + "\" ");
            document.getElementById("studentFileTextBox").appendChild(outputText);
        }
    }
})


var csrftoken = getCookie('csrftoken');
/*
//Signal method invoked from server
connection.on("initSignal", ( message) => {
    console.log("We got signal! and the message is: " + message);

    //Update paragraph tag with the message sent
    $("#jobstatus").html(message);

});


*/

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


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

/*

connection.on("ReceiveMessage", function (user, message) {
    //console.log("User=" + user + " and Message=" + message);
    var msg = message.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    var encodedMsg =  msg+"\n";
    var outputText = document.createTextNode(encodedMsg);
    document.getElementById("MYSOutputWindowID").appendChild(outputText);
    var br = document.createElement("br");
    document.getElementById("MYSOutputWindowID").appendChild(br);
    document.getElementById("MYSOutputWindowID").scrollTo(0, document.getElementById("MYSOutputWindowID").scrollHeight);
    
    
}); 

*/

$('input[type=radio][name=mode]').change(function() {
    if (this.value == 'all') {
        UpdateProcessOption(0);
    }
    else if (this.value == 'highlighted') {
        UpdateProcessOption(1);
    }
});


$(document).ready(function () {
    $("#ProcessButton").click(function () {
        //console.log(document.getElementById("studentFileHiddenButton").value);
        //document.getElementById("studentFileHiddenSubmit").click();
        var outputWindow = document.getElementById("MYSOutputWindowID");
        if (outputWindow.hasChildNodes()) {
            while (outputWindow.firstChild) {
                outputWindow.removeChild(outputWindow.lastChild);
            }
        }
        uploadFiles("studentFileHiddenButton", "templateFileHiddenButton");
        //$.post("/Home/OnPostUploadAsync",)
        
        //    
        //});
    
    });
    
    //$("#DownloadButtonId").click(function () {
    //    window.open('');
    //
    //});
});


//function UpdateProcessOption(radio_process_option) {
function UpdateProcessOption(radio_process_option) {

        var numberstring = radio_process_option.toString(10)
        var processOptionResult = { "Result1": numberstring };
        console.log(processOptionResult);
        $.ajax(
            {
                url: "/MYSApp/ProcessOptionChange/",
                data: JSON.stringify(processOptionResult),
                type: "POST",
                contentType: 'application/json; charset=utf-8',
                
                success: function () {

                    console.log("Info sucessfully POSTed");

                }

            });
}
    

function uploadFiles(inputId , inputId2) {
    var input = document.getElementById(inputId);
    var input2 = document.getElementById(inputId2);
    var files = input.files;
    var file2 = input2.files;
    var formData = new FormData();

    for (var i = 0; i != files.length; i++) {
        formData.append("studentFilesToUpload", files[i]);
    }
    formData.append("templateFileToUpload", file2[0]);

    $.ajax(
        {
            url: 'FileUpload/',
            data: formData,
            processData: false,
            contentType: false,
            type: "POST",
            success: function () {
                //alert("Files Uploaded!");
                //addDownloadButton();
                //$("#GetZipFileLink").click();
            }
        }
    );


}


// function a_onClick() {
//     alert('a_onClick');
// }

// function addDownloadButton() {
//     var downloadZipButton = document.createElement("button");
//     downloadZipButton.innerHTML = "Click to download results zip file";
//     downloadZipButton.style.margin = "10px";
//     downloadZipButton.style.height = "64px";
//     downloadZipButton.style.width = "150px";
//     downloadZipButton.id = "DownloadButtonId";
//     //downloadZipButton.style.display = "";
//     downloadZipButton.onclick = function () {
//         window.open('/Home/GetZipFile');

//     }

//     // 2. Append somewhere
//     var body = document.getElementById("MYSOutputWindowID");
//     body.appendChild(downloadZipButton);
//     document.getElementById("MYSOutputWindowID").scrollTo(0, document.getElementById("MYSOutputWindowID").scrollHeight);

    
    
// }



