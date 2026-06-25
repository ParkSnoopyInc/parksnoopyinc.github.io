const root = document.documentElement;
const toggle = document.querySelector("[data-theme-toggle]");
const storedTheme = localStorage.getItem("wheel-index-theme");
const preferredTheme = window.matchMedia("(prefers-color-scheme: dark)").matches
	? "dark"
	: "light";

function applyTheme(theme) {
	root.dataset.theme = theme;
	if (toggle) {
		toggle.textContent = theme === "dark" ? "Light Mode" : "Dark Mode";
		toggle.setAttribute("aria-pressed", String(theme === "dark"));
	}
}

applyTheme(storedTheme || preferredTheme);

toggle?.addEventListener("click", () => {
	const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
	localStorage.setItem("wheel-index-theme", nextTheme);
	applyTheme(nextTheme);
});
