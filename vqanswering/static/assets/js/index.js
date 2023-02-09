var me = {};

me.avatar = "https://i.postimg.cc/JzKLLD8Z/AI.png";

var you = {};
you.avatar = "https://i.postimg.cc/SssHqDdp/Y.png";

function formatAMPM(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
}            


//-- No use time. It is a javaScript effect.
function insertChat(who, text, time){
    if (time === undefined){
        time = 0;
    }
    var control = "";
    var date = formatAMPM(new Date());
    if (who == "you"){
        control = '<li style="width:100%">' +
                        '<div class="msj macro">' +
                            '<div class="text">' +
                                '<p class="text-l">'+ text +'</p>' +
                                '<p>'+date+'</p>' +
                            '</div>' +
                        '</div>' +
                    '</li>';                    
    }else{
        control = '<li style="width:100%;">' +
                        '<div class="msj-rta macro">' +
                            '<div class="text text-r">' +
                                '<p class="text-r-2">'+text+'</p>' +
                                '<p>'+date+'</p>' +
                            '</div>' +
                  '</li>';
    }


    setTimeout(
        function(){                        
            $(".chat-ul ul").append(control).scrollTop($(".chat-ul ul").prop('scrollHeight'));
        }, time);
    
}

function resetChat(){
    $(".chat-ul ul").empty();
}


function goPython(text, p_link){
            var token =  $('input[name="csrfToken"]').attr('value');
            $.ajax({
                type: "POST",
              url: "/handle_chat_question/",
             //context: {'data': $(".mytext").val()}
                data: {
                    'question': text,
                    'img': p_link.toString(),
                'csrfmiddlewaretoken': '{{ csrf_token }}'}
            }).done(function(result) {
                console.log(result)
                insertChat("you", result['answer'], 1500);
            });
        }

$(".mytext").on("keydown", function(e){
    if (e.which == 13){
        var link = document.querySelector("#painting_link")
        var text = $(this).val();
        if (text !== ""){
            insertChat("me", text);
            var answer = goPython($(this).val(), link.src)
            $(this).val('');
        }
        //console.log(answer)
    }
});


var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition
var SpeechGrammarList = SpeechGrammarList || webkitSpeechGrammarList
var SpeechRecognitionEvent = SpeechRecognitionEvent || webkitSpeechRecognitionEvent

var recognition = new SpeechRecognition();
var speechRecognitionList = new SpeechGrammarList();
recognition.grammars = speechRecognitionList;
recognition.continuous = false;
recognition.lang = 'en-US'//'en-US';

document.body.onclick = function() {
  recognition.start();
  console.log('Ready to receive a question.');
}

recognition.onresult = function(event) {
  // The SpeechRecognitionEvent results property returns a SpeechRecognitionResultList object
  // The SpeechRecognitionResultList object contains SpeechRecognitionResult objects.
  // It has a getter so it can be accessed like an array
  // The first [0] returns the SpeechRecognitionResult at the last position.
  // Each SpeechRecognitionResult object contains SpeechRecognitionAlternative objects that contain individual results.
  // These also have getters so they can be accessed like arrays.
  // The second [0] returns the SpeechRecognitionAlternative at position 0.
  // We then return the transcript property of the SpeechRecognitionAlternative object
    var link = document.querySelector("#painting_link")
    var question = event.results[0][0].transcript + '?';
    console.log(question)
    insertChat("me", question);
            var answer = goPython(question, link.src)
            //$(".mytext").val('');
  //diagnostic.textContent = 'Result received: ' + color + '.';
  //bg.style.backgroundColor = color;
}

recognition.onspeechend = function() {
  recognition.stop();
}


$('body > div > div > div:nth-child(2) > span').click(function(){
    $(".mytext").trigger({type: 'keydown', which: 13, keyCode: 13});
})

//-- Clear Chat
resetChat();

//-- Print Messages
// insertChat("you", "Hi! Nice to meet you!", 0);
// insertChat("you", "Ask me something about the painting!", 1500);
insertChat("you", "Hi! Nice to meet you!", 0);
insertChat("you", "Ask me something about the painting!", 1500);
//insertChat("me", "Who is the author?", 2000);
//insertChat("you", "Banksy", 2500);
//insertChat("me", "What color is the balloon?", 3000);
//insertChat("you", "red", 3500);
//insertChat("me", "how many people are in the image?", 4000);
//insertChat("you", "1", 4500);
//insertChat("me", "how many people are in the image?", 5000);
//insertChat("you", "1", 5500);
//-- NOTE: No use time on insertChat.