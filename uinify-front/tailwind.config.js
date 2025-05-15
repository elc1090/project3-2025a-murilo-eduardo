module.exports = {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Work Sans"', "sans-serif"],
      },
      colors: {
        "orange-accent": "#F36711",
        primary: "#07183b",
        secondary: "#091f4c",
        accent: "#4f82c1",
        "accent-2": "#0f2d69",
      },
    },
  },
  plugins: [],
};
