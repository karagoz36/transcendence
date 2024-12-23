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

    /** @param {CloseEvent} e */
    onClose(e) {
        if (e.code == 4000)
            addEventListener("page-changed", this.createSocket)
    }
    
	createSocket() {
		removeEventListener("page-changed", this.createSocket)
		this.socket = new WebSocket(`wss://${window.location.host}/websocket/${this.url}/`)
		this.socket.onmessage = this.receive
        this.socket.onerror = (ev) => console.error(ev)
		this.socket.onclose = this.onClose
	}
}