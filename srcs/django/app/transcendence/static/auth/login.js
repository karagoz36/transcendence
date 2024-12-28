// @ts-check
import { getPage } from "../global/SPA.js"
import { setJWT } from "../global/JWT.js"

/** @param {SubmitEvent} e */
async function handleLogin(e) {
    e.preventDefault();
    if (!e.target) throw new Error("handleLogin: e.target is null");

    const form = e.target;
    const username = form['username'].value;
    const password = form['password'].value;
    const csrftoken = form['csrfmiddlewaretoken'].value;
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
                showOtpPopup(username, csrftoken);
            } else {
                await completeLogin(username, password, csrftoken);
            }
        } else {
            const errorData = await res.json();
            alert(errorData.error || "Login failed.");
        }
    } catch (error) {
        console.error("Error during login:", error);
        alert("An unexpected error occurred.");
    }
}

async function completeLogin(username, password, csrftoken) {
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

function showOtpPopup(username, csrftoken) {
    const otpPopup = document.getElementById("otpPopup");
    if (!otpPopup) throw new Error("OTP popup not found");

    const otpInputs = document.querySelectorAll(".otp-input");
    if (!otpInputs) throw new Error("OTP input fields not found");

    const submitButton = document.getElementById("submitOtp");
    const cancelButton = document.getElementById("cancelOtp");

    if (!submitButton || !cancelButton) throw new Error("OTP buttons not found");

    otpPopup.classList.add("show");

    otpInputs.forEach((input, index) => {
        input.value = "";
        input.oninput = () => {
            if (input.value.length === 1 && index < otpInputs.length - 1) {
                otpInputs[index + 1].focus();
            }
            validateOtpInputs();
        };
    });

    submitButton.onclick = async () => {
        const otp = Array.from(otpInputs).map(input => input.value).join("");
        try {
            const otpResponse = await fetch("/api/verify_otp/", {
                method: "POST",
                body: JSON.stringify({ username, otp }),
                headers: {
                    "content-type": "application/json",
                    "X-CSRFToken": csrftoken
                }
            });

            if (otpResponse.ok) {
                otpPopup.classList.remove("show");
                await completeLogin(username, null, csrftoken);
            } else {
                const errorData = await otpResponse.json();
                alert(errorData.error || "Invalid 2FA code. Please try again.");
            }
        } catch (error) {
            console.error("Error verifying OTP:", error);
            alert("An unexpected error occurred.");
        }
    };

    cancelButton.onclick = () => {
        otpPopup.classList.remove("show");
    };
}

function validateOtpInputs() {
    const otpInputs = document.querySelectorAll(".otp-input");
    const submitButton = document.getElementById("submitOtp");

    if (!submitButton) return;

    const allFilled = Array.from(otpInputs).every(input => input.value.trim() !== "");
    submitButton.disabled = !allFilled;
}

// /** @param {SubmitEvent} e */
// async function handleLogin(e) {
// 	e.preventDefault()
// 	if (!e.target)
// 		throw new Error("handleLogin: e.target null")
// 	/** @type {String} */
// 	const username = e.target['username'].value
// 	/** @type {String} */
// 	const password = e.target['password'].value
// 	/** @type {String} */
// 	const csrftoken = e.target['csrfmiddlewaretoken'].value
// 	try {
//         console.time("Login API Response");
//         const res = await fetch("/api/login", {
// 			method: "POST",
// 			body: JSON.stringify({ username, password }),
// 			headers: {
// 				"content-type": "application/json",
// 				"X-CSRFToken": csrftoken
// 			}
// 		});
//         console.timeEnd("Login API Response");
// 		if (res.ok) {
//             const data = await res.json();
//             console.log("Response data:", data);
//             if (data.is_2fa_enabled) {
//                 let otp = prompt("Enter your 2FA code:");
//                 while (!otp || otp.trim() === "") {
//                     otp = prompt("2FA code cannot be empty. Enter your 2FA code:");
//                 }
// 				const otpResponse = await fetch("/api/verify_otp/", {
//                     method: "POST",
//                     body: JSON.stringify({ username, otp }),
//                     headers: {
//                         "content-type": "application/json",
//                         "X-CSRFToken": csrftoken
//                     }
//                 });
// 				if (otpResponse.ok) {
//                     console.log("2FA verified successfully.");
// 					await setJWT(csrftoken, username, password);
//                     await getPage("/");
//                 } else {
// 					const errorData = await otpResponse.json();
// 					alert(errorData.error || "Invalid 2FA code. Please try again.");
//                 }
//             } else {
//                 console.log("Login successful without 2FA.");
//                 const csrfRes = await fetch("/api/csrf-token/", {
//                     method: "GET",
//                     credentials: "same-origin",
//                 });
//                 if (!csrfRes.ok) {
//                     alert("Failed to refresh CSRF token.");
//                     return;
//                 }
//                 const csrfData = await csrfRes.json();
//                 const newCsrfToken = csrfData.csrfToken;
//                 await setJWT(newCsrfToken, username, password);
//                 await getPage("/");
//             }
//         } else {
//             const errorData = await res.json();
//             alert(errorData.error || "Login failed.");
//         }
//     } catch (e) {
//         console.error("Error during login:", e);
//         alert("An unexpected error occurred.");
//     }
// }

/** @param {SubmitEvent} e */
async function handleLogin42(e) {
    e.preventDefault(); 
    
    if (!e.target) {
        throw new Error("handleLogin: e.target null");
    }
    try {
        window.location.href = "/auth/login42/";
    } catch (error) {
        console.error("Error redirecting to 42 login:", error);
    }
}

function main() {
	/** @type {HTMLFormElement|null} */
	const form = document.querySelector("#login")
	if (form == null)
		throw new Error("querySelector: could not find login form")
	form.onsubmit = handleLogin
	/** @type {HTMLFormElement|null} */
    const form42 = document.querySelector('#login42')
    if (form42 == null)
        throw new Error("querySelector: could not find login42 form")
    form42.onsubmit = handleLogin42
}

main()