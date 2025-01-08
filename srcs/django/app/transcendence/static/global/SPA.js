// @ts-check

/** @param {MouseEvent} e */
async function preventAnchorReloading(e) {
	e.preventDefault() // @ts-ignore
	await getPage(e.target.href)
}

export function setAnchorEvent() {
	/** @type {NodeListOf<HTMLAnchorElement>} */
	const links = document.querySelectorAll("a")
	links.forEach(curr => curr.onclick = preventAnchorReloading)
}

/** 
 * @param {Element} newContainer
 * @param {Element} oldContainer
 * @param {string} toUpdate
*/
export function refreshScripts(newContainer, oldContainer, toUpdate) {
	/** @type {NodeListOf<HTMLScriptElement>} */
	const newScripts = newContainer.querySelectorAll("script")
	/** @type {NodeListOf<HTMLScriptElement>} */
	const oldScripts = oldContainer.querySelectorAll("script")
	console.log(newScripts)

	oldScripts.forEach(script => {
		script.type = "application/json"
		script.remove()
	})
	newScripts.forEach(script => {
		const newScript = document.createElement("script")
		newScript.src = script.src + `?v=${Date.now()}`
		newScript.type = script.type == "application/json" ? "module" : script.type
		document.querySelector(toUpdate)?.append(newScript)
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
	init.body = JSON.stringify(options.body)
	init.method = options.method
	init.headers = {
		...options.headers,
		cookie: document.cookie,
	}
	return init
}

/**
 * 
 * @param {string} url
 * @param {RequestInit} options
 * @param {boolean} addToHistory
 * @returns 
 */
async function getHTML(url, options, addToHistory) {
	/** @type {Response} */
	let res
	res = await fetch(url, options)
	if (res.status == 404 || res.status >= 500)
		throw new Error(`SPA: failed to fetch ${url}`)
	if (addToHistory && !res.url.includes("api"))
		history.pushState({page: res.url}, "", res.url)
	if (res.headers.get("content-type") == "application/json") {
		console.error(await res.json())
		throw new Error("got json instead of html")	
	}
	return await res.text()
}

/** 
 * @param {string} url
 * @param {PageOptions} options
 * @param {boolean} addToHistory 
 * @param {string} toUpdate
 **/
export async function getPage(url, options = {}, addToHistory = true, toUpdate = ".main-container") {
	const requestInit = convertOptionsToRequestInit(options)
	const res = await getHTML(url, requestInit, addToHistory)
	const parser = new DOMParser()
	const newPage = parser.parseFromString(res, "text/html")
	document.title = newPage.title

	const oldContainer = document.querySelector(toUpdate)
	if (!oldContainer)
		throw new Error(`failed to find ${toUpdate} in current body`)

	const newContainer = newPage.querySelector(toUpdate)
	if (!newContainer)
		throw new Error(`failed to find ${toUpdate} in fetched body at ${url}`)
	oldContainer.innerHTML = newContainer.innerHTML

	setAnchorEvent()
	refreshScripts(newContainer, oldContainer, toUpdate)
	const event = new CustomEvent("page-changed", {"detail": toUpdate})
	dispatchEvent(event)
}

window.addEventListener("popstate", async (e) => {
	await getPage(window.location.href, {}, false)
})

setAnchorEvent()

// window.onload = () => getPage(window.location.pathname)