function send(){

let text=document.getElementById("msg").value

fetch("/get_response",{

method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({message:text})

})

.then(res=>res.json())
.then(data=>{

let box=document.getElementById("chatbox")

box.innerHTML+=`<p class="user">${text}</p>`
box.innerHTML+=`<p class="bot">${data.reply}</p>`

})

}


function voice(){

let rec=new webkitSpeechRecognition()

rec.onresult=function(e){

document.getElementById("msg").value=
e.results[0][0].transcript

send()

}

rec.start()

}
function sendMessage() {

let userText = document.getElementById("userInput").value;

let chatBox = document.getElementById("chatBox");

chatBox.innerHTML += "<p><b>You:</b> " + userText + "</p>";

fetch("/chat", {
method: "POST",
headers: {
"Content-Type": "application/json"
},
body: JSON.stringify({message:userText})
})
.then(response => response.json())
.then(data => {

chatBox.innerHTML += "<p><b>Bot:</b> " + data.reply + "</p>";

});

document.getElementById("userInput").value = "";

}
