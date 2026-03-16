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
chat.innerHTML +=
"<div class='bot'><span>"+data.reply+"</span></div>";

chat.scrollTop = chat.scrollHeight;

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
