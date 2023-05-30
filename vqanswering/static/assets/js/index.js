let me = {};

let you = {};

const micro_div = $("#microphone")
const micro_icon = $("#micro-icon")
navigator.mediaDevices.enumerateDevices()
    .then(function (devices) {
        const audioDevices = devices.filter(function (device) {
            return device.kind === "audioinput";
        });

        if (audioDevices.length > 0) {
            // Microphone is available
            console.log("Microphone is available");
            micro_icon.attr("src", micro_icon_path);
        } else {
            // Microphone is not available
            console.log("Microphone is not available");
            // Set the image source to the inactive microphone image
            micro_icon.attr("src", no_micro_icon_path);
            // Display an alert message to the user
            window.alert("Please activate your microphone or plug in a microphone and refresh this page to use this app.");
        }
    })
    .catch(function (error) {
        // Error occurred while trying to enumerate devices
        console.error("Error occurred while trying to enumerate devices:", error);
    });

function formatAMPM(date) {
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
function insertChat(who, text, time) {
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

function resetChat() {
    $(".chat-ul ul").empty();
}


function goPython(text, p_link) {
    let token = $('input[name="csrfToken"]').attr('value');
    $.ajax({
        type: "POST",
        url: "/handle_chat_question/",
        data: {
            'question': text,
            'url': p_link.toString(),
            'csrfmiddlewaretoken': '{{ csrf_token }}'
        }
    }).done(function (result) {
        let answer = result['answer'].toString()
        insertChat("you", answer, 150);
    });
}


$(".input_text").on("keydown", function (e) {
    if (e.which === 13) {
        const currentUrl = window.location.href;
        console.log('Current URL:', currentUrl);
        let text = $(this).val();
        if (text !== "") {
            insertChat("me", text);
            const answer = goPython($(this).val(), currentUrl)
            $(this).val('');
        }
    }
});


var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition
var SpeechGrammarList = SpeechGrammarList || webkitSpeechGrammarList
var SpeechRecognitionEvent = SpeechRecognitionEvent || webkitSpeechRecognitionEvent

let recognition = new SpeechRecognition();
let speechRecognitionList = new SpeechGrammarList();
recognition.grammars = speechRecognitionList;
recognition.continuous = false;
recognition.lang = 'en-US'//'en-US';

function startRecording() {
    console.log('start');
    micro_icon.addClass("blink-image");

    navigator.mediaDevices.getUserMedia({audio: true})
        .then(function (stream) {
            // Microphone is available and active
            console.log("Microphone is available and active");

            // Stop the stream after 5 seconds
            setTimeout(function () {
                console.log('stop');
                stream.getTracks().forEach(function (track) {
                    track.stop();
                });
                recognition.stop();
                micro_icon.removeClass("blink-image");
            }, 5000);

            // Start recognition
            recognition.start();

            // Handle recognition results
            recognition.onresult = function (event) {
                const currentUrl = window.location.href;
                const question = event.results[0][0].transcript + '?';
                insertChat("me", question);
                const answer = goPython(question, currentUrl)
            };

            // Handle recognition errors
            recognition.onerror = function (event) {
                console.error(event.error);
            };
        })
        .catch(function (error) {
            // Microphone is not available or not active
            console.log("Microphone is not available or not active");
            window.alert("Please activate your microphone or plug in a microphone to use this feature.");
            // Set the image source to the inactive microphone image
            micro_icon.attr("src", no_micro_icon_path);
            micro_icon.removeClass("blink-image");
        });
}

// document.body.onclick
micro_div.click(function () {
    startRecording();
    console.log('Ready to receive a question.');
});

recognition.onresult = function (event) {
    const currentUrl = window.location.href;
    const question = event.results[0][0].transcript + '?';
    insertChat("me", question);
    const answer = goPython(question, currentUrl)
}

recognition.onspeechend = function () {
    recognition.stop();
    console.log('stop recognition')
}


$('body > div > div > div:nth-child(2) > span').click(function () {
    $(".input_text").trigger({type: 'keydown', which: 13, keyCode: 13});
})

//-- Clear Chat
resetChat();

//-- Print Messages
insertChat("you", "Hi! Nice to meet you!", 0);
insertChat("you", "Ask me something about this artwork!", 1500);

//-- NOTE: No use time on insertChat.