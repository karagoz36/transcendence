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
	}, false, "#messages-container");
	event.target["message"].value = "";
}

function main() {
	/** @type {NodeListOf<HTMLFormElement>|null} */
	const forms = document.querySelectorAll("form#send-message-form")
	if (forms == null)
		return
	forms.forEach(form => form.onsubmit = sendMessage)
	/** @type {NodeListOf<HTMLButtonElement>|null} */
	const buttons = document.querySelectorAll("button#open-chat-modal")
	buttons.forEach(button => button.onclick = transferID)
}

main()