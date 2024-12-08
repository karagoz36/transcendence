// @ts-check
/** 
 * @param {Element} newMainContainer
 * @param {Element} oldMainContainer
 * */
function refreshScripts(newMainContainer, oldMainContainer) {
	let scripts = newMainContainer.querySelectorAll("script")

	scripts.forEach(script => {
		const newScript = document.createElement("script")
		newScript.src = script.src + `?v=${Date.now()}`
		newScript.type = script.type
		script.remove()
		oldMainContainer.appendChild(newScript)
	})
}

/** 
 * @typedef {Object} PageOptions
 * @property {string} [method]
 * @property {HeadersInit} [headers]
 * @property {Object} [body]
*/

/**
 * @param {PageOptions} options
 */
function convertOptionsToRequestInit(options) {
	/** @type {RequestInit} */
	let init = {}
	if (options.method == "POST" && (options.headers == undefined || options.headers['X-CSRFToken'] == undefined))
		throw new Error("CSRF token missing for POST method")
	init.body = JSON.stringify(options)
	init.method = options.method
	init.headers = options.headers
	return init
}

/** @param {String} url */
/** @param {PageOptions} options */
export async function getPage(url, options = {}) {
	/** @type {Response|String} */
	let res
	res = await fetch("/api/login", convertOptionsToRequestInit(options))
	res = await res.text()

	const parser = new DOMParser()
	const newPage = parser.parseFromString(res, "text/html")

	const oldMainContainer = document.querySelector(".main-container")
	if (!oldMainContainer)
		throw new Error("failed to find main-container in current body")

	const newMainContainer = newPage.querySelector(".main-container")
	if (!newMainContainer)
		throw new Error(`failed to find main-container in fetched body at ${url}`)
	oldMainContainer.innerHTML = newMainContainer.innerHTML
	refreshScripts(newMainContainer, oldMainContainer)
}