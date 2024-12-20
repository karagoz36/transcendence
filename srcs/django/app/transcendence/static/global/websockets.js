export default class BaseWebSocket {
    /** @type {string} */
    url
    /** @param {string} url */
	constructor(url) {
        this.createSocket = this.createSocket.bind(this)
		this.createSocket(url)
	}

    /** @param {MessageEvent} e */
    receive(e) {
        console.error("function not overloaded")
    }

    /** @param {Event} e */
    connect(e) {}
    
    /** @param {string} url */
	createSocket(url) {
        this.url = url
		removeEventListener("page-changed", this.createSocket)
		this.socket = new WebSocket(`wss://${window.location.host}/websocket/${url}/`)
		this.socket.onmessage = this.receive
        this.socket.onopen = this.connect
        this.socket.onerror = () => {throw new Error("")}
		this.socket.onclose = () => addEventListener("page-changed", () => this.createSocket(url))
	}
}