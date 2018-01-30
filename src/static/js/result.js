$(document).ready(function () {
    setErrors();
});

function setErrors() {
    var words = removeEmptyFields($(".doc-query").val().replace(/\n/g, " ").split(" "));
    var textareas = $(".doc-query").parents('form').children('.query').children('.section-query');

    for (var i = 0; i < textareas.length; i++) {
        var textarea = textareas[i];
        var textareaWords = removeEmptyFields(textarea.value.replace(/\n/g, " ").split(" "));
        if (textarea.value === "") {
            continue;
        }

        for (var j = 0; j < words.length; j++) {
            if (textareaWords.includes(words[j])) {
                $(".doc-query").parents('.query').addClass('has-error has-feedback');
                $(".doc-query").parents('.query').children('.control-label').text(words[j] + " is also present in the chapter-search.");
                $(textarea).parents('.query').addClass('has-error has-feedback');
                $(textarea).parents('.query').children('.control-label').text(words[j] + " is also present in the document-search.");
                break;
            }
        }
    }
}