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
		console.error(await res.text())
		throw new Error(`fetch at /api/token failed`)
	}
	/** @type {JWT} */
	const jwt = await res.text()
	localStorage.setItem("JWT", jwt)
	const accessToken = JSON.parse(jwt).access
	setAccessTokenCookie(accessToken)
}

export async function refreshJWT() {
	const jwt = getJWT()
	const res = await fetch("/api/token", {
		method: "POST",
		headers: {"content-type": "application/json"},
		body: JSON.stringify({refresh: jwt.refresh})
	})
	const newJWT = await res.text()
	localStorage.setItem("JWT", newJWT)
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