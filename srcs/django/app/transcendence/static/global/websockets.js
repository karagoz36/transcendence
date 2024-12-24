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
    
    /** @param {Event} e */
    open(e) {}

	createSocket() {
		this.socket = new WebSocket(`wss://${window.location.host}/websocket/${this.url}/`)
		this.socket.onmessage = this.receive.bind(this)
        this.socket.onerror = e => console.error(e)
        this.socket.onopen = this.open.bind(this)
	}
}