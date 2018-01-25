$(document).ready(function () {
    $("#navbar1").addClass('active').siblings().removeClass('active');


    $(".doc-query").keyup(function (e) {
        if (!this.value.replace(/(\r\n|\n|\r)/gm, "")) {
            $(".query").removeClass('has-feedback has-error');
            $(".query").children('.control-label').html("");
            return;
        }

        var words = removeEmptyFields(this.value.replace( /\n/g, " " ).split( " " ));
        var textareas = $(this).parents('form').children('.query').children('.section-query');
        for (var i = 0; i < textareas.length; i++) {
            var textarea = textareas[i];
            if (textarea.value === "") {
                continue;
            }

            for (var j = 0; j < words.length; j++) {
                if (textarea.value.indexOf(words[j]) !== -1) {
                    $(this).parents('.query').addClass('has-error has-feedback');
                    $(this).parents('.query').children('.control-label').text(words[j] + " is also present in the chapter-search");
                    $(textarea).parents('.query').addClass('has-error has-feedback');
                    $(textarea).parents('.query').children('.control-label').text(words[j] + " is also present in the document-search");
                    break;
                } else {
                    $(this).parents('.query').removeClass('has-feedback has-error');
                    $(this).parents('.query').children('.control-label').html("");
                    $(textarea).parents('.query').removeClass('has-feedback has-error');
                    $(textarea).parents('.query').children('.control-label').html("");
                }
            }
        }
    });
});

function removeEmptyFields(l) {
    var ret = [];
    for (var i = 0; i < l.length; i++) {
        var word = l[i].replace(/(\r\n|\n|\r)/gm, "");
        if(word !== "") {
            ret.push(word)
        }
    }
    return ret;
}
