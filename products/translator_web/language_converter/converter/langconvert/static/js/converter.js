CKEDITOR.replace('inputText');

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            console.log(cookies[i]);
            const cookie =
                cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function (e) {
    console.log("Page Loaded");
    $.ajax({
        type: "GET",
        url: "getAllLanguages/",
        data: {},
        dataType: "json",
        success: function (response) {
            let allCode = Object.keys(response.language_code);
            let getAllLang = Object.values(response.language_code);
            let str = "";
            let str1 = "";
            str += `<select id="inputTextLang" class="selectBox"> <option value=''>select </option>`
            str1 += `<select id="outputTextLang" class="selectBox" name="dest[]" multiple> <option value=''>select </option>`
            console.log(getAllLang)

            if (allCode.length > 0 && getAllLang.length > 0) {
                for (let i = 0; i < allCode.length; i++) {
                    for (let j = 0; j < getAllLang.length; j++) {
                        if (i == j) {
                            str += `<option value='${allCode[i]}'>${getAllLang[j]}</option>`;
                            str1 += `<option value='${allCode[i]}'>${getAllLang[j]}</option>`;
                        }
                    }
                }
            }
            str += `</select>`;
            str1 += `</select>`;
            $('.leftLang').html(str);
            $('.rightLang').html(str1);

            // Initialize Select2 for the multiselect dropdowns
            $('#inputTextLang, #outputTextLang').select2({
                width: '230px',
                placeholder: 'Languages',
                height: '250px'
            });
        }
    });
});



$("#convertButton").click(function (e) {
    e.preventDefault();
    var editor = CKEDITOR.instances.inputText;
    var inputTextLang = $("#inputTextLang").val();
    var outputTextLang = $("#outputTextLang").val();
    var ckeditortext = editor.getData();
    //var tempElement = document.createElement('div');
    //tempElement.innerHTML = ckeditortext;
    console.log("this ismy inpt::", 'myText:', ckeditortext, 'srcLang:', inputTextLang, 'destLang:', outputTextLang,
        'csrfmiddlewaretoken:', getCookie('csrftoken'))
    // Extract the text content without HTML tags
    //var myText = tempElement.textContent || tempElement.innerText;
    //console.log(myText);
    //console.log(inputTextLang, ' and ', outputTextLang, ' this is lang converter project', myText)
    // ? fetching inputs for translate

    $.ajax({
        type: "POST",
        url: "/",
        data: {
            'myText': ckeditortext,
            'srcLang': inputTextLang,
            'destLang': outputTextLang,
            'csrfmiddlewaretoken': getCookie('csrftoken')
        },
        // headers: {
        // 'csrfmiddlewaretoken': getCookie('csrftoken')
        // },
        dataType: "json",
        success: function (obj) {
            let allConvertCode = Object.keys(obj);
            let allConvertText = Object.values(obj);
            console.log("get response successfully ", obj, allConvertCode, allConvertText);
            if (allConvertCode.length > 0 && allConvertText.length > 0){
            var output = '';
            for (var i = 0; i < allConvertCode.length; i++) {
                for (var j = 0; j < allConvertText.length; j++) {
                    if (i == j) {
                        $('.downloadAll').prop('disabled', false);
                        console.log("HELLO THIS IS RESPONSE::",allConvertCode[i]);
                        // output += `<textarea id="outputText${i}">`;
                        // output += `${allConvertText[j]}`;
                        // output += `</textarea>`;
                        // //output += `<button type="button" onclick="downloadPDF(${i})">Downloadpdf</button>` 
                        // output += `<input type="hidden" id="uniqueCode" value="${allConvertCode[i]}">`
                        // output += `<a href="download-pdf/${allConvertCode[i]}/"><button type="button" >Downloadpdf</button></a>`  


                        output += `<div class="accordion" id="accordionExample">
                                <div class="accordion-item">
                                    <h2 class="accordion-header" id="headingOne">
                                        <button class="accordion-button d-flex flex-row justify-content-between" style="display:flex; flex-direction:row; justify-content:space-between !important; margin-left:0px !important;" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne${allConvertCode[i]}" aria-expanded="true" aria-controls="collapseOne">
                                            <div>
                                                <p id="output-text">${allConvertCode[i]}</p>
                                            </div>
                                            <div style="max-width:5px">
                                                <a href="download-pdf/${allConvertCode[i]}/" style="margin:0px !important;" ><img src="static/img/pdf.svg"/></a>
                                                <button type="button" class="btn btn-primary" onclick="copyText(${i})">Copy</button>
                                            </div>
                                        </button>
                                    </h2>
                                    
                                    <div id="collapseOne${allConvertCode[i]}" class="accordion-collapse collapse" aria-labelledby="headingOne" data-bs-parent="#accordionExample">
                                    <div class="accordion-body" id="textToCopy${i}">
                                        ${allConvertText[j]}
                                         
                                    </div>
                                    </div>
                                </div>
                            </div>`

                    }
                }
            }
            $(".outputText").html(output);
        }
        },
        error: function (xhr, status, error) {
            console.log('AJAX error:', status, error);
        }
    });
});

function copyText(elementId) {
    // alert("elementId "+elementId)
    // var copyText = document.getElementById(elementId);
    // console.log("copyText == "+copyText)
    // copyText.select();
    // document.execCommand('copy');
    // alert('Text copied to clipboard!');

    copyToClipboard("#textToCopy"+elementId);
}


function copyToClipboard(selector) {
    // alert("selector "+selector);
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val($(selector).text()).select();
    document.execCommand("copy");
    $temp.remove();
    // alert("Text copied to clipboard!");
}



$("#subscriptionForm").click(function (e) {
    e.preventDefault();
    // ? fetching inputs for date filter
    var mailid = $("#input-data").val();
    console.log('mailid' + mailid)
    $.ajax({
        type: "POST",
        url: "email/",

        data: {
            'csrfmiddlewaretoken': getCookie('csrftoken'),
            'mailid': mailid,
        },

        dataType: "json",
        success: function (response) {
            console.log(response);
            $("#responseMessage").text(response.detail);
        },
        error: function (error) {
            $("#responseMessage").text(error.responseJSON.detail);
            console.error('Error:', error.responseJSON.detail);
        }
    });
});
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            console.log(cookies[i]);
            const cookie =
                cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}