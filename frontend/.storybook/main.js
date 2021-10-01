module.exports = {
  addons: [
    // "@storybook/addon-a11y",
    "@storybook/addon-essentials",
    "storybook-addon-next-router",
    "storybook-css-modules-preset"
    // "msw-storybook-addon"
  ],
  stories: [
    "../compositions/**/*.stories.tsx",
    "../shared-components/**/*.stories.tsx",
    "../pages/**/*.stories.tsx"
  ]
}
