import {getPage} from "./SPA.js"

/**
 * @param {str} text 
 * @returns {HTMLDivElement}
 **/
function createToast(text) {
	const toast = document.createElement("div")
	toast.id = "liveToast";
	toast.className = "toast show"; // Add multiple classes
	toast.setAttribute("role", "alert");
	toast.setAttribute("aria-live", "assertive");
	toast.setAttribute("aria-atomic", "true");
	toast.innerHTML = `
	<div class="toast-header">
    	<strong class="me-auto">Notification</strong>
      	<button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    <div class="toast-body">${text}</div>`
	return toast
}

/** @param {string} message */
function addNotif(message) {	
	const toast = createToast(message)
	const toastContainer = document.querySelector(".toast-container")
	toastContainer.append(toast)
	setTimeout(() => toastContainer.removeChild(toast), 10000)
}
/** @param {EventMessage} e */
function receiveMessage(e) {
	const data = JSON.parse(e.data)
	if (!data.message) {
		console.error(data.message)
		throw new Error("notification receive: expected message field")
	}
	addNotif(data.message)
	if (data.refresh == window.location.pathname)
		getPage(data.refresh)
}

function main() {
	const socket = new WebSocket(`wss://${window.location.host}/websocket/notifications/`)
	socket.onmessage = receiveMessage
}

main()

