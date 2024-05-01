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
            chatLogElement.innerHTML +=`
                                        <div style="display: flex;margin-top: 0.5rem; margin-left: 0.875rem; width: 100%;  max-width: 28rem;">
                                            <div style="border-radius: 50%; width: 3rem; height: 3rem;line-height:3rem; text-align: center; background-color: #D1D5DB;color:#000; ">
                                                ${data.initials}
                                            </div>
                                            <div>
                                                <div style="padding: 0.75rem; border-top-left-radius: 0.5rem;border-bottom-left-radius: 0.5rem; border-bottom-right-radius: 0.5rem; background-color: #D1D5DB; margin-left:1rem;margin-bottom:1rem;">
                                                    <p style="font-size:1.4rem;line-height:1.75rem;color:#000; ">${data.message}</p>
                                                </div>
                                                <span style="font-size: 1rem;color:var(--text-color1);margin-left:1rem;margin-top:1rem; ">${data.created_at} ago</span>
                                            </div>
                                        </div>
                                        `
        } else {
            chatLogElement.innerHTML += `
                                        <div style="display: flex;margin-top: 0.5rem; margin-left: 0.875rem; width: 100%;  max-width: 28rem; justify-content:flex-end;">
                                        
                                            <div>
                                                <div style="padding: 0.75rem; border-top-left-radius: 0.5rem;border-bottom-left-radius: 0.5rem; border-bottom-right-radius: 0.5rem; background-color: #93C5FD;margin-right:1rem;margin-bottom:1rem;">
                                                    <p style="font-size:1.4rem;line-height:1.75rem;color:#000; ">${data.message}</p>
                                                </div>
                                                <span style="font-size:1rem;color:var(--text-color-1);margin-left:1rem;margin-top:1rem; ">${data.created_at} ago</span>
                                            </div>
                                            <div style="border-radius: 50%; width: 3rem; height: 3rem;line-height:3rem; text-align: center; background-color: #D1D5DB;color:#000; ">
                                                ${data.initials}
                                            </div>

                                        </div>
                                        `
        }
    } else if (data.type == 'users_update') {
        chatLogElement.innerHTML += '<p class="mt-2">The admin/agent has joined the chat!'
    } else if (data.type == 'writing_active') {
        if (data.agent) {
            let tmpInfo = document.querySelector('.tmp-info')

            if (tmpInfo) {
                tmpInfo.remove()
            }

            chatLogElement.innerHTML += `
            <div class="tmp-info" style="display: flex;margin-top: 0.5rem; margin-left: 0.875rem; width: 100%;  max-width: 28rem;">
            <div style="border-radius: 50%; width: 3rem; height: 3rem;line-height:3rem; text-align: center; background-color: #D1D5DB;color:#000; ">
                ${data.initials}
            </div>
            <div>
                <div style="padding: 0.75rem; border-top-left-radius: 0.5rem;border-bottom-left-radius: 0.5rem; border-bottom-right-radius: 0.5rem; background-color: #D1D5DB; margin-left:1rem;margin-bottom:1rem;">
                    <p style="font-size:1.4rem;line-height:1.75rem;color:#000; ">The admin/replier is writing a message</p>
                </div>
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

    await fetch(`/api/create-room/${chatRoomUuid}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: data
    })
    .then(function(res) {
        return res.json()
    })
    .then(function(data) {
        console.log('data', data)
    })


    chatSocket = new WebSocket(`ws://${window.location.host}/ws/${chatRoomUuid}/`)


    chatSocket.onmessage = function(e) {
        console.log('onMessage')

        onChatMessage(JSON.parse(e.data))
    }


    chatSocket.onopen = function(e) {
        console.log('onOpen - chat socket was opened')

        scrollToBottom()
    }


    chatSocket.onclose = function(e) {

        console.log('onClose - chat socket was closed')
    }
}


/**
 * Event listeners
 */

chatOpenElement.onclick = function(e) {
    e.preventDefault()

    chatIconElement.classList.add('hidden')
    chatWelcomeElement.classList.remove('hidden')

    return false
}


chatJoinElement.onclick = function(e) {
    e.preventDefault()

    chatWelcomeElement.classList.add('hidden')
    chatRoomElement.classList.remove('hidden')

    joinChatRoom()

    return false
}


chatSubmitElement.onclick = function(e) {
    e.preventDefault()

    sendMessage()

    return false
}


chatInputElement.onkeyup = function(e) {
    if (e.keyCode == 13) {
        sendMessage()
    }
}


chatInputElement.onfocus = function(e) {
    chatSocket.send(JSON.stringify({
        'type': 'update',
        'message': 'writing_active',
        'name': chatName
    }))
}