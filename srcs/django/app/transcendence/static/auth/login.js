// @ts-check
import { getPage } from "../global/SPA.js"
import { setJWT } from "../global/JWT.js"

/** @param {SubmitEvent} e */
async function handleLogin(e) {
    e.preventDefault();
    if (!e.target) throw new Error("handleLogin: e.target is null");

    const form = e.target;
    /** @type {String} */
    const username = form['username'].value;
    /** @type {String} */
    const password = form['password'].value;
    /** @type {String} */
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
                showOtpPopup(username, password, csrftoken);
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

function showOtpPopup(username, password, csrftoken) {
    /** @type {HTMLElement | null} */
    const otpPopup = document.getElementById("otpPopup");
    /** @type {HTMLFormElement|null} */
    const otpForm = document.querySelector("#otpForm");
    /** @type {NodeListOf<HTMLInputElement>} */
    const otpInputs = document.querySelectorAll(".otp-input");
    /** @type {HTMLElement | null} */
    const cancelButton = document.getElementById("cancelOtp");

    if (!otpPopup || !otpForm || !otpInputs || !cancelButton) {
        throw new Error("OTP popup elements not found");
    }

    otpPopup.classList.add("show");
	let isPasting = false;

    otpInputs.forEach((input, index) => {
        input.value = "";

        input.oninput = () => {
            if (input.value.length === 1 && index < otpInputs.length - 1) {
                otpInputs[index + 1].focus();
            }
            validateOtpInputs();
        };

		input.onkeydown = (e) => {
			if (isPasting) return;
            if (e.key === "Backspace" && input.value === "" && index > 0) {
                otpInputs[index - 1].focus();
                otpInputs[index - 1].value = "";
            } else if (e.key === "Enter") {
                e.preventDefault();
                /** @type {object}} */
                const submitButton = document.getElementById("submitOtp");
                if (!submitButton.disabled) {
                    submitButton.click();
                }
            }
        };

        input.onpaste = (e) => {
            e.preventDefault();
			isPasting = true;
            const pasteData = (e.clipboardData)?.getData("text") || "";
            if (/^\d{6}$/.test(pasteData)) {
                otpInputs.forEach((field, idx) => {
                    field.value = pasteData[idx] || "";
                });
                validateOtpInputs();
            } else {
                alert("Please paste a valid 6-digit OTP code.");
            }
			setTimeout(() => {
				isPasting = false;
			}, 0);
        };
    });

    otpForm.onsubmit = async (e) => {
        e.preventDefault();
        const otp = Array.from(otpInputs).map(input => input.value).join("");
        try {
            const otpResponse = await fetch("/api/verify_otp/", {
                method: "POST",
                body: JSON.stringify({ username, otp }),
                headers: {
                    "content-type": "application/json",
                    "X-CSRFToken": csrftoken,
                },
            });

            if (otpResponse.ok) {
                otpPopup.classList.remove("show");
                await completeLogin(username, password, csrftoken);
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
     /** @type {NodeListOf<HTMLInputElement>} */
    const otpInputs = document.querySelectorAll(".otp-input");
    /** @type {HTMLElement|null} */
    const submitButton = document.getElementById("submitOtp");

    if (!(submitButton instanceof HTMLButtonElement)) return;

    const allFilled = Array.from(otpInputs).every(input => input.value.trim() !== "");
    submitButton.disabled = !allFilled;
}

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