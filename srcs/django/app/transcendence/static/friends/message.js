// @ts-check
import {getPage} from "../global/SPA.js"

/** @param {MouseEvent} e */
function transferID(e) {
   	/** @type {HTMLButtonElement|EventTarget|null} */
	const button = e.target
	if (!button) return
    /** @type {HTMLButtonElement|null} */
    const modalButton = document.querySelector("#send-message")
	if (modalButton == null)
		return
	/** @type {string|null} */ // @ts-ignore
	const userId = button.getAttribute("user-id")
	if (userId == null)
			return
    modalButton.setAttribute("user-id", userId)
}

/** @param {HTMLButtonElement} button */
function connectButton(button) {
    button.onclick = transferID
}

/** @param {SubmitEvent} event */
async function sendMessage(event) {
	event.preventDefault();
	if (!event.target) return
	/** @type {string} */
	const message = event.target["message"].value
	/** @type {HTMLButtonElement} */ // @ts-ignore
	const button = event.submitter
	const friendID = Number(button.getAttribute("user-id"))
	await getPage("/api/friend/send-message", {
		method: "POST",
		headers: {"content-type": "application/json"},
		body: {			
			"friendID": friendID,
			"message": message
		}
	}, true, "#messages-container")
}

function main() {
	/** @type {HTMLFormElement|null} */
	const forms = document.querySelectorAll("form#send-message-form")
	if (forms == null)
		return
	// form.onsubmit = logSubmit
	forms.forEach(form => form.onsubmit = sendMessage)
	document.querySelectorAll("#open-chat-modal").forEach(connectButton)
}

main()