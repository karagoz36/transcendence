// @ts-check
/** @param {Event} e */
function onAccordionClicked(e) {
	/** @type { NodeList } */
	const accordionContent = document.querySelectorAll(".accordion-collapse.collapsing")

	if (accordionContent.length == 1) {
		const toChange = document.querySelector(".accordion-collapse.collapsing")
		toChange?.classList.add("show")
		toChange?.classList.add("collapse")
		toChange?.classList.remove("collapsing")
	}
}

function keepOneAccordionOpened() {
	/** @type { NodeListOf<HTMLButtonElement> } */
	const buttons = document.querySelectorAll("button>.accordion-button")
	buttons.forEach(button => button.onclick = onAccordionClicked)
}

keepOneAccordionOpened()