// @ts-check

function main() {
	const urlParams = new URLSearchParams(window.location.search)
	if (urlParams.get("register") != null) {
		document.querySelector("#collapse-login")?.classList.remove("show")
		document.querySelector("#collapse-register")?.classList.add("show")
	}
}

main()
