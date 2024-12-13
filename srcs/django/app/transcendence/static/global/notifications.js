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
    	<strong class="me-auto">Bootstrap</strong>
      	<small>11 mins ago</small>
      	<button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    <div class="toast-body">${text}</div>`
	return toast
}

/** @param {MessageEvent} e */
function pushNotif(e) {
	const toast = createToast(e.data)
	const toastContainer = document.querySelector(".toast-container")
	toastContainer.append(toast)
	setTimeout(() => toastContainer.removeChild(toast), 10000)
}

function main() {
	const socket = new WebSocket(`wss://${window.location.host}/websocket/notifications/test/`)
	socket.onerror = () => console.log("test")
	socket.onmessage = pushNotif
	socket.onopen = () => socket.send("Message sent to server")
}

main()

