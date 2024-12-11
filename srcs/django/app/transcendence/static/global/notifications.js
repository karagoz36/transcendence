function webSocket() {
	const socket = new WebSocket(`wss://${window.location.host}/websocket/notifications`)
	socket.onmessage = (ev) => console.log(ev.data)
	socket.onopen = () => socket.send("coucou")
}

function main() {
	webSocket()
}

main()