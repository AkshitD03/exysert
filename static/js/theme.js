$(document).ready(function() {
    // Check the initial theme preference
    let currentTheme = localStorage.getItem('theme') ? localStorage.getItem('theme') : 'light';
    
    // Apply the saved theme
    applyTheme(currentTheme);

    // Function to apply the selected theme
    function applyTheme(theme) {
        if (theme === 'light') {
            $('link[href="/static/css/light_results.css"]').attr('disabled', false);
            $('link[href="/static/css/styles_light.css"]').attr('disabled', false);
            $('link[href="/static/css/styles_dark.css"]').attr('disabled', true);
            $('link[href="/static/css/dark-results.css"]').attr('disabled', true);
        } else {
            $('link[href="/static/css/light_results.css"]').attr('disabled', true);
            $('link[href="/static/css/styles_light.css"]').attr('disabled', true);
            $('link[href="/static/css/styles_dark.css"]').attr('disabled', false);
            $('link[href="/static/css/dark-results.css"]').attr('disabled', false);
        }
        localStorage.setItem('theme', theme);
    }

    // Event listener for theme toggle button
    $('#theme-toggle').click(function() {
        if (currentTheme === 'light') {
            currentTheme = 'dark';
        } else {
            currentTheme = 'light';
        }
        applyTheme(currentTheme);
    });
});
