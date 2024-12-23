// @ts-check

import { refreshJWT } from "./JWT.js"

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

/** 
 * @param {Element} newMainContainer
 * @param {Element} oldMainContainer
*/
function refreshScripts(newMainContainer, oldMainContainer) {
	/** @type {NodeListOf<HTMLScriptElement>} */
	const oldScripts = oldMainContainer.querySelectorAll("script")
	const newScripts = newMainContainer.querySelectorAll("script")

	oldScripts.forEach(script => {
		script.type = "application/json"
		script.remove()
	})
	newScripts.forEach(script => {
		const newScript = document.createElement("script")
		newScript.src = script.src + `?v=${Date.now()}`
		newScript.type = script.type
		document.querySelector(".main-container")?.append(newScript)
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
	/** @type {Response|String} */
	let res
	res = await fetch(url, options)
	if (res.status == 404 || res.status >= 500)
		throw new Error(`SPA: failed to fetch ${url}`)
	if (addToHistory && !url.includes("api"))
		history.pushState({page: url}, "", res.url)
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

	const oldMainContainer = document.querySelector(toUpdate)
	if (!oldMainContainer)
		throw new Error(`failed to find ${toUpdate} in current body`)

	const newMainContainer = newPage.querySelector(toUpdate)
	if (!newMainContainer)
		throw new Error(`failed to find ${toUpdate} in fetched body at ${url}`)
	oldMainContainer.innerHTML = newMainContainer.innerHTML

	setAnchorEvent()
	refreshScripts(newMainContainer, oldMainContainer)
	const event = new CustomEvent("page-changed", {"detail": toUpdate})
	dispatchEvent(event)
}

window.addEventListener("popstate", (e) => {
	getPage(window.location.href, {}, false)
})

setAnchorEvent()

// window.onload = () => getPage(window.location.pathname)