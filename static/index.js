

document.addEventListener('DOMContentLoaded',() => {

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on("connect", () => {
        document.querySelector('#messagebutton').onclick = function () {
            const selection = document.querySelector('#textmessage').value;
            socket.emit('submit message', {'selection': selection });
        }});


    socket.on('announce message', data => {
        sessionStorage.setItem("username", `${data.user}`);
        sessionStorage.setItem("channelname", `${data.channel}`);
        if (sessionStorage.getItem("channelname") == document.querySelector("#welcome1").innerHTML)
        {
        const li = document.createElement('li');
        li.style.listStyle = "none";
        li.innerHTML ="<span>" + `${data.user}` + "</span>" + "<p>" + ` ${data.selection} `+ "</p>"+ '<span class="time_date">' +`${data.time}`+ '</span>';
        if (sessionStorage.getItem("username") == document.querySelector("#welcome").innerHTML)
        {
            li.className = "received_withd_msg"
            li.style.float = "left"
        }
        else
        {
            li.className = "received_withd_msg"
            li.style.float = "right"
            li.style.color = "red"
        }
        document.querySelector('#ah').append(li);
    }});
});