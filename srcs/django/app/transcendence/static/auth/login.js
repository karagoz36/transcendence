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
        console.time("Login API Response");
        const res = await fetch("/api/login", {
			method: "POST",
			body: JSON.stringify({ username, password }),
			headers: {
				"content-type": "application/json",
				"X-CSRFToken": csrftoken
			}
		});
        console.timeEnd("Login API Response");
		if (res.ok) {
            const data = await res.json();
            console.log("Response data:", data);
            if (data.is_2fa_enabled) {
                let otp = prompt("Enter your 2FA code:");
                while (!otp || otp.trim() === "") {
                    otp = prompt("2FA code cannot be empty. Enter your 2FA code:");
                }
				const otpResponse = await fetch("/api/verify_otp/", {
                    method: "POST",
                    body: JSON.stringify({ username, otp }),
                    headers: {
                        "content-type": "application/json",
                        "X-CSRFToken": csrftoken
                    }
                });
				if (otpResponse.ok) {
                    console.log("2FA verified successfully.");
					await setJWT(csrftoken, username, password);
                    await getPage("/");
                } else {
					const errorData = await otpResponse.json();
					alert(errorData.error || "Invalid 2FA code. Please try again.");
                }
            } else {
                console.log("Login successful without 2FA.");
                const csrfRes = await fetch("/api/csrf-token/", {
                    method: "GET",
                    credentials: "same-origin",
                });
                if (!csrfRes.ok) {
                    alert("Failed to refresh CSRF token.");
                    return;
                }
                const csrfData = await csrfRes.json();
                const newCsrfToken = csrfData.csrfToken;
                await setJWT(newCsrfToken, username, password);
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