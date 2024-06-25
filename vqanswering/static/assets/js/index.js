const me = {};
const you = {};

let userLang = navigator.language ;//|| navigator.userLanguage

let userLanguageName = 'English (United Kingdom)';

const formatAMPM = (date) => {
    let hours = date.getHours();
    let minutes = date.getMinutes();
    let ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0' + minutes : minutes;
    let strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
}

//-- No use time. It is a javaScript effect.
const insertChat = (who, text, time = 0) => {
    if (time === undefined) {
        time = 0;
    }
    let control = "";
    let date = formatAMPM(new Date());
    if (who === "you") {
        control = '<li style="width:100%">' +
            '<div class="msj macro">' +
            '<div class="text">' +
            '<p class="text-l">' + text + '</p>' +
            '<p>' + date + '</p>' +
            '</div>' +
            '</div>' +
            '</li>';
    } else {
        control = '<li style="width:100%;">' +
            '<div class="msj-rta macro">' +
            '<div class="text">' +
            '<p class="text-r">' + text + '</p>' +
            '<p>' + date + '</p>' +
            '</div>' +
            '</li>';
    }

    setTimeout(
        function () {
            $(".chat-ul ul").append(control).scrollTop($(".chat-ul ul").prop('scrollHeight'));
        }, time);

}

const resetChat = () => {
    $(".chat-ul ul").empty();
}

const goPython = (text, p_link) => {
    const token = $('input[name="csrfToken"]').attr('value');
    console.log(userLanguageName, userLang)
    $.ajax({
        type: "POST",
        url: "/handle_chat_question/",
        data: {
            'question': text,
            'language': userLang, // userLanguageName
            'url': p_link.toString(),
            'csrfmiddlewaretoken': token
        }
    }).done(result => {
        const answer = result['answer'].toString();
        insertChat("you", answer, 150);
    }).fail((jqXHR, textStatus, errorThrown) => {
        console.error("Request failed: " + textStatus + ", " + errorThrown);
        window.alert("An error occurred while processing your request. Please try again.");
    });
};

document.getElementById('mobile-chat-button').addEventListener('click', function() {
    const currentUrl = window.location.href;
    let text = document.querySelector(".input_text").value;
    if (text !== "") {
        insertChat("me", text);
        goPython(text, currentUrl)
        document.querySelector(".input_text").value = '';
    }
});
$(".input_text").on("keydown", function (e) {
    if (e.which === 13) {
        const currentUrl = window.location.href;
        console.log('Current URL:', currentUrl);
        let text = $(this).val();
        if (text !== "") {
            insertChat("me", text);
            goPython($(this).val(), currentUrl)
            $(this).val('');
        }
    }
});

$('body > div > div > div:nth-child(2) > span').click(function () {
    $(".input_text").trigger({type: 'keydown', which: 13, keyCode: 13});
})

//-- Clear Chat
resetChat();

//-- Print Messages
insertChat("you", "Hi! Nice to meet you!", 0);
insertChat("you", "Ask me something about this artwork!", 1500);

