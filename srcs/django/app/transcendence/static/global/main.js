/** 
 * @param {HTMLDivElement} newMainContainer
 * */
function refreshScripts(newMainContainer) {
	let scripts = newMainContainer.querySelectorAll("script")
	scripts.forEach(script => {
		const newScript = document.createElement("script")
		newScript.src = script.src + `?v=${Date.now()}`
		newScript.type = script.type
		script.remove()
		document.body.querySelector(".main-container").appendChild(newScript)
	})
}

/** @param {String} url */
export async function getPage(url) {
	/** @type {Response|String}} */
	let res = await fetch("/api/login")
	res = await res.text()

	const parser = new DOMParser()
	const newPage = parser.parseFromString(res, "text/html")

	const newMainContainer = newPage.querySelector(".main-container")
	document.querySelector(".main-container").innerHTML = newMainContainer.innerHTML
	refreshScripts(newMainContainer)
}