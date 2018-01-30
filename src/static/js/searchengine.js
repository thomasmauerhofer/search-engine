$(document).ready(function () {
    $("#navbar1").addClass('active').siblings().removeClass('active');


    $(".doc-query").keyup(function (e) {
        setDocQueryError();
    });


    $(".section-query").keyup(function (e) {
        setSectionQueryError(this);
    });

    $("#button-use-pdf").click(function () {
        $("#use-query").hide();
        $("#use-pdf").show();
    });

    $("#button-use-queries").click(function () {
        $("#use-query").show();
        $("#use-pdf").hide();
    });
});


function setDocQueryError() {
    if (!$(".doc-query").val().replace(/(\r\n|\n|\r)/gm, "")) {
        $(".query").removeClass('has-feedback has-error');
        $(".query").children('.control-label').html("");
        return;
    }

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
            } else {
                $(".doc-query").parents('.query').removeClass('has-feedback has-error');
                $(".doc-query").parents('.query').children('.control-label').html("");
                $(textarea).parents('.query').removeClass('has-feedback has-error');
                $(textarea).parents('.query').children('.control-label').html("");
            }
        }
    }
}


function setSectionQueryError(query_field) {
    if ($(query_field).parents('.query').hasClass('has-error') && !query_field.value.replace(/(\r\n|\n|\r)/gm, "")) {
        $(query_field).parents('.query').removeClass('has-feedback has-error');
        $(query_field).parents('.query').children('.control-label').html("");
        $(".doc-query").parents('.query').removeClass('has-feedback has-error');
        $(".doc-query").parents('.query').children('.control-label').html("");
        return;
    }

    var words = removeEmptyFields(query_field.value.replace(/\n/g, " ").split(" "));
    var docQueryWords = removeEmptyFields($(".doc-query").val().replace(/\n/g, " ").split(" "));
    for (var j = 0; j < words.length; j++) {
        if (docQueryWords.includes(words[j])) {
            $(".doc-query").parents('.query').addClass('has-error has-feedback');
            $(".doc-query").parents('.query').children('.control-label').text(words[j] + " is also present in the document-search.");
            $(query_field).parents('.query').addClass('has-error has-feedback');
            $(query_field).parents('.query').children('.control-label').text(words[j] + " is also present in the chapter-search.");
            break;
        } else {

            $(".doc-query").parents('.query').removeClass('has-feedback has-error');
            $(".doc-query").parents('.query').children('.control-label').html("");
            $(query_field).parents('.query').removeClass('has-feedback has-error');
            $(query_field).parents('.query').children('.control-label').html("");
        }
    }
}


function removeEmptyFields(l) {
    var ret = [];
    for (var i = 0; i < l.length; i++) {
        var word = l[i].replace(/(\r\n|\n|\r)/gm, "");
        if (word !== "") {
            ret.push(word.toLowerCase())
        }
    }
    return ret;
}
