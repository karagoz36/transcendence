// @ts-check
import {getPage, setAnchorEvent} from "./SPA.js"
import BaseWebSocket from "./websockets.js";

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
		<a href="${link}" style="text-decoration: none; color: inherit;">
			${text}
		</a>
	</div>`
	toast.addEventListener("click", (event) => {
		event.preventDefault();
		getPage(link); // Redirige vers le lien
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
		if (!urls) return
		urls.forEach(async (url) => {
			if (url == window.location.pathname)
				await getPage(url)
		})
	}
}

function main() {
	const notif = new NotificationHandler("notifications")
}

main()
