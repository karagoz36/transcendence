// @ts-check
/** 
 * @param {Element} newMainContainer
 * @param {Element} oldMainContainer
*/
function refreshScripts(newMainContainer, oldMainContainer) {
	/** @type {NodeListOf<HTMLScriptElement>} */
	let scripts = oldMainContainer.querySelectorAll("script")

	scripts.forEach(script => {
		const newScript = document.createElement("script")
		newScript.src = script.src + `?v=${Date.now()}`
		newScript.type = script.type
		script.replaceWith(newScript)
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
	init.body = JSON.stringify(options.body)
	init.method = options.method
	init.headers = options.headers
	return init
}

/** @param {string} url */
/** @param {PageOptions} options */
/** @param {boolean} addToHistory */
export async function getPage(url, options = {}, addToHistory = true) {
	/** @type {Response|String} */
	let res
	res = await fetch(url, convertOptionsToRequestInit(options))
	if (res.status == 404 || res.status >= 500)
		throw new Error(`SPA: failed to fetch ${url}`)
	if (addToHistory)
		history.pushState({page: url}, "", res.url)
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

window.addEventListener("popstate", (e) => {
	getPage(window.location.href, {}, false)
})

/** @param {MouseEvent} e */
/** @this HTMLAnchorElement */
function preventAnchorReloading(e) {
	e.preventDefault()
	getPage(e.target.href)
}

function setAnchorEvent() {
	/** @type {NodeListOf<HTMLAnchorElement>} */
	const links = document.querySelectorAll("a")
	links.forEach(curr => curr.addEventListener("click", preventAnchorReloading))
}

setAnchorEvent()

const mainContainer = document.querySelector(".main-container")
if (!mainContainer)
	throw new Error("mutation observer: could not find main container")
const observer = new MutationObserver(setAnchorEvent)
observer.observe(mainContainer, { attributes: true, childList: true, subtree: true })