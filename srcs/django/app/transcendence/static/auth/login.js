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
	await setJWT(csrftoken, username, password)
	try {
		const res = await fetch("/api/login", {
			method: "POST",
			body: JSON.stringify({ username, password }),
			headers: {
				"content-type": "application/json",
				"X-CSRFToken": csrftoken
			}
		});
		if (res.ok) {
            const data = await res.json();
            if (data.is_2fa_enabled) {
                const otp = prompt("Enter your 2FA code:");
                console.log("2FA Code entered:", otp);
				if (otp && otp.trim() !== "")
					await getPage("/");
                // TODO: Ajouter la logique de validation avec email
            } else {
                console.log("Login successful without 2FA.");
                await getPage("/");
            }
        } else {
            const errorData = await res.json();
            alert(errorData.error || "Login failed.");
        }
    } catch (e) {
        console.error("Error during login:", e);
        alert("An unexpected error occurred.");
    }

}

function main() {
	/** @type {HTMLFormElement|null} */
	const form = document.querySelector("#login")
	if (form == null)
		throw new Error("querySelector: could not find login form")
	form.onsubmit = handleLogin
}

main()