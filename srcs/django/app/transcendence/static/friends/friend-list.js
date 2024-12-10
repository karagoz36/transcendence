// TODO
/** @param {SubmitEvent} e */
function sendMessage(e) {
	e.preventDefault()
	/** @type {HTMLInputElement} */
	const input = e.target['message']
}

function main() {
	const inputMessage = document.querySelector("#send-message-form")
	inputMessage.onsubmit = sendMessage
	
	const modal = document.getElementById('exampleModal')
	modal.addEventListener("shown.bs.modal", () => document.querySelector("#message-input").focus())
}

main()