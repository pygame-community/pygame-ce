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
        document.body.classList.remove('light-theme', 'dark-theme');
        document.body.classList.add(theme);
        localStorage.setItem('theme', theme);
    });
});
