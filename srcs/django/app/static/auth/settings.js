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
    console.log("CSRF Token:", csrftoken);
    console.log("Collected Data:", { username, email, is_2fa_enabled });

    try {
        const response = await fetch("/api/settings/update/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify({ username, email, is_2fa_enabled }),
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

/** Initialize event listeners */
function main() {
    /** @type {HTMLFormElement|null} */
    const form = document.querySelector("#settings-form");
    if (!form) {
        throw new Error("main: Unable to find settings form");
    }
    form.onsubmit = handleSettingsUpdate;
}

main();
