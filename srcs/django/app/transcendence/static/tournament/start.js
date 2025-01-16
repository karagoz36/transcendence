async function main() {
    /** @type {HTMLButtonElement} */
    const button = document.querySelector("button#start-tournament")
    button.onclick = async () => {
        await fetch("/tournament/start/")
    }
}

main()