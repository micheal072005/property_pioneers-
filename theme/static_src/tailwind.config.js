/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],


    theme: {
        extend: {
            colors: {
                // Deep Navy Blue - Professional, trustworthy, stable
                primary: {
                    50:  '#F0F4F8',
                    100: '#D9E2EC',
                    200: '#BCCCDC',
                    300: '#9FB3C8',
                    400: '#829AB1',
                    500: '#1E3A5F',   // Main brand navy
                    600: '#152C47',
                    700: '#0F2137',
                    800: '#0A1628',
                    900: '#050C18',
                },
                // Elegant Gold - Luxury, premium, success
                accent: {
                    50:  '#FFFBF0',
                    100: '#FFF4D6',
                    200: '#FFE8AD',
                    300: '#FFDC84',
                    400: '#FFD05B',
                    500: '#C5A572',   // Sophisticated muted gold
                    600: '#A68A5E',
                    700: '#876F4A',
                    800: '#685436',
                    900: '#493922',
                },
                // Neutral Grays - Clean, professional, modern
                neutral: {
                    50:  '#F8F9FA',
                    100: '#F1F3F5',
                    200: '#E9ECEF',
                    300: '#DEE2E6',
                    400: '#ADB5BD',
                    500: '#6C757D',
                    600: '#495057',
                    700: '#343A40',
                    800: '#212529',
                    900: '#0D1117',
                },
            },
            fontFamily: {
                serif: ['"Playfair Display"', 'serif'],
                sans: ['"Inter"', 'sans-serif'],
            },
        },
    },


    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
