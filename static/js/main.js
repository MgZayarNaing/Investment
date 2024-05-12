/**
 * Variables
 */

let chatName = ''
let chatSocket = null
let chatWindowUrl = window.location.href
let chatRoomUuid = Math.random().toString(36).slice(2, 12)


/**
 * Elements
 */

const chatElement = document.querySelector('#chat')
const chatOpenElement = document.querySelector('#chat_open')
const chatJoinElement = document.querySelector('#chat_join')
const chatIconElement = document.querySelector('#chat_icon')
const chatWelcomeElement = document.querySelector('#chat_welcome')
const chatRoomElement = document.querySelector('#chat_room')
const chatNameElement = document.querySelector('#chat_name')
const chatLogElement = document.querySelector('#chat_log')
const chatInputElement = document.querySelector('#chat_message_input')
const chatSubmitElement = document.querySelector('#chat_message_submit')


/**
 * Functions 
 */

function scrollToBottom() {
    chatLogElement.scrollTop = chatLogElement.scrollHeight
}


function getCookie(name) {
    var cookieValue = null

    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';')

        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim()

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))

                break
            }
        }
    }

    return cookieValue
}


function sendMessage() {
    chatSocket.send(JSON.stringify({
        'type': 'message',
        'message': chatInputElement.value,
        'name': chatName
    }))

    chatInputElement.value = ''
}


function onChatMessage(data) {
    console.log('onChatMessage', data)

    if (data.type == 'chat_message') {
        let tmpInfo = document.querySelector('.tmp-info')

        if (tmpInfo) {
            tmpInfo.remove()
        }

        if (data.agent) {
            chatLogElement.innerHTML += `
                                        <div style="display: flex;margin-top: 0.5rem; width: 100%;justify-content:flex-start;  max-width: 25rem;gap:1rem;flex-direction:column">
                                                                        
                                            <div style="display:flex;gap:1rem;justify-content:left;align-items:center;">
                                                <p style="color:#fff;background:#000;border-radius:50%;padding:1rem;"> ${data.initials}</p>
                                                <p style="line-height:1rem;max-width:15rem;padding:1rem;background:skyblue;border-top-right-radius:1rem;border-bottom-right-radius:1rem;border-bottom-left-radius:1rem;text-transform:none;font-size:.9rem;">${data.message}</p>
                                            </div>
                                            <div style="display:flex;gap:1rem;justify-content:space-between;align-items:center;">
                                                <span style="color:#000000;font-size:.7rem;padding-left:4rem;">${data.created_at} ago</span>
                                            </div>

                                        </div>
                                        `
        } else {
            chatLogElement.innerHTML += `
                                        <div style="display: flex;margin-top: 0.5rem; width: 100%;  max-width: 25rem; justify-content:flex-end;gap:.5rem;flex-direction:column">
                                        
                                            <div style="display:flex;gap:1rem;justify-content:right;align-items:center;">
                                                <p style="line-height:1rem;max-width:15rem;padding:1rem;background:skyblue;border-top-left-radius:1rem;border-bottom-right-radius:1rem;border-bottom-left-radius:1rem;text-transform:none;font-size:.9rem;">${data.message}</p>
                                                <p style="color:#fff;background:#000;border-radius:50%;padding:1rem;"> ${data.initials}</p>
                                            </div>
                                            <div style="display:flex;gap:.5rem;justify-content:right;align-items:center;">
                                               
                                                <span style="color:#000000;font-size:.7rem;padding-right:4rem;">${data.created_at} ago</span>
                                                
                                            </div>

                                        </div>
                                        `
        }
    } else if (data.type == 'users_update') {
        chatLogElement.innerHTML += '<p style="font-size:.8rem;color:#000; text-transform:none;margin:1rem 0;">The admin/agent has joined the chat!'
    } else if (data.type == 'writing_active') {
        if (data.agent) {
            let tmpInfo = document.querySelector('.tmp-info')

            if (tmpInfo) {
                tmpInfo.remove()
            }

            chatLogElement.innerHTML += `
                                        <div style="display: flex;margin-top: 0.5rem; width: 100%;justify-content:flex-start;  max-width: 25rem;gap:1rem;flex-direction:column">
                                                                        
                                            <div style="display:flex;gap:1rem;justify-content:left;align-items:center;">
                                                <p style="color:#fff;background:#000;border-radius:50%;padding:1rem;"> ${data.initials}</p>
                                                <p style="line-height:1rem;max-width:15rem;padding:1rem;background:gray;border-top-right-radius:1rem;border-bottom-right-radius:1rem;border-bottom-left-radius:1rem;text-transform:none;font-size:.9rem;">The admin/replier is writing a message.</p>
                                            </div>

                                        </div>
                                        `
        }
    }

    scrollToBottom()
}


async function joinChatRoom() {
    console.log('joinChatRoom')

    chatName = chatNameElement.value

    console.log('Join as:', chatName)
    console.log('Room uuid:', chatRoomUuid)

    const data = new FormData()
    data.append('name', chatName)
    data.append('url', chatWindowUrl)

    await fetch(`/chat/api/create-room/${chatRoomUuid}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: data
    })
        .then(function (res) {
            return res.json()
        })
        .then(function (data) {
            console.log('data', data)
        })


    chatSocket = new WebSocket(`ws://${window.location.host}/ws/${chatRoomUuid}/`)


    chatSocket.onmessage = function (e) {
        console.log('onMessage')

        onChatMessage(JSON.parse(e.data))
    }


    chatSocket.onopen = function (e) {
        console.log('onOpen - chat socket was opened')

        scrollToBottom()
    }


    chatSocket.onclose = function (e) {

        console.log('onClose - chat socket was closed')
    }
}


/**
 * Event listeners
 */

chatOpenElement.onclick = function (e) {
    e.preventDefault()

    chatIconElement.classList.add('hidden')
    chatWelcomeElement.classList.remove('hidden')

    return false
}


chatJoinElement.onclick = function (e) {
    e.preventDefault()

    chatWelcomeElement.classList.add('hidden')
    chatRoomElement.classList.remove('hidden')

    joinChatRoom()

    return false
}


chatSubmitElement.onclick = function (e) {
    e.preventDefault()

    sendMessage()

    return false
}


chatInputElement.onkeyup = function (e) {
    if (e.keyCode == 13) {
        sendMessage()
    }
}


chatInputElement.onfocus = function (e) {
    chatSocket.send(JSON.stringify({
        'type': 'update',
        'message': 'writing_active',
        'name': chatName
    }))
}