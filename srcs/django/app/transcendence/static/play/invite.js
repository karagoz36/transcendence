// @ts-check
import {getPage} from "../global/SPA.js"

/** @param {MouseEvent} e */
async function invite(e) {
    /** @type {HTMLButtonElement} */ // @ts-ignore
    const button = e.target
    /** @type {string} */ // @ts-ignore
    const username = button.getAttribute("friend-username")
    await getPage(`/api/play/send-invite?username=${username}`)
}

function main() {
    /** @type {NodeListOf<HTMLButtonElement>} */
    const buttons = document.querySelectorAll("button#invite")
    buttons.forEach(button => button.onclick = invite)
}

main()