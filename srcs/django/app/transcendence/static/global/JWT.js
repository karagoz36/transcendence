/**
 * @param {string} csrfmiddlewaretoken
 * @param {string} username
 * @param {string} password
 */
export async function setJWT(csrfmiddlewaretoken, username, password) {
	const res = await fetch("/api/token", {
		method: "POST",
		body: JSON.stringify({username, password}),
		headers: {
			"X-CSRFToken": csrfmiddlewaretoken,
			"content-type": "application/json",
		}
	})
	localStorage.setItem("JWT", await res.text())
}

export async function refreshJWT() {
	const jwt = getJWT()
	const res = await fetch("/api/token", {
		method: "POST",
		headers: {"content-type": "application/json"},
		body: JSON.stringify({refresh: jwt.refresh})
	})
	localStorage.setItem("JWT", await res.text())
}

/** 
 * @typedef {Object} JWT
 * @property {string} [access]
 * @property {string} [refresh]
 */

/**
 * @returns {JWT}
 */
export function getJWT() {
	const item = localStorage.getItem("JWT")
	if (!item)
		throw new Error("getJWT: failed to find JWT in localStorage")
	return JSON.parse(item)
}