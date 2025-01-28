import { getPage } from "../global/SPA.js"

/** @param {SubmitEvent} e */
async function handleSettingsUpdate(e) {
    e.preventDefault();
    if (!e.target) {
        throw new Error("handleSettingsUpdate: e.target is null");
    }

    /** @type {HTMLFormElement} */
    const form = e.target;

    const csrftoken = form['csrfmiddlewaretoken'].value;
    const username = form['username'].value;
    const password = form['password'].value;
    const avatar = form['avatar'].files[0];
    const email = form['email'].value.trim();
    const is_2fa_enabled = form['is_2fa_enabled'].checked;

    if (is_2fa_enabled && email === "") {
        alert("You must provide an email address to enable 2FA.");
        return;
    }

    try {
        const formData = new FormData();
        formData.append("username", username);
        formData.append("email", email);
        formData.append("is_2fa_enabled", is_2fa_enabled);
        formData.append("avatar", avatar);
        formData.append("password", password);

        const response = await fetch("/api/settings/update/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
            },
            body: formData,
        });
        
        const data = await response.json();
        alert(data.message);
        await getPage("/settings")
    } catch (err) {
        console.error("Error in handleSettingsUpdate:", err);
        alert("An unexpected error occurred. Please try again.");
    }
}

async function handleRemoveAvatar() {
    const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    try {
        const response = await fetch("/api/settings/remove-avatar/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
            },
        });

        if (response.ok) {
            alert("Avatar removed successfully!");
            await getPage("/settings")
        } else {
            const errorData = await response.json();
            alert("Error removing avatar: " + (errorData.error || "Unknown error"));
        }
    } catch (err) {
        console.error("Error in handleRemoveAvatar:", err);
        alert("An unexpected error occurred. Please try again.");
    }
}

function main() {
    /** @type {HTMLFormElement|null} */
    const form = document.querySelector("#settings-form");
    if (!form) {
        throw new Error("main: Unable to find settings form");
    }
    form.onsubmit = handleSettingsUpdate;

    const removeAvatarButton = document.querySelector("#remove-avatar");
    if (removeAvatarButton) {
        removeAvatarButton.onclick = handleRemoveAvatar;
    }
}

main();
