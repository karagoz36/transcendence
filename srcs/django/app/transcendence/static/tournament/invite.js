// @ts-check

import {getPage} from "../global/SPA.js"

/** @param {SubmitEvent} e */
async function onSubmit(e) {
    e.preventDefault()
    if (!e.target)
        return
    await getPage(`/tournament/invite/?username=${e.target["username"].value}`, {}, false)
}

function main() {
    /** @type {NodeListOf<HTMLFormElement>} */
    const forms = document.querySelectorAll("form#tournament-invite")

    forms.forEach(form => {
        form.onsubmit = onSubmit
    })
}

main()