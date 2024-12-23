// @ts-check
export default class BaseWebSocket {
    /** @type {string} */
    url
    /** @type {WebSocket} */
    socket

    /** @param {string} url */
	constructor(url) {
        this.url = url
        this.createSocket = this.createSocket.bind(this)
		this.createSocket()
	}

    /** @param {MessageEvent} e */
    receive(e) {
        console.error("function not overloaded")
    }

	createSocket() {
		removeEventListener("page-changed", this.createSocket)
		this.socket = new WebSocket(`wss://${window.location.host}/websocket/${this.url}/`)
		this.socket.onmessage = this.receive
        this.socket.onerror = e => console.error(e)
		this.socket.onclose = (e) => e.code == 4000 ? addEventListener("page-changed", this.createSocket) : ""
	}
}