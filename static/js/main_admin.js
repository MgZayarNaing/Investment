/**
 * Variables
 */

const chatRoom = document.querySelector('#room_uuid').textContent.replaceAll('"', '')

let chatSocket = null


/**
 * Elements
 */

const chatLogElement = document.querySelector('#chat_log')
const chatInputElement = document.querySelector('#chat_message_input')
const chatSubmitElement = document.querySelector('#chat_message_submit')


/**
 * Functions
 */

function scrollToBottom() {
    chatLogElement.scrollTop = chatLogElement.scrollHeight
}


function sendMessage() {
    chatSocket.send(JSON.stringify({
        'type': 'message',
        'message': chatInputElement.value,
        'name': document.querySelector('#user_name').textContent.replaceAll('"', ''),
        'agent': document.querySelector('#user_id').textContent.replaceAll('"', ''),
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
        
        if (!data.agent) {
            chatLogElement.innerHTML += `
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

            <div style="border-radius: 50%; width: 3rem; height: 3rem;line-height:3rem; text-align: center; background-color: #D1D5DB;color:#000; ">${data.initials}</div>
        </div>
            `
        }
    } else if (data.type == 'writing_active') {
        if (!data.agent) {
            let tmpInfo = document.querySelector('.tmp-info')

            if (tmpInfo) {
                tmpInfo.remove()
            }

            chatLogElement.innerHTML += `
                <div class="tmp-info flex w-full mt-2 space-x-3 max-w-md">
                    <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300 text-center pt-2">${data.initials}</div>

                    <div>
                        <div class="bg-gray-300 p-3 rounded-l-lg rounded-br-lg">
                            <p class="text-sm">The client is typing...</p>
                        </div>
                    </div>
                </div>
            `
        }
    }

    scrollToBottom()
}


/**
 * Web socket
 */

chatSocket = new WebSocket(`ws://${window.location.host}/ws/${chatRoom}/`)

chatSocket.onmessage = function(e) {
    console.log('on message')

    onChatMessage(JSON.parse(e.data))
}

chatSocket.onopen = function(e) {
    console.log('on open')

    scrollToBottom()
}

chatSocket.onclose = function(e) {
    console.log('chat socket closed unexpectadly')
}


/**
 * Event listeners
 */

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
        'name': document.querySelector('#user_name').textContent.replaceAll('"', ''),
        'agent': document.querySelector('#user_id').textContent.replaceAll('"', ''),
    }))
}