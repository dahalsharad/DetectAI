function uploadFileAndText() {
    var fileInput = document.getElementById('fileToUpload');
    var file = fileInput.files[0]; // Get the first file selected by the user

    var textInput = document.getElementById('inputText').value;

    var formData = new FormData();
    formData.append('fileToUpload', file);
    formData.append('inputText', textInput);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/process_text/', true);
    xhr.onload = function() {
        if (xhr.status === 200) {
            var response = xhr.responseText;
            document.getElementById('outputText').innerText = response;
        } else {
            console.error('Error:', xhr.statusText);
        }
    };
    xhr.onerror = function() {
        console.error('Request failed');
    };
    xhr.send(formData);
}
