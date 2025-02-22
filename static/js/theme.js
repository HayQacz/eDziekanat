document.addEventListener('DOMContentLoaded', function() {
    const themeSwitch = document.getElementById('themeSwitch');
    const currentTheme = localStorage.getItem('theme') || 'light';
    setTheme(currentTheme);
    themeSwitch.checked = currentTheme === 'dark';

    themeSwitch.addEventListener('change', function() {
        const theme = themeSwitch.checked ? 'dark' : 'light';
        setTheme(theme);
    });

    function setTheme(theme) {
        if (theme === 'dark') {
            document.body.classList.add('dark-theme');
            document.body.classList.remove('light-theme');
        } else {
            document.body.classList.add('light-theme');
            document.body.classList.remove('dark-theme');
        }
        localStorage.setItem('theme', theme);
    }
});
