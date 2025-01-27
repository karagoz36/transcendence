async function onBtnClick() {
    await fetch(window.location.href)
}

async function main() {
    /** @type {HTMLButtonElement} */
    const btn = document.querySelector("#join-running-game")
    btn.onclick = onBtnClick
}

main()