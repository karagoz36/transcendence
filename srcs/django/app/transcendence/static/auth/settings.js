/** @param {SubmitEvent} e */
async function handleSettingsUpdate(e) {
    e.preventDefault();
    if (!e.target) {
        throw new Error("handleSettingsUpdate: e.target is null");
    }

    /** @type {HTMLFormElement} */
    const form = e.target;

    /** Collect form data */
    const username = form['username'].value;
    const email = form['email'].value;
    const is_2fa_enabled = form['is_2fa_enabled'].checked;
    const csrftoken = form['csrfmiddlewaretoken'].value;
    const avatar = form['avatar'].files[0];
    const password = form['password'].value;
    const alias = form['alias'].value;

    console.log("CSRF Token:", csrftoken);
    console.log("Collected Data:", { username, email, avatar, is_2fa_enabled });

    try {
        // Créer un objet FormData pour inclure l'avatar et les autres données
        const formData = new FormData();
        formData.append("username", username);
        formData.append("email", email);
        formData.append("password", password);
        formData.append("alias", alias);
        formData.append("is_2fa_enabled", is_2fa_enabled);
        formData.append("avatar", avatar);
        
        const response = await fetch("/api/settings/update/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
            },
            body: formData,
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log("Settings update response:", data);
            alert("Settings updated successfully!");
            location.reload();
        } else {
            const errorData = await response.json();
            alert("Error updating settings: " + (errorData.error || "Unknown error"));
        }
    } catch (err) {
        console.error("Error in handleSettingsUpdate:", err);
        alert("An unexpected error occurred. Please try again.");
    }
}


/** Remove avatar logic */
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
            location.reload();
        } else {
            const errorData = await response.json();
            alert("Error removing avatar: " + (errorData.error || "Unknown error"));
        }
    } catch (err) {
        console.error("Error in handleRemoveAvatar:", err);
        alert("An unexpected error occurred. Please try again.");
    }
}

/** Initialize event listeners */
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
