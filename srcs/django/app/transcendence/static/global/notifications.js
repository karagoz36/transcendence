// @ts-check
import {getPage, setAnchorEvent} from "./SPA.js"
import BaseWebSocket from "./websockets.js";
import { openChat } from "../friends/message.js";


/**
 * @param {string} text 
 * @returns {HTMLDivElement}
 **/
function createToast(text, link) {
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
    <div class="toast-body">
			${text}
	</div>`
	toast.querySelector(".btn-close").addEventListener("click", (event) => {
		event.stopPropagation();
	});
	
	toast.addEventListener("click", async (event) => {
		event.preventDefault();
		await getPage(link);
	});
	return toast
}

/** 
 * @param {string} message
 * @param {number} duration 
*/
function addNotif(message, link, duration) {	
	const toast = createToast(message, link)
	const toastContainer = document.querySelector(".toast-container")
	toastContainer?.append(toast)
	setAnchorEvent()
	duration = typeof(duration) == "number" ? duration : 10000
	if (duration > 0)
		setTimeout(() => toast.remove(), duration)
}

class NotificationHandler extends BaseWebSocket {
	/** @param {CloseEvent} e */
	close(e) {
		if (e.code == 4000)
			addEventListener("page-changed", this.createSocket)
	}
	
	/** @param {Event} e */
	open(e) {
		removeEventListener("page-changed", this.createSocket)
	}

	/** @param {MessageEvent} e */
	async receive(e) {
		const data = JSON.parse(e.data)
		if (data.message){
			let link = data.link
			console.log(link)
			addNotif(data.message, link, data.duration)
		}
		if (data.redirect)
			await getPage(data.redirect)

		/** @type {string[]} */
		const urls = data.refresh
		if (!urls)
			return

		for (let url of urls) {
			if (url == window.location.pathname || url == window.location.pathname + window.location.search) {
				await getPage(url)
				break
			}
		}
	}
}

function main() {
	const notif = new NotificationHandler("notifications")
}

main()
