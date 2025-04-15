export default {
  content: ["./src/**/*.tsx", "./src/**/*.css"],
  plugins: [require("@tailwindcss/forms")],
  theme: {
    extend: {
      colors: {
        black: "#1f1f1f",
        white: "#f5f5f5",
        primary: "#4d5ed8",
        secondary: "#f98927",
      },
    },
  },
};
