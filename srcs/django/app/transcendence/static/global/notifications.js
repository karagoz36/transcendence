// @ts-check
import {getPage} from "./SPA.js"
import BaseWebSocket from "./websockets.js";

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

class NotificationHandler extends BaseWebSocket {
	/** @param {MessageEvent} e */
	receive(e) {
		const data = JSON.parse(e.data)
		console.log(data)
		if (data.message)
			addNotif(data.message)
		if (data.refresh == window.location.pathname)
			getPage(data.refresh)
	}
}

function main() {
	const notif = new NotificationHandler("notifications")
}

main()
