const search_buttons = document.querySelectorAll('.searchbar-button');
const search_submit = document.querySelector('.searchbar-submit');

// When the icon is clicked, submit the search form
search_buttons.forEach((button) => {
    button.addEventListener('click', () => {
        search_submit.click();
    });
});

if (localStorage.getItem('theme') === null) {
    localStorage.setItem('theme', 'light-theme');
    document.body.classList.add('light-theme');
} else {
    document.body.classList.add(localStorage.getItem('theme'));
}

const theme_icons = document.querySelectorAll('.theme-icon');
theme_icons.forEach((icon) => {
    icon.addEventListener('click', () => {
        const theme = icon.getAttribute('data-theme');
        document.body.classList.add('light-theme', 'dark-theme');
        document.body.classList.remove(theme);
        localStorage.setItem('theme', document.body.classList[0]);
    });
});
