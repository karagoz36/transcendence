// @ts-check
import { getPage } from "../global/SPA.js"
import { setJWT } from "../global/JWT.js"

/** @param {SubmitEvent} e */
async function handleLogin(e) {
	e.preventDefault()
	if (!e.target)
		throw new Error("handleLogin: e.target null")
	/** @type {String} */
	const username = e.target['username'].value
	/** @type {String} */
	const password = e.target['password'].value
	/** @type {String} */
	const csrftoken = e.target['csrfmiddlewaretoken'].value
	try {
        const response = await fetch("/api/user/is_2fa_enabled/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username }),
        });
		if (response.ok) {
			const data = await response.json();
            if (data.is_2fa_enabled) {
                const otp = prompt("Enter your 2FA code:");
                console.log("2FA Code entered:", otp);
            }
		}
	}
	catch (e) {
		console.error("Error quelque part");
	}
	await setJWT(csrftoken, username, password)
	await getPage("/api/login", {
		method: "POST",
		body: {username, password},
		headers: {
			"content-type": "application/json",
			"X-CSRFToken": csrftoken
		}
	})
}

function main() {
	/** @type {HTMLFormElement|null} */
	const form = document.querySelector("#login")
	if (form == null)
		throw new Error("querySelector: could not find login form")
	form.onsubmit = handleLogin
}

main()