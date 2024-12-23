// @ts-check
import {getPage, setAnchorEvent} from "./SPA.js"
import BaseWebSocket from "./websockets.js";

/**
 * @param {string} text 
 * @returns {HTMLDivElement}
 **/
function createToast(text) {
	const toast = document.createElement("div")
	toast.id = "liveToast";
	toast.className = "toast show";
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
	setAnchorEvent()
	setTimeout(() => toast.remove(), 10000)
}

class NotificationHandler extends BaseWebSocket {
	/** @param {string} url */
	constructor(url) {
		super(url)
		this.socket.onclose = e => {
			if (e.code == 4000)
				addEventListener("page-changed", this.createSocket)
		}
	}

	/** @param {MessageEvent} e */
	receive(e) {
		const data = JSON.parse(e.data)
		if (data.message)
			addNotif(data.message)

		/** @type {string[]} */
		const urls = data.refresh
		if (!urls) return
		urls.forEach(url => {
			if (url == window.location.pathname)
				getPage(url)
		})
	}
}

function main() {
	const notif = new NotificationHandler("notifications")
}

main()
