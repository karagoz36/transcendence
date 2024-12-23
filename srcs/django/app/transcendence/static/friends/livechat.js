// @ts-check
import BaseWebSocket from "../global/websockets.js";

class MessagesHandler extends BaseWebSocket {
	/** @param {CustomEvent} e */
	onPageChange(e) {
		if (e.detail != ".main-container")
			return
		this.socket.onmessage = null
		this.socket.close()
	}

	/** @param {string} url */
	constructor(url) {
		super(url)
		addEventListener("page-changed", this.onPageChange.bind(this))
	}

    /** @param {MessageEvent} e */
	receive(e) {
		/** @type {HTMLDivElement} */ // @ts-ignore
		const messageContainer = document.querySelector("#messages-container")
		const div = document.createElement("div")
		div.innerHTML = e.data
		messageContainer.appendChild(div)
	}
}

function main() {
	const notif = new MessagesHandler("messages")
}

main()