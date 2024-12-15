// @ts-check

/** @param {HTMLButtonElement} sendMessageButton */
function passFriendIDToModal(sendMessageButton) {
	/** @type {NodeListOf<HTMLButtonElement>} */
	const buttons = document.querySelectorAll("button#open-chat-modal")
	
	buttons.forEach(button => {
		button.onclick = () => {
			// @ts-ignore
			sendMessageButton.setAttribute("user-id", button.getAttribute("user-id"))
		}
	})
}

/** @param {MouseEvent} e */
function sendMessage(e) {
	e.preventDefault()
	/** @type {HTMLButtonElement} */ // @ts-ignore
	const button = e.target
	const friendID = Number(button.getAttribute("user-id"))
	console.log(friendID)
}

function main() {
	/** @type {HTMLButtonElement} */ // @ts-ignore
	const button = document.querySelector("button#send-message")
	passFriendIDToModal(button)
	button.onclick = sendMessage
}

main()