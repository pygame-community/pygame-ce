
const htmlElement = document.documentElement;

if (localStorage.getItem('theme') === null) {
    localStorage.setItem('theme', 'light-theme');
    htmlElement.classList.add('light-theme');
} else {
    htmlElement.classList.add(localStorage.getItem('theme'));
}

// Execute once the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const search_buttons = document.querySelectorAll('.searchbar-button');
    const search_submit = document.querySelector('.searchbar-submit');

    // When the icon is clicked, submit the search form
    search_buttons.forEach((button) => {
        button.addEventListener('click', () => {
            search_submit.click();
        });
    });

    const theme_icons = document.querySelectorAll('.theme-icon');
    theme_icons.forEach((icon) => {
        icon.addEventListener('click', () => {
            const theme = icon.getAttribute('data-theme');
            htmlElement.classList.add('light-theme', 'dark-theme');
            htmlElement.classList.remove(theme);
            localStorage.setItem('theme', htmlElement.classList[0]);
        });
    });
});
