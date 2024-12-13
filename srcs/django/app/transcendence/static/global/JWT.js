// @ts-check

/** 
 * @typedef {Object} JWT
 * @property {string} [access]
 * @property {string} [refresh]
 */

/** @param {string} accessToken */
function setAccessTokenCookie(accessToken) {
	document.cookie = `access_token=${accessToken};`
	+ "max-age=86400;SameSite=Lax;"
	+ "path=/;"
}

/**
 * @param {string} csrftoken
 * @param {string} username
 * @param {string} password
 */
export async function setJWT(csrftoken, username, password) {
	const res = await fetch("/api/token", {
		method: "POST",
		body: JSON.stringify({username, password}),
		headers: {
			cookie: document.cookie,
			"content-type": "application/json",
			"X-CSRFToken": csrftoken
		}
	})
	if (res.status != 200) {
		/** @type {HTMLDivElement|null} */
		console.error(await res.text())
		return
	}
	/** @type {JWT} */
	const jwt = await res.json()
	localStorage.setItem("JWT", JSON.stringify(jwt))
	const accessToken = jwt.access // @ts-ignore
	setAccessTokenCookie(accessToken)
}

export async function refreshJWT() {
	const jwt = getJWT()
	const res = await fetch("/api/token", {
		method: "POST",
		headers: {"content-type": "application/json"},
		body: JSON.stringify({refresh: jwt.refresh})
	})
	/** @type {JWT} */
	const newJWT = await res.json()
	localStorage.setItem("JWT", JSON.stringify(newJWT)) // @ts-ignore
	setAccessTokenCookie(newJWT.access)
}

/**
 * @returns {JWT}
 */
export function getJWT() {
	const item = localStorage.getItem("JWT")
	if (!item)
		throw new Error("getJWT: failed to find JWT in localStorage")
	return JSON.parse(item)
}