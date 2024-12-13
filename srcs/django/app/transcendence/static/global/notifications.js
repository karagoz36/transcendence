// @ts-check
import {getPage} from "./SPA.js"

/**
 * @param {string} text 
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
	toastContainer?.append(toast)
}
/** @param {MessageEvent} e */
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

class NotificationHandler {
	constructor() {
		this.createSocket = this.createSocket.bind(this)
		this.createSocket()
	}

	createSocket() {
		removeEventListener("page-changed", this.createSocket)
		this.socket = new WebSocket(`wss://${window.location.host}/websocket/notifications/`)
		this.socket.onmessage = receiveMessage
		this.socket.onclose = () => addEventListener("page-changed", this.createSocket)
	}
}

function main() {
	const notif = new NotificationHandler()
}

main()